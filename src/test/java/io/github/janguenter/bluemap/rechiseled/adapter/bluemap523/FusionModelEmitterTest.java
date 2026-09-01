/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.rechiseled.adapter.bluemap523;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class FusionModelEmitterTest {

    @Test
    void piecedClippingDropsZeroAreaSlabSeams() {
        assertEquals(4, FusionModelEmitter.piecedPartCount(0F, 0F, 1F, 1F));
        assertEquals(2, FusionModelEmitter.piecedPartCount(0F, 0.5F, 1F, 1F));
        assertEquals(1, FusionModelEmitter.piecedPartCount(0F, 0.5F, 0.5F, 1F));
        assertEquals(0, FusionModelEmitter.piecedPartCount(0F, 0.5F, 1F, 0.5F));
    }
}
