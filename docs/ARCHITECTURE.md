# Architecture

## Lifecycle

```text
preflight renderer + extension registries
  -> verify exact adapter and Fusion source gitlinks, indexes, HEADs, clean states, and trees
  -> detect exact Rechiseled/Fusion JAR tuple
  -> validate active first-wins structural closure
  -> compile 5,822 bounded Fusion programs
  -> route exactly the 1,743 generated allowlist IDs
  -> retain 593 source sheets and 4,802 collision-probe output keys
  -> crop active logical tiles during resource bake
  -> render original selected model geometry with connected materials
```

The process route begins inactive. Both registry IDs are preflighted before
either registration. A collision, missing tuple, structural hash mismatch,
dimension mismatch, unsupported AST, required-resource failure, or synthetic
texture collision leaves the entire route inactive. Operator disablement uses
`bluemap.rechiseled.disabledProfiles` or
`BLUEMAP_RECHISELED_DISABLED_PROFILES` with profile ID
`rechiseled-fusion-1.2.5-1.3.12`.

The source-bundled adapter API owns the exact 5.23 runtime identity, guarded
registry operations, resource-extension wrapper, and synthetic dispatch check.
The add-on still owns its entrypoint, runtime, route, renderer, diagnostics,
resource admission, and fallback policy. No module JAR is nested or installed.

## Exact profile

The profile generator consumes the two exact operator-supplied artifacts and
emits only identities, hashes, allowlists, counts, dimensions, and layout names.
It locks 1,743 routed blockstates, 5,825 Rechiseled model resources (5,822
direct custom models plus three internal stock parents), 593 PNGs, and 590
metadata files. Six `minecraft:*` geometry parents plus their shared transitive
`minecraft:block/block` parent form a separately hash-locked seven-path host
model ABI; they are not part of the Rechiseled closure or route ownership.

The route contains 569 propertyless cubes, 12 axis pillars, 581 slabs, and 581
stairs. Waterlogged is preserved for slabs/stairs. No block entity, NBT, camo,
animation, connected glass, or appearance-proxy behavior is interpreted.

Structural blockstate/model/metadata bytes remain exact. PNG bytes may be
overridden when their layout dimensions remain exact. The validator reads
archive entries while BlueMap's ZIP filesystem is open and retains only bounded
model bytes and override identities; third-party resource bytes are not stored
in the add-on.

## Program model

Each custom variant model compiles into immutable child-first texture and
connection maps. Allowed predicate nodes are `or`, `and`, `is_direction`,
`match_block`, `match_state`, and `is_same_state`. Aliases begin with `#` and
are cycle checked. `match_block` compares native ID only; `match_state`
compares native ID plus its listed property values and ignores extra persisted
properties; `is_same_state` compares the complete native state and rejects air.

Horizontal x/z axis children inherit geometry/textures but override all face
keys through `#all` to `is_same_state`. Axis y uses the base predicates and can
interconnect with its matching slab/stair family. No NeoForge appearance hook
or proxy projection is attempted.

## Geometry and texture orientation

The emitter starts from the original BlueMap-selected variant and baked model.
It retains element geometry, default/explicit face UV, face rotation, element
transform, variant transform, UV-lock, cullface, tint, lighting, AO, cave
removal, top-only filtering, random offset, and map-color semantics.

After all transforms, it derives the final face normal and the world directions
of decreasing V (`U`) and increasing U (`R`). The eight texture orientations
map predicate directions independently of mask slots. Neighbor offsets are:

```text
T=U, TR=U+R, R=R, BR=-U+R,
B=-U, BL=-U-R, L=-R, TL=U-R
```

This final-quad derivation is required for x/z pillars and UV-locked stairs;
local face constants are insufficient. Lighting, culling, top-only filtering,
and map color also use final directions.

Five neutral model types compile from the exact source-module gitlink into the
add-on JAR. The consumer-local `TextureLayout` maps by enum name only at the
selector call. Resource admission, profile parsing, predicates, tile catalogs,
route activation, fallback, and mesh emission remain local.

## Sheet layouts

Source sheets are cropped into collision-safe `bluemap_rechiseled:tiles/*`
textures without overwriting installed keys. The exact output count is 4,802.
All output keys are included in BlueMap's texture filter so an operator-provided
collision is observable before any mutation.

| Layout | Sheets | Logical grid | Physical input |
| --- | ---: | --- | --- |
| Plain | 3 | 1×1 | 16×16 |
| PIECED | 499 | 5×1 | 80×16 |
| FULL | 43 | 8×6 | legacy 128×128; bottom two rows ignored |
| HORIZONTAL | 36 | 4×1 | 64×16 |
| VERTICAL | 8 | 1×4 | 16×64 |
| SIMPLE | 4 | 4×4 | 64×64 |

FULL selects 47 reachable cells; tile 41 and physical rows 6–7 are never
emitted. PIECED uses five whole-face shortcuts. Other masks clip the original
UV polygon against the global U/V 0.5 quadrants, preserve the original UV
coordinates and geometry, and triangulate only non-zero-area intersections.
Cullface is evaluated once before splitting.

## Failure and stock semantics

Per-block rendering records its geometry start and initial map color. Any
malformed state/resource/runtime failure resets both and invokes the original
pre-extension blockstate through BlueMap's stock `ResourceModelRenderer`.
Capacity exhaustion is deliberately not contained. Diagnostics are bounded and
contain no coordinates, state properties, NBT, player data, or world data.

Generated active tiles are alpha checked for every exact and overridden sheet.
Discarded FULL padding and unreachable tile 41 do not de-solidify a family,
while the reachable purpur tile-40 alpha anomaly correctly makes affected
full/axis and double-slab states non-culling and non-occluding. Top/bottom
slabs and stairs remain non-full.
