/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.rechiseled.profile;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ExactModArtifactDetectorTest {

    @Test
    void acceptsOnlyTheUniqueExactDualArtifactTuple(@TempDir Path temporary)
            throws IOException {
        Path rechiseled = required("rechiseledJar");
        Path fusion = required("fusionJar");
        assertTrue(ExactModArtifactDetector.matchesRequiredPair(List.of(rechiseled, fusion)));
        assertFalse(ExactModArtifactDetector.matchesRequiredPair(List.of(rechiseled)));
        Path duplicate = temporary.resolve("duplicate-rechiseled.jar");
        Files.copy(rechiseled, duplicate);
        assertFalse(ExactModArtifactDetector.matchesRequiredPair(List.of(
                rechiseled, duplicate, fusion
        )));
    }

    private static Path required(String property) {
        String value = System.getProperty(property);
        if (value == null || value.isBlank()) {
            throw new AssertionError("missing exact test artifact property: " + property);
        }
        return Path.of(value);
    }
}
