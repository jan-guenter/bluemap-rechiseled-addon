# ADR 0001: keep the Fusion interpreter repository-local

- Status: accepted for the first tranche
- Date: 2026-08-13

## Decision

The bounded Fusion model/predicate/orientation/sheet interpreter stays inside
this standalone Rechiseled add-on for its first release. It owns no block IDs
outside the exact generated `rechiseled:*` allowlist.

## Rationale

This is the first exact Fusion-format consumer in the portfolio. Extracting a
shared library before two independently accepted consumers exist would freeze
an unproven API and couple releases. Repository-local code also makes the ARR
resource boundary and production JAR audit unambiguous.

## Consequences

RechiseledCreate remains a future bridge. If another add-on needs the same
bounded interpreter, compare accepted implementations and extract only stable
MIT-owned contracts through a separate reviewed release.
