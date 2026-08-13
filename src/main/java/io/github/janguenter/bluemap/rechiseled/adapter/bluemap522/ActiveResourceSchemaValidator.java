/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.rechiseled.adapter.bluemap522;

import de.bluecolored.bluemap.core.resources.pack.resourcepack.ResourcePack;
import de.bluecolored.bluemap.core.util.Key;
import io.github.janguenter.bluemap.rechiseled.profile.Rechiseled125Fusion1312Profile;
import io.github.janguenter.bluemap.rechiseled.profile.ResourceManifest;
import io.github.janguenter.bluemap.rechiseled.profile.TextureCatalog;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HashMap;
import java.util.HexFormat;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.Map;
import java.util.Set;

/** Validates the first-wins active exact resource closure and compiles its model programs. */
final class ActiveResourceSchemaValidator {

    private static final int BUFFER_SIZE = 64 * 1024;
    private static final int MAX_MODEL_BYTES = 256 * 1024;

    private ActiveResourceSchemaValidator() {
    }

    static Result validate(
            ResourcePack resourcePack,
            Iterable<Path> roots,
            ResourceManifest manifest,
            TextureCatalog textures
    ) throws IOException, InterruptedException {
        Map<String, Capture> active = new LinkedHashMap<>();
        Map<String, Capture> activeHostModels = new LinkedHashMap<>();
        for (Path root : roots) {
            if (Thread.interrupted()) {
                throw new InterruptedException();
            }
            resourcePack.loadResourcePath(root, activeRoot -> {
                collect(activeRoot, manifest, textures, active, true);
                collect(
                        activeRoot,
                        Rechiseled125Fusion1312Profile.HOST_MODELS,
                        textures,
                        activeHostModels,
                        false
                );
            });
        }
        if (active.size() != manifest.entries().size()) {
            return Result.invalid("required-resource-closure-missing");
        }
        if (activeHostModels.size()
                != Rechiseled125Fusion1312Profile.HOST_MODELS.entries().size()) {
            return Result.invalid("host-geometry-abi-missing");
        }
        for (Capture capture : activeHostModels.values()) {
            if (!capture.valid()) {
                return Result.invalid("host-geometry-abi-mismatch");
            }
        }

        Map<String, byte[]> models = new HashMap<>();
        Set<Key> pixelOverrides = new LinkedHashSet<>();
        for (ResourceManifest.Entry entry : manifest.entries().values()) {
            if (Thread.interrupted()) {
                throw new InterruptedException();
            }
            Capture capture = active.get(entry.path());
            if (capture == null || !capture.valid()) {
                return Result.invalid("active-resource-integrity-mismatch");
            }
            if (entry.kind().equals("model")) {
                models.put(entry.path(), capture.modelBytes());
            } else if (entry.kind().equals("texture") && capture.pixelOverride()) {
                pixelOverrides.add(textureKey(entry.path()));
            }
        }
        try {
            return Result.success(FusionProgramCatalog.parse(models), pixelOverrides);
        } catch (IllegalArgumentException exception) {
            return Result.invalid("active-fusion-schema-mismatch");
        }
    }

    private static void collect(
            Path root,
            ResourceManifest manifest,
            TextureCatalog textures,
            Map<String, Capture> active,
            boolean requireRechiseledRoot
    ) throws IOException {
        if (requireRechiseledRoot && !Files.isDirectory(root.resolve("assets/rechiseled"))) {
            return;
        }
        for (ResourceManifest.Entry entry : manifest.entries().values()) {
            String path = entry.path();
            if (active.containsKey(path)) {
                continue;
            }
            Path candidate = root.resolve(path);
            if (Files.isRegularFile(candidate)) {
                active.put(path, capture(candidate, entry, textures));
            }
        }
    }

    private static Capture capture(
            Path resource,
            ResourceManifest.Entry entry,
            TextureCatalog textures
    ) throws IOException {
        if (entry.kind().equals("texture")) {
            TextureCatalog.Entry texture = textures.get(textureKey(entry.path()));
            boolean valid = texture != null && validTexture(resource, texture);
            boolean pixelOverride = valid && !entry.sha256().equals(sha256(resource));
            return new Capture(valid, null, pixelOverride);
        }
        boolean valid = Files.size(resource) == entry.size()
                && entry.sha256().equals(sha256(resource));
        if (!valid || !entry.kind().equals("model")) {
            return new Capture(valid, null, false);
        }
        if (entry.size() > MAX_MODEL_BYTES) {
            return new Capture(false, null, false);
        }
        return new Capture(true, Files.readAllBytes(resource), false);
    }

    static boolean validTexture(Path resource, TextureCatalog.Entry texture) throws IOException {
        BufferedImage image;
        try (InputStream input = Files.newInputStream(resource)) {
            image = ImageIO.read(input);
        }
        return image != null && image.getWidth() == texture.width()
                && image.getHeight() == texture.height();
    }

    private static Key textureKey(String path) {
        String prefix = "assets/rechiseled/textures/";
        if (!path.startsWith(prefix) || !path.endsWith(".png")) {
            throw new IllegalArgumentException("malformed texture manifest path");
        }
        return Key.parse("rechiseled:" + path.substring(prefix.length(), path.length() - 4));
    }

    private static String sha256(Path path) throws IOException {
        MessageDigest digest;
        try {
            digest = MessageDigest.getInstance("SHA-256");
        } catch (NoSuchAlgorithmException exception) {
            throw new IllegalStateException("SHA-256 unavailable", exception);
        }
        byte[] buffer = new byte[BUFFER_SIZE];
        try (InputStream input = Files.newInputStream(path)) {
            int read;
            while ((read = input.read(buffer)) >= 0) {
                digest.update(buffer, 0, read);
            }
        }
        return HexFormat.of().formatHex(digest.digest());
    }

    record Result(
            boolean valid,
            String reason,
            FusionProgramCatalog catalog,
            Set<Key> pixelOverrides
    ) {

        private static Result success(
                FusionProgramCatalog catalog,
                Set<Key> pixelOverrides
        ) {
            return new Result(
                    true, "exact-active-schema", catalog, Set.copyOf(pixelOverrides)
            );
        }

        private static Result invalid(String reason) {
            return new Result(false, reason, null, Set.of());
        }
    }

    private record Capture(boolean valid, byte[] modelBytes, boolean pixelOverride) {
    }
}
