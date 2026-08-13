# Rechiseled staging gallery

This deterministic datapack contains exactly 1,924 logical cases and 2,271
verified placements:

- 1,743 isolated swatches, one for every routed Rechiseled ID;
- 179 structural cases spanning every sheet layout, representative masks,
  PIECED splits, FULL edges/padding exclusion, slab/stair/axis topology,
  cross-shape predicates, and glowstone;
- two untouched stock controls: one unrouted Rechiseled block and vanilla stone.

The isolated section deliberately uses negative coordinates. One representative
stair family covers all 80 legal states. Each of its non-straight targets, plus
the PIECED and glowstone non-straight witnesses, has a deterministic same-half
perpendicular support placed first; all 68 supports and targets are independently
verified. All 12 axis IDs cover x/y/z. The full isolated census contains all 27
routed glowstone IDs.

Generate or check it with `python3 gallery/generate.py --check`, package it with
`gallery/package.sh <output.zip>`, then use:

```text
/function rechiseled_gallery:build
/function rechiseled_gallery:verify
/function rechiseled_gallery:pose
/function rechiseled_gallery:release
```

The scoreboard counters persist across a same-world restart. Require generated
`#swatches`, `#structures`, `#controls`, and `#checked` counts plus zero
`#failures`. The datapack bundles only first-party IDs, states, coordinates,
commands, and metadata—no Rechiseled or Fusion assets.

Status: owner-accepted release candidate, publication pending. On 2026-08-13,
the corrected 27,563-byte gallery archive (SHA-256
`9d749c9e98775379e52645d598395dc94a37109808df7ac99633ee8f24e09201`)
produced all 1,924 logical cases and verified all 2,271 placements with zero
failures. The exact production JAR and bounded render passed startup, a clean
same-pod restart without gallery rebuilding, the canonical raw render audit,
and the agent browser sanity check before the owner visually accepted the
result. See [`../docs/STAGING.md`](../docs/STAGING.md) for the exact candidate
and evidence identities.
