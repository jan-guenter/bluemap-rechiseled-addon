# Compatibility

The only supported activation tuple is:

- All the Mons 1.2.0, pack commit
  `c7bb230f21d14d26859d0b92548f089b3a493ad9`;
- Minecraft 1.21.1 and NeoForge 21.1.248;
- Java 21;
- BlueMap feature-backport version
  `5.22-feature.backport-5.23-stateless-java-web-server-46`, commit
  `7e07f4e74ec1e92a6ead9aa1e66054af3e133aac`, API commit
  `285c9a60eff3ac2b0cab308ce1058d1565be0971`;
- exact Rechiseled 1.2.5 and Fusion 1.3.12 artifacts from README;
- BlueMap Fusion Resource Models `0.1.0-alpha.1`, commit
  `3ddd5d39bb7cc8664c242aedd849a636316075c2`, source tree
  `6e85031ff2f0e7417a7a2fb0babbf7ed5a4f218a`.
- BlueMap Add-on Adapter API `0.1.0-alpha.2`, commit
  `e81f08bc4bfbf02d810ec8949a019130e2e61634`, source tree
  `2f974c9bb2ba13888d69682f86f30f58922d30eb`.

This is evidence-locked compatibility, not a general version range. A changed
artifact byte identity, resource schema, BlueMap ABI, pack version, Minecraft
version, or loader baseline requires a fresh profile and release.

The add-on is a plain BlueMap add-on. It registers no Minecraft content,
networking, NeoForge hooks, Mixins, client UI, or required client resources.
Removal plus restart restores BlueMap's stock path.

Same-dimension pixel-only resource-pack sheet overrides are supported. Model,
blockstate, metadata, dimensions, and the seven-path Minecraft host-model ABI
are not extensible. Additional Fusion predicates/layouts and appearance/camo
proxies fail closed.
