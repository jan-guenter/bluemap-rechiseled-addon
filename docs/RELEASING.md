# Releasing

Version `0.1.0-alpha.2` is immutable and published. The current
`0.1.0-alpha.3` source is an unpublished BlueMap 5.23 migration candidate. Its
artifact identities remain `PENDING`. Do not tag or publish it until aggregate
integration review is accepted and `provenance/release.json` is sealed.

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
Authoritative pull-request CI produces the production JAR, sources JAR, POM,
and Gradle module payloads. A reviewed follow-up records all four exact
identities in `provenance/release.json`; final pull-request CI and the combined
runtime gate must reproduce and exercise them before release. The release
workflow rejects provenance whose status is not `owner-accepted-release-candidate`.

Release only from a clean, independently reviewed commit merged through a pull
request. A release tag must equal `v<addon_version>` and be an annotated,
immutable tag whose commit is on `main`. Version increases also require a PR.

## Pre-tag checklist

- exact dual artifacts and generated profile/gallery checks pass;
- authoritative CI clean build, tests, Checkstyle, production/sources JAR
  boundaries, POM, and artifact verifier are green;
- runtime/gallery/restart/browser and owner visual acceptance are recorded for
  the exact CI JAR;
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
