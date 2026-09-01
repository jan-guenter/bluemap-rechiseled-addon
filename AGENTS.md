# Agent guide

This is the standalone public repository for the exact Rechiseled 1.2.5 plus
Fusion 1.3.12 BlueMap add-on. Read the workspace and portfolio agent guides,
this README, `docs/ARCHITECTURE.md`, `docs/PROVENANCE.md`, and
`docs/RELEASING.md` before changing it.

## Boundaries

- Java 21, BlueMap 5.23 feature-backport commit
  `7e07f4e74ec1e92a6ead9aa1e66054af3e133aac`, API commit
  `285c9a60eff3ac2b0cab308ce1058d1565be0971`, Minecraft 1.21.1.
- Source-bundle BlueMap Add-on Adapter API `0.1.0-alpha.2` only from commit
  `e81f08bc4bfbf02d810ec8949a019130e2e61634`, source tree
  `2f974c9bb2ba13888d69682f86f30f58922d30eb`.
- Source-bundle BlueMap Fusion Resource Models `0.1.0-alpha.1` only from
  commit `3ddd5d39bb7cc8664c242aedd849a636316075c2`, source tree
  `6e85031ff2f0e7417a7a2fb0babbf7ed5a4f218a`.
- Own only the generated 1,743-row `rechiseled:*_connecting` allowlist.
- Never register `fusion:*`, depend on another mod for activation, or add a
  RechiseledCreate bridge here.
- Bundle no Rechiseled/Fusion code, classes, JSON, PNG, metadata, or JARs.
- Both exact artifacts are All rights reserved. Use installed resources and
  independently authored behavior only.
- Preserve stock rendering outside the exact route and atomically fall back on
  per-block failure. Propagate BlueMap capacity failures.
- Preserve pixel-only sheet overrides with exact dimensions; structural JSON
  and metadata remain exact.
- Keep add-on IDs under `bluemap_rechiseled`, Java under
  `io.github.janguenter.bluemap.rechiseled`, extension ID
  `bluemap_rechiseled:exact_profile`, and renderer/dispatch ID
  `bluemap_rechiseled:fusion_model`.
- Do not change orchestration files, cluster state, remotes, tags, releases, or
  production systems from this repository task.
- Keep local profile parsing, predicates, catalogs, routes, fallback, and
  emission policy outside the shared Fusion model package.
- Keep entrypoint, runtime state, renderer, and failure policy outside the
  shared adapter package.

## Generated inputs

Run `tools/generate_profile.py` only with the two exact artifacts documented in
README. Generated profile and gallery files must be reproducible and checked
in. Never hand-edit generated TSV/JSON/function/checksum outputs.

## Validation cadence

Implement a coherent tranche before validating. At the end, run one focused
profile/gallery/Python/Java/checkstyle compile-test gate from README. Do not run
`clean`, full `check build`, publication, or JAR packaging tasks locally; PR CI
is authoritative. Before a commit, freeze the tree and obtain an independent
read-only audit. Record only observed results.

Before presenting a BlueMap link, open that exact link in the agent browser and
perform the workspace-required lightweight visual sanity check.
