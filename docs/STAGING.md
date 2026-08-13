# Staging

No runtime result is recorded yet. Use only the disposable shared BlueMap test
server/PVC; never production state.

## Gate

1. Install the reviewed CI production JAR beside exact Rechiseled 1.2.5,
   Fusion 1.3.12, the pack dependencies, and the pinned BlueMap backport.
2. Reset/reuse the disposable world and install the packaged gallery datapack.
3. Apply the workspace staging gamerules that disable time/weather/random
   ticks/mobs/patrols/phantoms/traders/wardens/spawners/PvP/movement checks,
   damage, raids, and global sounds.
4. Run `function rechiseled_gallery:build` and
   `function rechiseled_gallery:verify`; require exact generated counters and
   zero failures.
5. Render the bounded gallery map and retain the add-on activation/fallback
   diagnostics and raw render audit.
6. Restart the same pod cleanly and rerun `verify` without rebuilding.
7. Open the exact BlueMap link in the agent browser for the required lightweight
   nonblank/nonbroken sanity check before presenting it to the owner.
8. Have the owner compare Minecraft and BlueMap. Record acceptance only after
   explicit confirmation.

The gallery is intentionally bold: 1,743 isolated routes plus normalized
layout/mask/topology/axis/glowstone cases in one bounded render cycle. It does
not claim arbitrary resource packs, RechiseledCreate, or production worlds.
