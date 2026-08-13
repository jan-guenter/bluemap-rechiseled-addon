# Provenance

## Implementation lineage

The immediate structural foundation is the owner-authored MIT BlueMap Chisel
Add-on tree at commit `3a300b85f5371a6bf42fd7c8d998fc3b55239dd6`.
Its release lineage includes tag `v0.1.0-alpha.1` commit
`f9131a5143062e2045cf26823aabb8628bb5d94d`. That scaffold supplied build,
profile, activation, diagnostics, gallery, documentation, CI, and resumable
release mechanics. It was fully retargeted; no Chisel runtime claim remains.

The earlier owner-authored MIT BlueMap Chipped Add-on tag
`v0.1.0-alpha.1`, commit
`c474a82b6bfd1b4173d119cb1e053a5458167e4b`, is the scaffold's additional
profile/resource-extension lineage.

Geometry, UV-lock, lighting, AO, culling, cave, top-only, map-color, random
offset, and model-selection mechanics in `FusionModelEmitter` adapt BlueMap
5.22's MIT `ResourceModelRenderer` at the audited backport commit
`9be321df995a1103808621d529eb72773e719d4d`. The affected file retains the
BlueMap copyright and MIT notice.
The complete BlueMap notice is also retained in `LICENSE-BlueMap` and packaged
as `META-INF/LICENSE-BlueMap` in both published JARs.

Fusion predicate, orientation, selector, cropping, and PIECED clipping logic is
independently authored from exact runtime JSON schemas and observable behavior.

## ARR runtime inputs

The exact Rechiseled 1.2.5 and Fusion 1.3.12 NeoForge descriptors both declare
`All rights reserved`. Neither codebase is copied or adapted. Their JARs are
operator-installed runtime/verification inputs; the add-on bundles no code,
classes, JSON, model, texture, metadata, capture, mesh, or binary from them.

Version-correlated reference-only source identities are:

- Rechiseled `neoforge-1.21` commit
  `e9e806c3ef3d0277a006e7fc9de4fff74d34dcd7`;
- Fusion `neoforge-1.21` commit
  `bace466e1c4f116ff2df535aadab690c81160a0e`.

Those checkouts were reference-only semantic corroboration, not code-reuse,
build, licensing, or reproducibility inputs; no source expression was copied
or adapted. Neither checkout supplies a license file, while the exact runtime
descriptors explicitly say ARR.

## Generated evidence

`tools/generate_profile.py` verifies SHA-1/SHA-256/SHA-512 and size for both
artifacts, independently regenerates the exact allowlist/resource closure, and
emits only first-party metadata. It also emits a separate hash-only seven-path
Minecraft host-model ABI for the external model-parent chain. Generated
definitions, paths, dimensions, hashes, and layout names are facts, not
redistributed upstream expression.

`provenance/upstreams.json` is the machine-readable identity record.
