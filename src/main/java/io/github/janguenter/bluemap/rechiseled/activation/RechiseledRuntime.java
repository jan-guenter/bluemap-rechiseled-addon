/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.rechiseled.activation;

import io.github.janguenter.bluemap.rechiseled.adapter.bluemap523.FusionProgramCatalog;

/** Process-scoped state for the single exact Rechiseled/Fusion route. */
public final class RechiseledRuntime {

    public static final String ROUTE_ID = "rechiseled-fusion-1.2.5-1.3.12";
    public static final RechiseledRuntime INSTANCE = new RechiseledRuntime();

    private final RouteActivation route = new RouteActivation(ROUTE_ID);
    private volatile FusionProgramCatalog catalog;

    private RechiseledRuntime() {
    }

    public RouteActivation route() {
        return route;
    }

    public FusionProgramCatalog catalog() {
        return catalog;
    }

    public synchronized void activate(FusionProgramCatalog installedCatalog) {
        catalog = java.util.Objects.requireNonNull(installedCatalog, "installedCatalog");
        route.activate();
    }

    public synchronized void inactive(String detail) {
        catalog = null;
        route.inactive(detail);
    }

    public void disable(String detail) {
        catalog = null;
        route.fail(detail);
    }
}
