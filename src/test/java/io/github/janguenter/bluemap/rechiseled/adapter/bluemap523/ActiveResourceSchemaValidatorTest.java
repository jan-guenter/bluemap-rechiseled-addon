/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.rechiseled.adapter.bluemap523;

import io.github.janguenter.bluemap.rechiseled.profile.TextureCatalog;
import io.github.janguenter.bluemap.rechiseled.profile.TextureLayout;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.net.URI;
import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ActiveResourceSchemaValidatorTest {

    private static final TextureCatalog.Entry EXPECTED = new TextureCatalog.Entry(
            TextureLayout.PIECED, 80, 16, "0".repeat(64)
    );

    @Test
    void acceptsPixelOverridesButRejectsLayoutDimensionChanges(@TempDir Path temporary)
            throws IOException {
        Path changedPixels = temporary.resolve("changed.png");
        write(changedPixels, 80, 16, 0xff12ab34);
        assertTrue(ActiveResourceSchemaValidator.validTexture(changedPixels, EXPECTED));

        Path wrongDimensions = temporary.resolve("wrong.png");
        write(wrongDimensions, 79, 16, 0xff12ab34);
        assertFalse(ActiveResourceSchemaValidator.validTexture(wrongDimensions, EXPECTED));
    }

    @Test
    void validatesImagesThroughAnOpenZipFileSystem(@TempDir Path temporary)
            throws IOException {
        Path zip = temporary.resolve("resources.zip");
        URI uri = URI.create("jar:" + zip.toUri());
        try (FileSystem fileSystem = FileSystems.newFileSystem(uri, Map.of("create", "true"))) {
            Path image = fileSystem.getPath("/assets/rechiseled/textures/block/example.png");
            Files.createDirectories(image.getParent());
            write(image, 80, 16, 0xffabcdef);
            assertTrue(ActiveResourceSchemaValidator.validTexture(image, EXPECTED));
        }
    }

    @Test
    void alphaBearingOverrideTilesFailSafeOutOfFullCubeCulling() throws IOException {
        KeyAndTexture opaque = texture(16, 16, 0xffffffff);
        KeyAndTexture transparent = texture(16, 16, 0x00123456);
        assertTrue(RechiseledResourceExtension.opaqueTexture(opaque.texture()));
        assertFalse(RechiseledResourceExtension.opaqueTexture(transparent.texture()));
    }

    @Test
    void doubleSlabsUseTheOpaqueFullCubePropertyLane() {
        de.bluecolored.bluemap.core.world.BlockState doubled =
                new de.bluecolored.bluemap.core.world.BlockState(
                        de.bluecolored.bluemap.core.util.Key.parse(
                                "rechiseled:test_slab_connecting"
                        ),
                        Map.of("type", "double")
                );
        de.bluecolored.bluemap.core.world.BlockState bottom =
                new de.bluecolored.bluemap.core.world.BlockState(
                        de.bluecolored.bluemap.core.util.Key.parse(
                                "rechiseled:test_slab_connecting"
                        ),
                        Map.of("type", "bottom")
                );
        assertTrue(RechiseledResourceExtension.isDoubleSlab(doubled));
        assertFalse(RechiseledResourceExtension.isDoubleSlab(bottom));
    }

    @Test
    void fullOpacitySkipsOnlyTheProvenUnreachableTile41() {
        TextureCatalog.Entry full = new TextureCatalog.Entry(
                TextureLayout.FULL, 128, 128, "0".repeat(64)
        );
        assertTrue(RechiseledResourceExtension.reachableTile(full, 40));
        assertFalse(RechiseledResourceExtension.reachableTile(full, 41));
        assertTrue(RechiseledResourceExtension.reachableTile(full, 47));
    }

    @Test
    void bakedAtlasRemapsMustPreserveExactSheetDimensions() {
        TextureCatalog.Entry entry = new TextureCatalog.Entry(
                TextureLayout.PIECED, 80, 16, "0".repeat(64)
        );
        assertTrue(RechiseledResourceExtension.validBakedSheetDimensions(
                new BufferedImage(80, 16, BufferedImage.TYPE_INT_ARGB), entry
        ));
        assertFalse(RechiseledResourceExtension.validBakedSheetDimensions(
                new BufferedImage(160, 16, BufferedImage.TYPE_INT_ARGB), entry
        ));
    }

    private static KeyAndTexture texture(int width, int height, int color)
            throws IOException {
        BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);
        java.awt.Graphics2D graphics = image.createGraphics();
        try {
            graphics.setColor(new java.awt.Color(color, true));
            graphics.fillRect(0, 0, width, height);
        } finally {
            graphics.dispose();
        }
        de.bluecolored.bluemap.core.util.Key key =
                de.bluecolored.bluemap.core.util.Key.parse("test:texture");
        return new KeyAndTexture(
                key,
                de.bluecolored.bluemap.core.resources.pack.resourcepack.texture.Texture.from(
                        key, image
                )
        );
    }

    private record KeyAndTexture(
            de.bluecolored.bluemap.core.util.Key key,
            de.bluecolored.bluemap.core.resources.pack.resourcepack.texture.Texture texture
    ) {
    }

    private static void write(Path path, int width, int height, int color) throws IOException {
        BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);
        image.setRGB(width / 2, height / 2, color);
        try (java.io.OutputStream output = Files.newOutputStream(path)) {
            ImageIO.write(image, "png", output);
        }
    }
}
