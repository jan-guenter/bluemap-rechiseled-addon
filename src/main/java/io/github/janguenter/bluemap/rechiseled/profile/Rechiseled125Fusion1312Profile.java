/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.rechiseled.profile;

import java.util.Map;
import java.util.Set;

/** Exact All the Mons 1.2.0 Rechiseled/Fusion profile. */
public final class Rechiseled125Fusion1312Profile {

    public static final String PROFILE_ID = "rechiseled-fusion-1.2.5-1.3.12";
    public static final String RECHISELED_SHA256 =
            "7bf14cf8a4bfdc4b6c990126a75da29fd2bb7559d1c05b71e29c8fd5ae044435";
    public static final long RECHISELED_SIZE = 11_498_611L;
    public static final String FUSION_SHA256 =
            "17f5215648a98bcde4134577b013200dbf363273ae282449c51408ae8346f2fa";
    public static final long FUSION_SIZE = 923_270L;
    public static final int ALL_BLOCK_COUNT = 3_627;
    public static final int ROUTED_BLOCK_COUNT = 1_743;
    public static final int ROUTED_STATE_COUNT = 50_571;
    public static final int STOCK_BLOCK_COUNT = 1_884;
    public static final int STOCK_STATE_COUNT = 54_660;
    public static final int DIRECT_MODEL_COUNT = 5_822;
    public static final int MODEL_COUNT = 5_825;
    public static final int TEXTURE_COUNT = 593;
    public static final int METADATA_COUNT = 590;
    public static final int RESOURCE_COUNT = 8_751;
    public static final int HOST_MODEL_COUNT = 7;
    public static final String DEFINITIONS_SHA256 =
            "34fd46b5f0967bdc19434fbd78e1013110726d6e090fcf77206602b3544863d1";
    public static final String RESOURCES_SHA256 =
            "514b11f0181b6f8ac451c834d9a9f71c5213a062e74236f669927738007d8ac9";
    public static final String TEXTURES_SHA256 =
            "eeccade45fcdab86bd04362e5ff1695b327576671852af23891db9f0d6f83526";
    public static final String HOST_MODELS_SHA256 =
            "99575da08068de74de57bdd47281195b58c679966ea68ebea89597dd3c2b83fb";

    public static final DefinitionCatalog CATALOG = DefinitionCatalog.load(
            "/bluemap-rechiseled/profiles/rechiseled/1.2.5-fusion-1.3.12/definitions.tsv",
            ROUTED_BLOCK_COUNT,
            DEFINITIONS_SHA256
    );
    public static final Map<String, RechiseledDefinition> DEFINITIONS = CATALOG.definitions();
    public static final Set<String> ROUTED_BLOCKS = DEFINITIONS.keySet();
    public static final ResourceManifest RESOURCES = ResourceManifest.load(
            "/bluemap-rechiseled/profiles/rechiseled/1.2.5-fusion-1.3.12/required-resources.tsv",
            RESOURCE_COUNT,
            RESOURCES_SHA256
    );
    public static final TextureCatalog TEXTURES = TextureCatalog.load(
            "/bluemap-rechiseled/profiles/rechiseled/1.2.5-fusion-1.3.12/textures.tsv",
            TEXTURE_COUNT,
            TEXTURES_SHA256
    );
    public static final ResourceManifest HOST_MODELS = ResourceManifest.load(
            "/bluemap-rechiseled/profiles/rechiseled/1.2.5-fusion-1.3.12/host-models.tsv",
            HOST_MODEL_COUNT,
            HOST_MODELS_SHA256,
            "minecraft"
    );

    private Rechiseled125Fusion1312Profile() {
    }
}
