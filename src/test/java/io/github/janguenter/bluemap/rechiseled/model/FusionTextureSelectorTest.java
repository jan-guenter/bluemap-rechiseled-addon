/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.rechiseled.model;

import io.github.janguenter.bluemap.rechiseled.profile.TextureLayout;
import io.github.janguenter.bluemap.resource.fusion.model.FusionDirection;
import io.github.janguenter.bluemap.resource.fusion.model.FusionTextureLayout;
import io.github.janguenter.bluemap.resource.fusion.model.FusionTextureSelector;
import org.junit.jupiter.api.Test;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class FusionTextureSelectorTest {

    @Test
    void matchesFrozenOutputForEveryAdmittedLayoutAndMask()
            throws NoSuchAlgorithmException {
        for (TextureLayout layout : TextureLayout.values()) {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            for (int mask = 0; mask < 256; mask++) {
                digest.update((byte) select(layout, mask));
            }
            assertEquals(
                    expectedDigest(layout),
                    HexFormat.of().formatHex(digest.digest()),
                    layout.name()
            );
            assertEquals(layout.name(), sharedLayout(layout).name());
            assertThrows(IllegalArgumentException.class, () -> select(layout, -1));
            assertThrows(IllegalArgumentException.class, () -> select(layout, 256));
        }
    }

    @Test
    void matchesEveryFrozenPiecedCornerMask() {
        int[] expected = {0, 3, 2, 4, 0, 3, 2, 1};
        for (FusionDirection direction : FusionDirection.values()) {
            for (int mask = 0; mask < 256; mask++) {
                int selectedMask = mask;
                if (isCorner(direction)) {
                    assertEquals(
                            expected[cornerIndex(mask, direction)],
                            FusionTextureSelector.piecedCorner(mask, direction),
                            direction + " " + mask
                    );
                } else {
                    assertThrows(
                            IllegalArgumentException.class,
                            () -> FusionTextureSelector.piecedCorner(
                                    selectedMask, direction
                            ),
                            direction + " " + mask
                    );
                }
            }
        }
    }

    private static int select(TextureLayout layout, int mask) {
        return FusionTextureSelector.tile(sharedLayout(layout), mask);
    }

    private static FusionTextureLayout sharedLayout(TextureLayout layout) {
        return FusionTextureLayout.valueOf(layout.name());
    }

    private static String expectedDigest(TextureLayout layout) {
        return switch (layout) {
            case PLAIN ->
                    "5341e6b2646979a70e57653007a1f310169421ec9bdd9f1a5648f75ade005af1";
            case PIECED ->
                    "92dcecde86b0a9befe3e02cd1f80c9d59aafd013e189df752d155355c62cf88a";
            case FULL ->
                    "bfd54c79f43a7ed6c02e34f967b75aa7abba4a9b94d88f0226281734164fb3b5";
            case HORIZONTAL ->
                    "7a10cda30a7d6b4c16b13f46c93568d55ae36fbc9de4adceecfb18b2f3447e8a";
            case VERTICAL ->
                    "7e1a5e61d61d4bd72457368f6f14afa2b4454912fc5f152444f3a0bf3c5af14a";
            case SIMPLE ->
                    "e5fff2bdef5286ec6523e8a2a9d93ee0f770f47fdfe7d0dd7aa8e40056992e34";
        };
    }

    private static int cornerIndex(int mask, FusionDirection direction) {
        return switch (direction) {
            case TOP_LEFT -> bit(mask, FusionDirection.LEFT)
                    | bit(mask, FusionDirection.TOP) << 1
                    | bit(mask, FusionDirection.TOP_LEFT) << 2;
            case TOP_RIGHT -> bit(mask, FusionDirection.RIGHT)
                    | bit(mask, FusionDirection.TOP) << 1
                    | bit(mask, FusionDirection.TOP_RIGHT) << 2;
            case BOTTOM_LEFT -> bit(mask, FusionDirection.LEFT)
                    | bit(mask, FusionDirection.BOTTOM) << 1
                    | bit(mask, FusionDirection.BOTTOM_LEFT) << 2;
            case BOTTOM_RIGHT -> bit(mask, FusionDirection.RIGHT)
                    | bit(mask, FusionDirection.BOTTOM) << 1
                    | bit(mask, FusionDirection.BOTTOM_RIGHT) << 2;
            default -> throw new IllegalArgumentException("not a corner");
        };
    }

    private static int bit(int mask, FusionDirection direction) {
        return mask >> direction.bit() & 1;
    }

    private static boolean isCorner(FusionDirection direction) {
        return switch (direction) {
            case TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT -> true;
            default -> false;
        };
    }
}
