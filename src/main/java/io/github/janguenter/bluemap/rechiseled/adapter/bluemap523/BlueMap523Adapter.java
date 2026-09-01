/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.rechiseled.adapter.bluemap523;

import de.bluecolored.bluemap.core.map.hires.block.BlockRendererType;
import de.bluecolored.bluemap.core.resources.pack.resourcepack.ResourcePack;
import de.bluecolored.bluemap.core.util.Key;
import io.github.janguenter.bluemap.addon.adapter.api.bluemap523.RegistryGuard;
import io.github.janguenter.bluemap.addon.adapter.api.bluemap523.ResourceExtensionType;
import io.github.janguenter.bluemap.rechiseled.activation.RechiseledRuntime;

/** BlueMap 5.23 feature-backport ABI boundary. */
public final class BlueMap523Adapter {

    private static final RechiseledRuntime RUNTIME = RechiseledRuntime.INSTANCE;
    private static final Key EXTENSION_KEY =
            Key.parse("bluemap_rechiseled:exact_profile");
    static final Key RENDERER_KEY =
            Key.parse("bluemap_rechiseled:fusion_model");
    private static final BlockRendererType RENDERER = new BlockRendererType.Impl(
            RENDERER_KEY,
            (pack, gallery, settings) -> new RechiseledRenderer(pack, gallery, settings, RUNTIME)
    );
    private static final ResourcePack.Extension<RechiseledResourceExtension> EXTENSION =
            new ResourceExtensionType<>(
                    EXTENSION_KEY,
                    pack -> new RechiseledResourceExtension(pack, RUNTIME)
            );

    private BlueMap523Adapter() {
    }

    public static synchronized boolean install() {
        if (!RegistryGuard.canRegister(BlockRendererType.REGISTRY, RENDERER)
                || !RegistryGuard.canRegister(ResourcePack.Extension.REGISTRY, EXTENSION)) {
            RUNTIME.disable("registry-collision");
            return false;
        }
        if (!RegistryGuard.register(BlockRendererType.REGISTRY, RENDERER)
                || !RegistryGuard.register(ResourcePack.Extension.REGISTRY, EXTENSION)) {
            RUNTIME.disable("registry-collision");
            return false;
        }
        return true;
    }

    static BlockRendererType renderer() {
        return RENDERER;
    }

    static RechiseledResourceExtension extension(ResourcePack resourcePack) {
        return resourcePack.getExtension(EXTENSION);
    }

    static ResourcePack.Extension<RechiseledResourceExtension> extensionType() {
        return EXTENSION;
    }
}
