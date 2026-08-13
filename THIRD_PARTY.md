# Third-party and provenance inventory

| Component | Role | Exact identity | License | Bundled |
| --- | --- | --- | --- | --- |
| BlueMap | Compile-time ABI and adapted renderer semantics | Backport `5.22-agent.backport-5.22-mc1.21.1-2`, commit `9be321df995a1103808621d529eb72773e719d4d` | MIT | License notice only |
| BlueMap Chisel Add-on | MIT scaffold/build/activation/release mechanics | scaffold commit `3a300b85f5371a6bf42fd7c8d998fc3b55239dd6`; release tag `v0.1.0-alpha.1`, commit `f9131a5143062e2045cf26823aabb8628bb5d94d` | MIT | No |
| BlueMap Chipped Add-on | Earlier MIT profile/resource-extension mechanics | tag `v0.1.0-alpha.1`, commit `c474a82b6bfd1b4173d119cb1e053a5458167e4b` | MIT | No |
| Rechiseled | Operator-installed blocks/models/textures | `1.2.5`, 11,498,611 bytes, SHA-256 `7bf14cf8a4bfdc4b6c990126a75da29fd2bb7559d1c05b71e29c8fd5ae044435` | All rights reserved | No |
| Fusion | Operator-installed model/texture format resources | `1.3.12`, 923,270 bytes, SHA-256 `17f5215648a98bcde4134577b013200dbf363273ae282449c51408ae8346f2fa` | All rights reserved | No |
| JUnit Jupiter | Tests | 5.11.4 BOM | EPL-2.0 | No |
| Checkstyle | Source style | 10.18.2 | LGPL-2.1-or-later | No |

Version-correlated Rechiseled and Fusion source checkouts were reference-only
semantic corroboration, not code-reuse, build, licensing, or reproducibility
inputs; no source expression was copied or adapted. Exact runtime JSON/PNG
metadata and observable behavior establish the bounded interface implemented
independently here. Production and sources JAR audits reject third-party
classes, nested JARs, and `assets/rechiseled/`.

BlueMap's complete MIT copyright and permission notice is retained in
`LICENSE-BlueMap` and packaged as `META-INF/LICENSE-BlueMap` in both the
production and sources JARs.

The complete machine-readable record is `provenance/upstreams.json`.
