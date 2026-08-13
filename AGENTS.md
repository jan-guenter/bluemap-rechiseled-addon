# Agent guide

This is the standalone public repository for the exact Rechiseled 1.2.5 plus
Fusion 1.3.12 BlueMap add-on. Read the workspace and portfolio agent guides,
this README, `docs/ARCHITECTURE.md`, `docs/PROVENANCE.md`, and
`docs/RELEASING.md` before changing it.

## Boundaries

- Java 21, BlueMap 5.22 backport commit
  `9be321df995a1103808621d529eb72773e719d4d`, Minecraft 1.21.1.
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
