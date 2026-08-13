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

Status: generated/static only. No server placement, render, restart, browser, or
owner visual result has been recorded for this tranche.
