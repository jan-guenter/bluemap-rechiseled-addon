# BlueMap Rechiseled Add-on

This standalone MIT BlueMap add-on renders the connected models installed by
Rechiseled 1.2.5 and Fusion 1.3.12 on the exact All the Mons 1.2.0 baseline.
Version `0.1.0-alpha.2` source-bundles the released MIT BlueMap Fusion Resource
Models module from an exact gitlink. The module replaces four repository-local
helper/selector types without changing the six-layout profile, predicates,
route, fallback, or emitter. The `0.1.0-alpha.1` release candidate is
runtime-gated and owner visually accepted; its evidence is recorded in
[`docs/STAGING.md`](docs/STAGING.md).

## Exact contract

Activation requires both byte-exact operator-installed artifacts:

- `rechiseled-1.2.5-neoforge-mc1.21.jar`, 11,498,611 bytes, SHA-256
  `7bf14cf8a4bfdc4b6c990126a75da29fd2bb7559d1c05b71e29c8fd5ae044435`;
- `fusion-1.3.12-neoforge-mc1.21.1.jar`, 923,270 bytes, SHA-256
  `17f5215648a98bcde4134577b013200dbf363273ae282449c51408ae8346f2fa`.

The add-on owns exactly 1,743 `rechiseled:*_connecting` block IDs and 50,571
legal states. It leaves the other 1,884 Rechiseled IDs and 54,660 states on
BlueMap's stock path. It never registers or routes a `fusion:*` block.

| Routed shape | IDs | Legal states |
| --- | ---: | ---: |
| Full cube | 569 | 569 |
| Axis pillar | 12 | 36 |
| Slab | 581 | 3,486 |
| Stairs | 581 | 46,480 |
| **Total** | **1,743** | **50,571** |

The generated metadata locks 1,743 blockstates, 5,825 Rechiseled model
resources, 593 PNG sheets, and 590 Fusion metadata files. The add-on bundles
none of those third-party bytes. A separate seven-path Minecraft host-model ABI
locks the six external geometry parents and their shared transitive parent. At
runtime the add-on reads the active operator-installed resources, validates
both structural closures, crops 4,802 collision-safe tile textures, and emits
the original BlueMap model geometry with connected materials.

## Rendering behavior

The renderer preserves original blockstate selection, full/slab/stair/pillar
geometry, model and variant transforms, partial UV rectangles, face rotation,
UV-lock, culling, AO, lighting, cave removal, top-only rendering, map color,
alpha, and capacity failures. It implements the exact `pieced`, `full`,
`horizontal`, `vertical`, and `simple` layouts. Legacy FULL sheets use only the
active 8×6 cells; transparent rows 6–7 and unreachable tile 41 are excluded.

Connection predicates support only the exact bounded AST:
`or`, `and`, `is_direction`, `match_block`, `match_state`, and
`is_same_state`. Native Rechiseled states are compared directly; block-entity,
NBT, camo, appearance-proxy, animation, and RechiseledCreate bridge behavior
are outside this tranche.

Any route-wide tuple, schema, required-resource, or registry collision leaves
the entire route inactive. A malformed individual observation atomically
discards partial geometry and renders the original pre-extension blockstate
through BlueMap's stock renderer. `MaxCapacityReachedException` propagates.

The shared module supplies axis arithmetic, direction masks, texture
orientation, layout names, and sheet selection. `TextureLayout` remains local
and maps by enum name at the selector call. This profile still admits exactly
`PLAIN`, `PIECED`, `FULL`, `HORIZONTAL`, `VERTICAL`, and `SIMPLE`.

Pixel-only resource-pack overrides remain supported when sheet dimensions stay
exact. Structural JSON and Fusion metadata remain hash-locked. Active tile
alpha is checked for exact and overridden sheets alike, so the reachable
purpur FULL tile-40 anomaly and alpha-bearing overrides safely disable
full-cube culling for affected states.

## Build and review

Java 21 and the exact local BlueMap 5.22 backport checkout are required. The
focused local tranche gate is shown below. Clone with `--recurse-submodules`,
or initialize an existing checkout with `git submodule update --init --recursive`.
The settings preflight rejects a missing, dirty, staged, wrong-commit, or
source-tree-mismatched Fusion module checkout.

```bash
python3 tools/verify_pinned_artifacts.py \
  --rechiseled /absolute/path/rechiseled-1.2.5-neoforge-mc1.21.jar \
  --fusion /absolute/path/fusion-1.3.12-neoforge-mc1.21.1.jar
python3 gallery/generate.py --check
python3 -m unittest discover -s tools/tests -p 'test_*.py'
gradle --no-daemon \
  -PrechiseledJar=/absolute/path/rechiseled-1.2.5-neoforge-mc1.21.jar \
  -PfusionJar=/absolute/path/fusion-1.3.12-neoforge-mc1.21.1.jar \
  test checkstyleMain checkstyleTest compileJava compileTestJava
```

Pull-request CI performs the authoritative clean build, production/sources JAR
boundary audit, POM generation, and artifact verification once. Both archive
gates require the exact shared source/class roster once and reject displaced
local types. See
[`docs/RELEASING.md`](docs/RELEASING.md).

The owner-accepted candidate is commit
`382ad2c3178026d727a3e3785a2674d3b87b35f5`. Its 645,622-byte production JAR
has SHA-256
`39793187b97b504e085664a23eb5e54961dfdeac1e9ccf57e1bd701bd90c0242`.
This identity is a reviewed release candidate, not yet a published release.

## Gallery

`gallery/` deterministically generates 1,924 logical cases and 2,271 verified
placements: all 1,743 routed IDs in isolated negative-coordinate swatches, 179
structural cases, and two untouched stock controls. Structural cases cover all
layouts, representative eight-neighbor masks, sheet edges, PIECED splitting,
all 80 stair states for one family, every axis pillar in x/y/z, shape
interconnection, and glowstone. The 68 requested non-straight stair targets
have deterministic same-half perpendicular supports placed before the targets.

## Licensing

Project code is MIT. Both exact Rechiseled and Fusion artifacts declare
`All rights reserved`; they are runtime inputs only. No upstream code, classes,
JSON, models, textures, or binaries from either artifact are redistributed.
BlueMap MIT renderer mechanics retain attribution. See
[`LICENSE-BlueMap`](LICENSE-BlueMap),
[`THIRD_PARTY.md`](THIRD_PARTY.md) and
[`docs/PROVENANCE.md`](docs/PROVENANCE.md).
