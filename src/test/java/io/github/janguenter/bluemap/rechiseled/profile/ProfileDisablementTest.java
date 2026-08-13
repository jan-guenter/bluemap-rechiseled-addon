/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.rechiseled.profile;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ProfileDisablementTest {

    @Test
    void mergesNormalizedPropertyAndEnvironmentLists() {
        ProfileDisablement disabled = ProfileDisablement.from(
                "rechiseled-fusion-1.2.5-1.3.12, invalid value",
                "RECHISELED-FUSION-1.2.5-1.3.12,other"
        );
        assertTrue(disabled.isDisabled(Rechiseled125Fusion1312Profile.PROFILE_ID));
        assertEquals(2, disabled.disabledProfiles().size());
    }
}
