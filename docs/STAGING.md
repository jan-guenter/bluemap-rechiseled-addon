# Staging

## Accepted BlueMap 5.23 result

The owner accepted Rechiseled in the combined All the Mons 1.2.0 BlueMap 5.23
integration gallery on 2026-09-01. The reviewed v37 component record pinned
source commit `9f2a46ba2ade03274c61129a4e54dfcb2add42d3` and the sealed
650,002-byte CI base JAR with SHA-256
`e28b83c30e56b8f779751093008e9d49ea1a7d9e08ea54cb384780c1eac938d8`.
The integration composer replaced only the entrypoint class. The resulting
650,048-byte reviewed JAR has SHA-256
`9881d5803126128890097f51b4a7ef8a357c23beb48d8eaf0882bffb9794ea9d`.

The exact composer entrypoint source, SHA-256
`a16af40382ae45c15908614d90baaa8fcccf230158b56eee60d7759813ba6e42`,
was promoted into the repository. Its reviewed class SHA-256 is
`b85a128b6ab1b73f4accdd967c43f3b12a2816894217436f94207a10b2d80bca`.
Authoritative pull-request CI run `33528747904` at commit
`b8ad0dea2a46f361489c097deb75a4090d302914` reproduced that exact class
and built the sealed release candidate.

The CI production JAR is 650,048 bytes with SHA-256
`95c9e026b4b2826be67b594390c69b1c4d2d5c1036152fa5a36271a82a66ff33`.
All 94 entry payloads and their order are byte-identical to the reviewed JAR.
Only bit 11 of every ZIP entry's general-purpose flag differs. Gradle sets the
UTF-8-name flag, while the integration composer's Python ZIP rewrite cleared
it for the same ASCII entry names. This metadata does not change any packaged
byte presented to BlueMap.

This acceptance covers the combined disposable integration gallery and the
exact entry payloads above. It does not claim a production deployment,
arbitrary resource packs, or RechiseledCreate behavior.

## Historical accepted result

The owner accepted the original rendered result on 2026-08-13. It was published
as immutable prerelease `0.1.0-alpha.1`. The accepted candidate identities were:

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
   Fusion 1.3.12, the pack dependencies, and the pinned BlueMap backport. If an
   integration harness rewrites ZIP metadata, require identical entry payloads
   and order and record the exact archive-only difference.
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
