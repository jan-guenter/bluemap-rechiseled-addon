# Staging

## Accepted result

The owner accepted the rendered result on 2026-08-13. Publication remains
pending. The accepted release-candidate identities are:

- reviewed commit:
  `382ad2c3178026d727a3e3785a2674d3b87b35f5`;
- production JAR: 645,622 bytes, SHA-256
  `39793187b97b504e085664a23eb5e54961dfdeac1e9ccf57e1bd701bd90c0242`;
- corrected gallery archive: 27,563 bytes, SHA-256
  `9d749c9e98775379e52645d598395dc94a37109808df7ac99633ee8f24e09201`;
- canonical raw render audit: 176,116 bytes, SHA-256
  `3a269f762485cdce3995a7344935f439f031f07b3f939ee487d4e1bd49e8537c`.

The disposable shared server/PVC started cleanly with the exact candidate,
built all 1,924 logical gallery cases, and verified all 2,271 placements with
zero failures. The bounded BlueMap render and canonical raw audit passed. The
same pod then stopped and restarted cleanly; verification again covered all
2,271 placements without rebuilding the gallery. The exact review link passed
the required lightweight agent-browser sanity check before presentation, and
the owner subsequently confirmed visual acceptance.

This evidence is limited to the disposable staging world. It does not claim a
client-connection test, arbitrary resource packs, a production world, or
production deployment.

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
