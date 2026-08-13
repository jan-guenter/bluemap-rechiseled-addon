#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Generate the bounded exhaustive Rechiseled 1.2.5 staging gallery."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
DEFINITIONS = (
    REPOSITORY
    / "src/main/resources/bluemap-rechiseled/profiles/rechiseled/"
    / "1.2.5-fusion-1.3.12/definitions.tsv"
)
SWATCH_ORIGIN = (-180, 100, -180)
SWATCH_COLUMNS = 42
STRUCTURAL_ORIGIN = (10, 100, -180)
STRUCTURAL_COLUMNS = 20
CELL_SIZE = 6


@dataclass(frozen=True, order=True)
class Position:
    x: int
    y: int
    z: int

    def offset(self, dx: int = 0, dy: int = 0, dz: int = 0) -> "Position":
        return Position(self.x + dx, self.y + dy, self.z + dz)

    def command(self) -> str:
        return f"{self.x} {self.y} {self.z}"


@dataclass(frozen=True)
class Placement:
    position: Position
    block: str


@dataclass(frozen=True)
class Fixture:
    case_id: str
    category: str
    anchor: Position
    placements: tuple[Placement, ...]
    notes: str


def definitions() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in DEFINITIONS.read_text(encoding="ascii").splitlines():
        fields = line.split("\t")
        if len(fields) != 5:
            raise ValueError("malformed exact definitions catalog")
        rows.append((fields[0], fields[1]))
    families = {
        family: sum(item[1] == family for item in rows)
        for family in {item[1] for item in rows}
    }
    expected = {"full": 569, "axis": 12, "slab": 581, "stairs": 581}
    if len(rows) != 1_743 or len({row[0] for row in rows}) != 1_743:
        raise ValueError("exact routed block census changed")
    if families != expected:
        raise ValueError(f"exact routed shape census changed: {families}")
    return rows


def swatches(rows: list[tuple[str, str]]) -> list[Placement]:
    x0, y, z0 = SWATCH_ORIGIN
    return [
        Placement(
            Position(
                x0 + 3 * (index % SWATCH_COLUMNS),
                y,
                z0 + 3 * (index // SWATCH_COLUMNS),
            ),
            block,
        )
        for index, (block, _shape) in enumerate(rows)
    ]


def structural_fixtures() -> list[Fixture]:
    fixtures: list[Fixture] = []

    def anchor(index: int) -> Position:
        x0, y, z0 = STRUCTURAL_ORIGIN
        return Position(
            x0 + CELL_SIZE * (index % STRUCTURAL_COLUMNS),
            y,
            z0 + CELL_SIZE * (index // STRUCTURAL_COLUMNS),
        )

    def add(
        case_id: str,
        category: str,
        blocks: list[tuple[int, int, int, str]],
        notes: str,
    ) -> None:
        center = anchor(len(fixtures))
        placements = tuple(
            Placement(center.offset(dx, dy, dz), block)
            for dx, dy, dz, block in blocks
        )
        fixtures.append(Fixture(case_id, category, center, placements, notes))

    # On an UP face: T=-Z, TR=+X-Z, R=+X, BR=+X+Z,
    # B=+Z, BL=-X+Z, L=-X, TL=-X-Z.
    offsets = (
        (0, 0, -1), (1, 0, -1), (1, 0, 0), (1, 0, 1),
        (0, 0, 1), (-1, 0, 1), (-1, 0, 0), (-1, 0, -1),
    )
    masks = (
        ("none", 0x00), ("top", 0x01), ("right", 0x04),
        ("bottom", 0x10), ("left", 0x40), ("top-right", 0x05),
        ("top-bottom", 0x11), ("left-right", 0x44),
        ("cardinals", 0x55), ("one-diagonal", 0x57),
        ("mask-dd", 0xDD), ("full-edge47", 0x7F),
        ("full-edge46", 0xFD), ("all", 0xFF),
    )
    layout_blocks = (
        ("pieced", "rechiseled:acacia_planks_beams_connecting"),
        ("full", "rechiseled:acacia_planks_brick_pattern_connecting"),
        ("horizontal", "rechiseled:acacia_planks_bricks_connecting"),
        ("vertical", "rechiseled:obsidian_pillars_connecting"),
        (
            "simple",
            "rechiseled:amethyst_block_pillar_connecting[axis=y]",
        ),
    )
    for layout, block in layout_blocks:
        for label, mask in masks:
            case_block = (
                "rechiseled:purpur_brick_pattern_connecting"
                if layout == "full" and label == "mask-dd"
                else block
            )
            placements = [(0, 0, 0, case_block)]
            placements.extend(
                (*offsets[bit], case_block)
                for bit in range(8)
                if mask & (1 << bit)
            )
            add(
                f"layout-{layout}-"
                f"{'purpur-tile40' if layout == 'full' and label == 'mask-dd' else label}",
                "layout-mask",
                placements,
                f"{layout} top-face mask 0x{mask:02x}",
            )

    add(
        "layout-plain-axis-end",
        "layout-mask",
        [(0, 0, 0, "rechiseled:blue_ice_pillar_connecting[axis=y]")],
        "plain end texture; no connected-sheet selection",
    )

    slab = "rechiseled:acacia_planks_beams_slab_connecting"
    for slab_type in ("bottom", "double", "top"):
        for waterlogged in ("false", "true"):
            state = f"{slab}[type={slab_type},waterlogged={waterlogged}]"
            add(
                f"slab-{slab_type}-waterlogged-{waterlogged}",
                "slab-state",
                [(0, 0, 0, state)],
                "exact slab topology and persisted waterlogged state",
            )

    for slab_type in ("bottom", "top"):
        state = f"{slab}[type={slab_type},waterlogged=false]"
        add(
            f"pieced-slab-{slab_type}-connected",
            "pieced-partial",
            [(0, 0, 0, state), (1, 0, 0, state)],
            "connected partial side UV crosses the global PIECED seam",
        )

    stairs = "rechiseled:acacia_planks_beams_stairs_connecting"
    for facing in ("east", "north", "south", "west"):
        for half in ("bottom", "top"):
            for shape in (
                "inner_left", "inner_right", "outer_left", "outer_right", "straight"
            ):
                for waterlogged in ("false", "true"):
                    state = (
                        f"{stairs}[facing={facing},half={half},shape={shape},"
                        f"waterlogged={waterlogged}]"
                    )
                    add(
                        f"stairs-{facing}-{half}-{shape}-waterlogged-{waterlogged}",
                        "stairs-state",
                        [(0, 0, 0, state)],
                        "all 80 legal topology/rotation/half/waterlogged states",
                    )

    pieced_stair = (
        f"{stairs}[facing=east,half=bottom,shape=inner_left,waterlogged=false]"
    )
    add(
        "pieced-stair-connected",
        "pieced-partial",
        [(0, 0, 0, pieced_stair), (1, 0, 0, pieced_stair)],
        "connected stair partial UV and inner topology take PIECED split path",
    )

    axis_ids = [
        "rechiseled:amethyst_block_pillar_connecting",
        "rechiseled:blue_ice_pillar_connecting",
        "rechiseled:bone_block_connecting_connecting",
        "rechiseled:bone_block_pillar_connecting",
        "rechiseled:coal_block_pillar_connecting",
        "rechiseled:cobbled_deepslate_pillar_connecting",
        "rechiseled:cobblestone_pillar_connecting",
        "rechiseled:copper_block_pillar_connecting",
        "rechiseled:emerald_block_pillar_connecting",
        "rechiseled:lapis_block_pillar_connecting",
        "rechiseled:netherite_block_pillar_connecting",
        "rechiseled:redstone_block_pillar_connecting",
    ]
    for block in axis_ids:
        label = block.split(":", 1)[1]
        add(
            f"axis-{label}",
            "axis-state",
            [
                (-2, 0, 0, f"{block}[axis=x]"),
                (0, 0, 0, f"{block}[axis=y]"),
                (2, 0, 0, f"{block}[axis=z]"),
            ],
            "all x/y/z pillar transforms and per-face mixed layouts",
        )

    pillar = "rechiseled:amethyst_block_pillar_connecting"
    add(
        "axis-x-same-state-continuity",
        "axis-connection",
        [(0, 0, 0, f"{pillar}[axis=x]"), (1, 0, 0, f"{pillar}[axis=x]")],
        "horizontal child is_same_state x-to-x continuity",
    )
    add(
        "axis-z-same-state-continuity",
        "axis-connection",
        [(0, 0, 0, f"{pillar}[axis=z]"), (0, 0, 1, f"{pillar}[axis=z]")],
        "horizontal child is_same_state z-to-z continuity",
    )
    add(
        "axis-state-mismatch",
        "axis-connection",
        [
            (-1, 0, 0, f"{pillar}[axis=x]"),
            (0, 0, 0, f"{pillar}[axis=y]"),
            (1, 0, 0, f"{pillar}[axis=z]"),
        ],
        "x/y/z are deliberately not the same persisted state",
    )
    add(
        "axis-y-shape-interconnection",
        "axis-connection",
        [
            (0, 0, 0, f"{pillar}[axis=y]"),
            (1, 0, 0, "rechiseled:amethyst_block_pillar_slab_connecting"
             "[type=bottom,waterlogged=false]"),
            (0, 0, 1, "rechiseled:amethyst_block_pillar_stairs_connecting"
             "[facing=east,half=bottom,shape=straight,waterlogged=false]"),
        ],
        "axis=y base predicate interconnects matching slab and stair family",
    )

    add(
        "glowstone-full-connected",
        "glowstone",
        [
            (dx, 0, dz, "rechiseled:glowstone_bricks_connecting")
            for dz in (-1, 0, 1)
            for dx in (-1, 0, 1)
        ],
        "ordinary installed block light; no invented emissive material",
    )
    add(
        "glowstone-slab-connected",
        "glowstone",
        [
            (dx, 0, 0, "rechiseled:glowstone_bricks_slab_connecting"
             "[type=bottom,waterlogged=false]")
            for dx in (-1, 0, 1)
        ],
        "connected glowstone slab geometry and ordinary element light",
    )
    add(
        "glowstone-stair-connected",
        "glowstone",
        [
            (0, 0, 0, "rechiseled:glowstone_bricks_stairs_connecting"
             "[facing=east,half=bottom,shape=inner_left,waterlogged=false]"),
            (1, 0, 0, "rechiseled:glowstone_bricks_stairs_connecting"
             "[facing=east,half=bottom,shape=outer_right,waterlogged=false]"),
        ],
        "connected glowstone stair silhouettes and ordinary element light",
    )

    occupied: set[Position] = set()
    for fixture in fixtures:
        for placement in fixture.placements:
            if placement.position in occupied:
                raise AssertionError(f"structural fixture overlap at {placement.position}")
            occupied.add(placement.position)
    return fixtures


def controls() -> list[Placement]:
    return [
        Placement(Position(148, 100, -55), "rechiseled:acacia_planks_beams"),
        Placement(Position(154, 100, -55), "minecraft:stone"),
    ]


def swatches_tsv(rows: list[tuple[str, str]], blocks: list[Placement]) -> str:
    lines = ["index\tblock_id\tshape_family\tx\ty\tz"]
    for index, ((block_id, family), placement) in enumerate(
        zip(rows, blocks, strict=True)
    ):
        position = placement.position
        lines.append(
            f"{index}\t{block_id}\t{family}\t{position.x}\t{position.y}\t{position.z}"
        )
    return "\n".join(lines) + "\n"


def cases_tsv(fixtures: list[Fixture], stock: list[Placement]) -> str:
    lines = ["case_id\tcategory\tx\ty\tz\tplacements\tnotes"]
    for fixture in fixtures:
        lines.append(
            f"{fixture.case_id}\t{fixture.category}\t{fixture.anchor.x}\t"
            f"{fixture.anchor.y}\t{fixture.anchor.z}\t{len(fixture.placements)}\t"
            f"{fixture.notes}"
        )
    for index, control in enumerate(stock):
        position = control.position
        lines.append(
            f"stock-{index}\tstock\t{position.x}\t{position.y}\t{position.z}\t1\t"
            f"untouched stock renderer control: {control.block}"
        )
    return "\n".join(lines) + "\n"


def all_placements(
    isolated: list[Placement], fixtures: list[Fixture], stock: list[Placement]
) -> list[Placement]:
    result = list(isolated)
    result.extend(item for fixture in fixtures for item in fixture.placements)
    result.extend(stock)
    positions = [placement.position for placement in result]
    if len(positions) != len(set(positions)):
        raise AssertionError("gallery sections overlap")
    return result


def region_commands(command: str, y1: int, y2: int, block: str) -> list[str]:
    lines: list[str] = []
    for x in range(-192, 161, 32):
        for z in range(-192, -47, 32):
            x2 = min(x + 31, 160)
            z2 = min(z + 31, -48)
            lines.append(f"{command} {x} {y1} {z} {x2} {y2} {z2} {block}")
    return lines


def build_function(
    isolated: list[Placement], fixtures: list[Fixture], stock: list[Placement]
) -> str:
    lines = [
        "# Generated by gallery/generate.py; do not edit.",
        "function rechiseled_gallery:clear",
        *region_commands("fill", 99, 99, "minecraft:stone"),
        "scoreboard players set #swatches rechiseled_gallery 0",
        "scoreboard players set #structures rechiseled_gallery 0",
        "scoreboard players set #controls rechiseled_gallery 0",
    ]
    for placement in isolated:
        lines.append(f"setblock {placement.position.command()} {placement.block}")
        lines.append("scoreboard players add #swatches rechiseled_gallery 1")
    for fixture in fixtures:
        for placement in fixture.placements:
            lines.append(f"setblock {placement.position.command()} {placement.block}")
        lines.append("scoreboard players add #structures rechiseled_gallery 1")
    for placement in stock:
        lines.append(f"setblock {placement.position.command()} {placement.block}")
        lines.append("scoreboard players add #controls rechiseled_gallery 1")
    lines.extend((
        "function rechiseled_gallery:verify",
        "tellraw @a [{\"text\":\"Rechiseled gallery: \"},"
        "{\"score\":{\"name\":\"#checked\",\"objective\":\"rechiseled_gallery\"}},"
        "{\"text\":\" checked placements, \"},"
        "{\"score\":{\"name\":\"#failures\",\"objective\":\"rechiseled_gallery\"}},"
        "{\"text\":\" failures\"}]",
    ))
    return "\n".join(lines) + "\n"


def verify_function(
    isolated: list[Placement], fixtures: list[Fixture], stock: list[Placement]
) -> str:
    placements = all_placements(isolated, fixtures, stock)
    lines = [
        "# Generated by gallery/generate.py; do not edit.",
        "scoreboard players set #failures rechiseled_gallery 0",
        "scoreboard players set #checked rechiseled_gallery 0",
    ]
    for placement in placements:
        lines.append(
            f"execute unless block {placement.position.command()} {placement.block} run "
            "scoreboard players add #failures rechiseled_gallery 1"
        )
        lines.append("scoreboard players add #checked rechiseled_gallery 1")
    expected = (
        ("#checked", len(placements)),
        ("#swatches", len(isolated)),
        ("#structures", len(fixtures)),
        ("#controls", len(stock)),
    )
    for score, value in expected:
        lines.append(
            f"execute unless score {score} rechiseled_gallery matches {value} run "
            "scoreboard players add #failures rechiseled_gallery 1"
        )
    return "\n".join(lines) + "\n"


def rendered_files() -> tuple[dict[Path, bytes], int, int]:
    rows = definitions()
    isolated = swatches(rows)
    fixtures = structural_fixtures()
    stock = controls()
    placements = all_placements(isolated, fixtures, stock)
    logical_cases = len(isolated) + len(fixtures) + len(stock)
    files: dict[Path, bytes] = {
        Path("swatches.tsv"): swatches_tsv(rows, isolated).encode("utf-8"),
        Path("cases.tsv"): cases_tsv(fixtures, stock).encode("utf-8"),
        Path("cases.json"): (json.dumps({
            "schema_version": 1,
            "baseline": {
                "pack": "All the Mons 1.2.0",
                "minecraft": "1.21.1",
                "rechiseled": "1.2.5",
                "fusion": "1.3.12",
            },
            "routed_swatch_count": len(isolated),
            "structural_case_count": len(fixtures),
            "stock_control_count": len(stock),
            "logical_case_count": logical_cases,
            "verified_placement_count": len(placements),
            "coverage": {
                "layouts": ["plain", "pieced", "full", "horizontal", "vertical", "simple"],
                "full_tile_41": "unreachable by exhaustive 256-mask selector test",
                "full_padding_rows": "excluded by logical 8x6 crop",
                "negative_coordinates": True,
                "stair_legal_states_for_representative": 80,
                "axis_ids_x_y_z": 12,
                "glowstone_routed_ids_in_isolated_census": 27,
            },
            "structural_cases": [
                {
                    "case_id": fixture.case_id,
                    "category": fixture.category,
                    "anchor": fixture.anchor.__dict__,
                    "notes": fixture.notes,
                    "placements": [
                        {
                            "x": item.position.x,
                            "y": item.position.y,
                            "z": item.position.z,
                            "block": item.block,
                            "expected_route": "custom",
                        }
                        for item in fixture.placements
                    ],
                }
                for fixture in fixtures
            ],
            "stock_controls": [
                {
                    "x": item.position.x,
                    "y": item.position.y,
                    "z": item.position.z,
                    "block": item.block,
                    "expected_route": "stock-control",
                }
                for item in stock
            ],
        }, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        Path("datapack/pack.mcmeta"): (json.dumps({
            "pack": {
                "description": "ATM 1.2.0 Rechiseled 1.2.5 BlueMap review gallery",
                "pack_format": 48,
            }
        }, indent=2) + "\n").encode("utf-8"),
        Path("datapack/data/minecraft/tags/function/load.json"): (
            json.dumps({"values": ["rechiseled_gallery:load"]}, indent=2) + "\n"
        ).encode("utf-8"),
        Path("datapack/data/rechiseled_gallery/function/load.mcfunction"): (
            "# Generated by gallery/generate.py; do not edit.\n"
            "scoreboard objectives add rechiseled_gallery dummy\n"
            "forceload add -192 -192 160 -48\n"
        ).encode("utf-8"),
        Path("datapack/data/rechiseled_gallery/function/build.mcfunction"):
            build_function(isolated, fixtures, stock).encode("utf-8"),
        Path("datapack/data/rechiseled_gallery/function/verify.mcfunction"):
            verify_function(isolated, fixtures, stock).encode("utf-8"),
        Path("datapack/data/rechiseled_gallery/function/clear.mcfunction"): (
            "# Generated by gallery/generate.py; do not edit.\n"
            + "\n".join(region_commands("fill", 99, 104, "minecraft:air"))
            + "\n"
        ).encode("utf-8"),
        Path("datapack/data/rechiseled_gallery/function/pose.mcfunction"): (
            "# Generated by gallery/generate.py; do not edit.\n"
            "tp @s -14.5 150 -112.5 180 45\n"
        ).encode("utf-8"),
        Path("datapack/data/rechiseled_gallery/function/release.mcfunction"): (
            "# Generated by gallery/generate.py; do not edit.\n"
            "forceload remove -192 -192 160 -48\n"
        ).encode("utf-8"),
    }
    checksums = [
        f"{hashlib.sha256(content).hexdigest()}  {path.as_posix()}"
        for path, content in sorted(files.items(), key=lambda item: item[0].as_posix())
    ]
    files[Path("SHA256SUMS")] = ("\n".join(checksums) + "\n").encode("ascii")
    return files, logical_cases, len(placements)


def write_or_check(files: dict[Path, bytes], check: bool) -> int:
    differences: list[str] = []
    for relative, expected in files.items():
        path = ROOT / relative
        if check:
            if not path.is_file() or path.read_bytes() != expected:
                differences.append(relative.as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected)
    if differences:
        print("generated gallery differs: " + ", ".join(differences), file=sys.stderr)
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    files, cases, placements = rendered_files()
    result = write_or_check(files, args.check)
    if result == 0 and not args.check:
        print(f"generated {cases}-case / {placements}-placement Rechiseled gallery")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
