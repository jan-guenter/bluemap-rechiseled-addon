/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.rechiseled.profile;

import org.junit.jupiter.api.Test;

import java.util.EnumMap;
import java.util.Map;
import java.util.stream.Collectors;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class RechiseledProfileTest {

    @Test
    void locksRouteAndLegalStateCensus() {
        Map<ShapeFamily, Long> shapes = Rechiseled125Fusion1312Profile.DEFINITIONS.values()
                .stream()
                .collect(Collectors.groupingBy(
                        RechiseledDefinition::shape,
                        () -> new EnumMap<>(ShapeFamily.class),
                        Collectors.counting()
                ));
        assertEquals(Map.of(
                ShapeFamily.FULL, 569L,
                ShapeFamily.AXIS, 12L,
                ShapeFamily.SLAB, 581L,
                ShapeFamily.STAIRS, 581L
        ), shapes);
        int legalStates = Rechiseled125Fusion1312Profile.DEFINITIONS.values()
                .stream().mapToInt(RechiseledDefinition::legalStates).sum();
        assertEquals(50_571, legalStates);
        assertEquals(1_743, Rechiseled125Fusion1312Profile.ROUTED_BLOCKS.size());
        assertTrue(Rechiseled125Fusion1312Profile.ROUTED_BLOCKS.stream()
                .allMatch(id -> id.startsWith("rechiseled:") && id.endsWith("_connecting")));
        assertFalse(Rechiseled125Fusion1312Profile.ROUTED_BLOCKS.stream()
                .anyMatch(id -> id.startsWith("fusion:")));
    }

    @Test
    void locksInstalledResourceClosureAndLayoutCensus() {
        Map<String, Long> resources = Rechiseled125Fusion1312Profile.RESOURCES.entries()
                .values().stream()
                .collect(Collectors.groupingBy(
                        ResourceManifest.Entry::kind, Collectors.counting()
                ));
        assertEquals(Map.of(
                "blockstate", 1_743L,
                "model", 5_825L,
                "texture", 593L,
                "metadata", 590L
        ), resources);
        Map<TextureLayout, Long> layouts = Rechiseled125Fusion1312Profile.TEXTURES.entries()
                .values().stream()
                .collect(Collectors.groupingBy(
                        TextureCatalog.Entry::layout, Collectors.counting()
                ));
        assertEquals(Map.of(
                TextureLayout.PLAIN, 3L,
                TextureLayout.PIECED, 499L,
                TextureLayout.FULL, 43L,
                TextureLayout.HORIZONTAL, 36L,
                TextureLayout.VERTICAL, 8L,
                TextureLayout.SIMPLE, 4L
        ), layouts);
        assertEquals(6, TextureLayout.FULL.rows());
        assertEquals(8, TextureLayout.FULL.physicalRows());
        assertEquals(7, Rechiseled125Fusion1312Profile.HOST_MODELS.entries().size());
        assertTrue(Rechiseled125Fusion1312Profile.HOST_MODELS.entries().keySet().stream()
                .allMatch(path -> path.startsWith("assets/minecraft/models/block/")));
        assertTrue(Rechiseled125Fusion1312Profile.HOST_MODELS.entries().containsKey(
                "assets/minecraft/models/block/block.json"
        ));
        Rechiseled125Fusion1312Profile.TEXTURES.entries().forEach((key, entry) -> {
            assertTrue(key.getFormatted().startsWith("rechiseled:block/"));
            assertEquals(16, entry.width() / entry.layout().columns());
            assertEquals(16, entry.height() / entry.layout().physicalRows());
        });
    }
}
