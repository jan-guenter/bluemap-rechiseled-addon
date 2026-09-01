/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.rechiseled.adapter.bluemap523;

import de.bluecolored.bluemap.core.util.Key;
import io.github.janguenter.bluemap.rechiseled.profile.Rechiseled125Fusion1312Profile;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class FusionProgramCatalogTest {

    private static final Set<String> CUBE = Set.of(
            "down", "east", "north", "side", "south", "up", "west"
    );
    private static final Set<String> SHAPE = Set.of("bottom", "side", "top");
    private static final Set<String> HORIZONTAL_AXIS = Set.of(
            "all", "down", "east", "north", "side", "south", "up", "west"
    );

    @Test
    void parsesEveryExactCustomModelAndResolvesAllMaterialPredicates()
            throws IOException {
        Map<String, byte[]> models = exactModels(required("rechiseledJar"));
        FusionProgramCatalog catalog = FusionProgramCatalog.parse(models);
        assertEquals(5_822, catalog.size());

        Map<Set<String>, Long> keysets = catalog.programs().values().stream()
                .map(program -> program.connections().keySet())
                .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
        assertEquals(1_162L, keysets.get(CUBE));
        assertEquals(4_648L, keysets.get(SHAPE));
        assertEquals(12L, keysets.get(HORIZONTAL_AXIS));

        for (FusionProgramCatalog.Program program : catalog.programs().values()) {
            assertFalse(program.textures().isEmpty());
            Set<String> materials = program.connections().keySet().equals(SHAPE)
                    ? SHAPE : Set.of("down", "east", "north", "south", "up", "west");
            for (String material : materials) {
                assertFalse(program.predicate(material) instanceof FusionPredicate.Never,
                        () -> "unresolved material " + material + " in " + program.model());
            }
        }
    }

    @Test
    void everyDirectVariantModelHasAnExactProgram() throws IOException {
        Path jar = required("rechiseledJar");
        FusionProgramCatalog catalog = FusionProgramCatalog.parse(exactModels(jar));
        int selected = 0;
        Set<Key> unique = new HashSet<>();
        try (ZipFile zip = new ZipFile(jar.toFile())) {
            for (String path : Rechiseled125Fusion1312Profile.RESOURCES.entries().keySet()) {
                if (!path.contains("/blockstates/")) {
                    continue;
                }
                String json = new String(
                        zip.getInputStream(zip.getEntry(path)).readAllBytes(),
                        StandardCharsets.UTF_8
                );
                com.google.gson.JsonObject variants = com.google.gson.JsonParser.parseString(json)
                        .getAsJsonObject().getAsJsonObject("variants");
                for (Map.Entry<String, com.google.gson.JsonElement> entry
                        : variants.entrySet()) {
                    com.google.gson.JsonObject variant = entry.getValue().getAsJsonObject();
                    Key model = Key.parse(variant.get("model").getAsString());
                    assertNotNull(catalog.get(model), () -> "missing program for " + model);
                    unique.add(model);
                    selected++;
                }
            }
        }
        assertEquals(25_588, selected);
        assertEquals(5_822, unique.size());
    }

    private static Map<String, byte[]> exactModels(Path jar) throws IOException {
        Map<String, byte[]> models = new HashMap<>();
        try (ZipFile zip = new ZipFile(jar.toFile())) {
            Rechiseled125Fusion1312Profile.RESOURCES.entries().forEach((path, manifest) -> {
                if (!manifest.kind().equals("model")) {
                    return;
                }
                ZipEntry entry = zip.getEntry(path);
                assertNotNull(entry, path);
                try {
                    models.put(path, zip.getInputStream(entry).readAllBytes());
                } catch (IOException exception) {
                    throw new java.io.UncheckedIOException(exception);
                }
            });
        } catch (java.io.UncheckedIOException exception) {
            throw exception.getCause();
        }
        assertEquals(5_825, models.size());
        assertTrue(models.keySet().stream().allMatch(
                path -> path.startsWith("assets/rechiseled/models/")
        ));
        return models;
    }

    private static Path required(String property) {
        String value = System.getProperty(property);
        if (value == null || value.isBlank()) {
            throw new AssertionError("missing exact test artifact property: " + property);
        }
        return Path.of(value);
    }
}
