# Compatibility

The only supported activation tuple is:

- All the Mons 1.2.0, pack commit
  `c7bb230f21d14d26859d0b92548f089b3a493ad9`;
- Minecraft 1.21.1 and NeoForge 21.1.248;
- Java 21;
- BlueMap upstream 5.22 commit
  `fe5115d5548a30d34175b8e0449aaca280af199f` or the audited Java-21 backport
  `5.22-agent.backport-5.22-mc1.21.1-2` commit
  `9be321df995a1103808621d529eb72773e719d4d`;
- exact Rechiseled 1.2.5 and Fusion 1.3.12 artifacts from README;
- BlueMap Fusion Resource Models `0.1.0-alpha.1`, commit
  `3ddd5d39bb7cc8664c242aedd849a636316075c2`, source tree
  `6e85031ff2f0e7417a7a2fb0babbf7ed5a4f218a`.

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
