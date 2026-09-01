/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.rechiseled;

import io.github.janguenter.bluemap.addon.adapter.api.bluemap523.BlueMapRuntimeCompatibility;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

/** BlueMap add-on entrypoint installed before resource-pack construction. */
public final class BlueMapRechiseledAddon implements Runnable {

    public BlueMapRechiseledAddon() {
    }

    @Override
    public void run() {
        try {
            if (!BlueMapRuntimeCompatibility.matchesCurrent()) {
                inactive("unsupported BlueMap internal ABI", null);
                return;
            }
            Class<?> adapter = Class.forName(
                    "io.github.janguenter.bluemap.rechiseled.adapter.bluemap523.BlueMap523Adapter",
                    true,
                    BlueMapRechiseledAddon.class.getClassLoader()
            );
            Method install = adapter.getMethod("install");
            Object integrationCandidateInstallResult = install.invoke(null);
            if (!Boolean.TRUE.equals(integrationCandidateInstallResult)) {
                inactive("candidate adapter installation rejected", null);
                return;
            }
            System.out.println("BlueMap ATMons integration candidate activated: rechiseled@7e07f4e74ec1e92a6ead9aa1e66054af3e133aac");
        } catch (InvocationTargetException exception) {
            inactive("exact adapter initialization failed", exception.getCause());
        } catch (ReflectiveOperationException | LinkageError | RuntimeException exception) {
            inactive("exact adapter is unavailable", exception);
        }
    }

    private static void inactive(String reason, Throwable cause) {
        String detail = cause == null ? "" : " (" + cause.getClass().getSimpleName() + ")";
        System.err.println("BlueMap Rechiseled add-on is inactive: " + reason + detail + ".");
    }
}
