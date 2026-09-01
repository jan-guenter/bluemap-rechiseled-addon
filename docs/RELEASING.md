# Releasing

Version `0.1.0-alpha.2` is immutable and published. The current
`0.1.0-alpha.3` source is the owner-accepted BlueMap 5.23 migration candidate.
Its four artifact identities are sealed from authoritative pull-request CI run
`33528747904`. The reviewed integration JAR and release JAR have identical
entry payloads and order. Their only archive difference is the UTF-8-name flag
recorded in `docs/STAGING.md` and `provenance/release.json`.

Initialize all exact source checkouts before any gate:

```bash
git submodule update --init --recursive -- \
  tooling/bluemap-addon-toolkit \
  modules/bluemap-addon-adapter-api \
  modules/bluemap-fusion-resource-models
```

The settings preflight must accept all gitlinks and reject a changed adapter or
Fusion module HEAD, index, worktree, or `src/main/java` tree.

This repository's local policy forbids JAR and publication-metadata tasks.
Authoritative pull-request CI produced the production JAR, sources JAR, POM,
and Gradle module payloads recorded in `provenance/release.json`; final
pull-request CI and the combined runtime gate must reproduce and exercise them
before release. The release
workflow rejects provenance whose status is not `owner-accepted-release-candidate`.

Release only from a clean, independently reviewed commit merged through a pull
request. A release tag must equal `v<addon_version>` and be an annotated,
immutable tag whose commit is on `main`. Version increases also require a PR.

## Pre-tag checklist

- exact dual artifacts and generated profile/gallery checks pass;
- authoritative CI clean build, tests, Checkstyle, production/sources JAR
  boundaries, POM, and artifact verifier are green;
- runtime and owner visual acceptance are recorded for the exact packaged
  entry payloads, with any whole-archive metadata difference fully accounted
  for;
- status, diff, version, commit, tag target, remote, JAR contents, coordinates,
  and release notes are reviewed;
- docs/provenance contain no future, inherited, or unobserved claim.

## Workflow

`.github/workflows/release.yml` validates the immutable tag, rebuilds once,
preflights the exact GitHub Packages version, creates/resumes a draft GitHub
Release, publishes Maven only when absent, verifies remote bytes and checksum
sidecars, creates a build-provenance attestation, and finally publishes the
release. A published complete version is verified without mutation. A partial
or mismatched Maven version fails closed.

The workflow is resumable through `workflow_dispatch` with the same immutable
tag. Never delete/recreate a published tag/version or use `--clobber` against a
published release.

## Coordinates

- GitHub repository: `jan-guenter/bluemap-rechiseled-addon`
- Maven: `io.github.jan-guenter:bluemap-rechiseled-addon:<version>`
- Assets: `bluemap-rechiseled-addon-<version>.jar`, sources JAR, POM, Gradle
  module metadata, and `SHA256SUMS`.
