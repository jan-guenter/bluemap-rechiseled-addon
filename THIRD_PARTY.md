# Third-party and provenance inventory

| Component | Role | Exact identity | License | Bundled |
| --- | --- | --- | --- | --- |
| BlueMap | Compile-time ABI and adapted renderer semantics | Feature-backport `5.22-feature.backport-5.23-stateless-java-web-server-46`, commit `7e07f4e74ec1e92a6ead9aa1e66054af3e133aac`, API `285c9a60eff3ac2b0cab308ce1058d1565be0971` | MIT | License notice only |
| BlueMap Chisel Add-on | MIT scaffold/build/activation/release mechanics | scaffold commit `3a300b85f5371a6bf42fd7c8d998fc3b55239dd6`; release tag `v0.1.0-alpha.1`, commit `f9131a5143062e2045cf26823aabb8628bb5d94d` | MIT | No |
| BlueMap Chipped Add-on | Earlier MIT profile/resource-extension mechanics | tag `v0.1.0-alpha.1`, commit `c474a82b6bfd1b4173d119cb1e053a5458167e4b` | MIT | No |
| BlueMap Fusion Resource Models | First-party neutral Fusion model source | `0.1.0-alpha.1`, commit `3ddd5d39bb7cc8664c242aedd849a636316075c2`, source tree `6e85031ff2f0e7417a7a2fb0babbf7ed5a4f218a` | MIT | Five sources compile into this add-on; no module JAR |
| BlueMap Add-on Adapter API | First-party BlueMap 5.23 bootstrap source | `0.1.0-alpha.2`, commit `e81f08bc4bfbf02d810ec8949a019130e2e61634`, source tree `2f974c9bb2ba13888d69682f86f30f58922d30eb` | MIT | Four sources compile into this add-on; no module JAR |
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
