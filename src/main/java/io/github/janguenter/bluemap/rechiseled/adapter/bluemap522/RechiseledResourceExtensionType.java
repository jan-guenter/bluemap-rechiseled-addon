/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.rechiseled.adapter.bluemap522;

import de.bluecolored.bluemap.core.resources.pack.resourcepack.ResourcePack;
import de.bluecolored.bluemap.core.util.Key;
import io.github.janguenter.bluemap.rechiseled.activation.RechiseledRuntime;

/** Resource-pack extension factory registered before resource loading begins. */
final class RechiseledResourceExtensionType
        implements ResourcePack.Extension<RechiseledResourceExtension> {

    static final Key KEY = Key.parse("bluemap_rechiseled:exact_profile");

    private final RechiseledRuntime runtime;

    RechiseledResourceExtensionType(RechiseledRuntime runtime) {
        this.runtime = runtime;
    }

    @Override
    public Key getKey() {
        return KEY;
    }

    @Override
    public RechiseledResourceExtension create(ResourcePack pack) {
        return new RechiseledResourceExtension(pack, runtime);
    }
}
