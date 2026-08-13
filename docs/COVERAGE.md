# Coverage

## Exact census

| Category | Routed IDs | Legal states |
| --- | ---: | ---: |
| Full | 569 | 569 |
| Axis | 12 | 36 |
| Slab | 581 | 3,486 |
| Stairs | 581 | 46,480 |
| **Routed** | **1,743** | **50,571** |
| Stock Rechiseled | **1,884** | **54,660** |

The generated installed-resource closure is 8,751 paths: 1,743 blockstates,
5,825 models, 593 PNGs, and 590 Fusion metadata files. Layout counts are 499
PIECED, 43 FULL, 36 HORIZONTAL, eight VERTICAL, four SIMPLE, and three plain.
The separate host-model ABI locks seven Minecraft model paths: six external
geometry parents and their shared transitive parent.
Exactly 27 routed glowstone IDs use ordinary installed block/element lighting;
the add-on invents no emissive material.

## Focused automated coverage

- all 256 FULL masks with canonical table SHA-256
  `bfd54c79f43a7ed6c02e34f967b75aa7abba4a9b94d88f0226281734164fb3b5`;
- all 256 inputs for SIMPLE, HORIZONTAL, and VERTICAL;
- PIECED shortcuts and all eight corner indices;
- all eight texture orientations on every final face plus predicate remapping;
- `match_block`, projected `match_state`, complete `is_same_state`, direction,
  AND, and OR semantics, bounded to the exact five-level/14-node maximum;
- parsing all 5,822 exact custom programs and resolving every rendered material
  key;
- exact shape/state/resource/layout counts, seven-path host ABI, and
  dual-artifact activation;
- pixel overrides, dimension rejection, ZIP-backed image reads, alpha-safe
  culling, and double-slab full-cube properties;
- PIECED full/half/quarter UV clipping with zero-area seam rejection;
- deterministic gallery/checksum and profile regeneration.

## Deterministic gallery

The generated gallery has exactly 1,924 logical cases and 2,271 verified
placements:

| Gallery group | Logical cases |
| --- | ---: |
| Isolated routed-ID swatches | 1,743 |
| Structural cases | 179 |
| Untouched stock controls | 2 |

Structural coverage includes all six sheet types; representative cardinal,
diagonal, edge, all-connected, and PIECED split masks; FULL tiles 40, 46, and
47, including the active purpur tile-40 alpha anomaly; explicit exclusion of
unreachable 41/padding rows; all six slab states plus connected top/bottom
PIECED slab and connected PIECED stair partial-UV witnesses;
all 80 stair states for one family; x/y/z for all 12 axis IDs; same-axis and
cross-shape connection witnesses; all routed glowstone IDs in the isolated
census plus full/slab/stair structures; and negative coordinates. Every one of
the 68 non-straight stair targets has a non-overlapping same-half perpendicular
support placed first, and both target and final straight support states are
verified.

The exact owner-accepted candidate at commit
`382ad2c3178026d727a3e3785a2674d3b87b35f5` completed the disposable staging
gate on 2026-08-13. Its 1,924-case gallery produced all 2,271 expected
placements with zero verification failures, rendered successfully, and
remained valid after a clean same-pod restart without rebuilding. The
645,622-byte production JAR has SHA-256
`39793187b97b504e085664a23eb5e54961dfdeac1e9ccf57e1bd701bd90c0242`;
the corrected 27,563-byte gallery has SHA-256
`9d749c9e98775379e52645d598395dc94a37109808df7ac99633ee8f24e09201`.
The canonical 176,116-byte raw render audit has SHA-256
`3a269f762485cdce3995a7344935f439f031f07b3f939ee487d4e1bd49e8537c`.
The exact BlueMap view passed the agent browser sanity check and the owner
visually accepted it. No client-connection or production-world result is
claimed, and publication remains pending.

## Exclusions

Unrouted Rechiseled blocks, RechiseledCreate, `rechiseled_chipped` recipe-only
integration, `fusion:*` blocks, connected glass, appearance proxies, block
entities, NBT, camo, animation, and mutable machine state remain stock or out of
scope.
