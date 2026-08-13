# SPDX-License-Identifier: MIT
"""Regression coverage for stable vanilla stair topology in the gallery."""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "rechiseled_gallery_generator", ROOT / "gallery/generate.py"
)
assert SPEC is not None and SPEC.loader is not None
gallery = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gallery
SPEC.loader.exec_module(gallery)

OFFSETS = {
    "north": (0, 0, -1),
    "east": (1, 0, 0),
    "south": (0, 0, 1),
    "west": (-1, 0, 0),
}
OPPOSITE = {"north": "south", "east": "west", "south": "north", "west": "east"}
COUNTER_CLOCKWISE = {"north": "west", "east": "north", "south": "east", "west": "south"}


def parse_block(value: str) -> tuple[str, dict[str, str]]:
    if "[" not in value:
        return value, {}
    block_id, raw = value[:-1].split("[", 1)
    return block_id, dict(field.split("=", 1) for field in raw.split(","))


def offset(position: gallery.Position, direction: str) -> gallery.Position:
    dx, dy, dz = OFFSETS[direction]
    return position.offset(dx, dy, dz)


def is_stair(value: tuple[str, dict[str, str]] | None) -> bool:
    return value is not None and value[0].endswith("_stairs_connecting")


def can_take_shape(
    own: tuple[str, dict[str, str]],
    position: gallery.Position,
    direction: str,
    world: dict[gallery.Position, tuple[str, dict[str, str]]],
) -> bool:
    neighbor = world.get(offset(position, direction))
    return not (
        is_stair(neighbor)
        and neighbor[1]["facing"] == own[1]["facing"]
        and neighbor[1]["half"] == own[1]["half"]
    )


def derived_shape(
    position: gallery.Position,
    world: dict[gallery.Position, tuple[str, dict[str, str]]],
) -> str:
    own = world[position]
    facing = own[1]["facing"]
    half = own[1]["half"]
    axis = "x" if facing in {"east", "west"} else "z"

    front = world.get(offset(position, facing))
    if is_stair(front):
        front_facing = front[1]["facing"]
        front_axis = "x" if front_facing in {"east", "west"} else "z"
        if (
            front[1]["half"] == half
            and front_axis != axis
            and can_take_shape(own, position, OPPOSITE[front_facing], world)
        ):
            return (
                "outer_left"
                if front_facing == COUNTER_CLOCKWISE[facing]
                else "outer_right"
            )

    back = world.get(offset(position, OPPOSITE[facing]))
    if is_stair(back):
        back_facing = back[1]["facing"]
        back_axis = "x" if back_facing in {"east", "west"} else "z"
        if (
            back[1]["half"] == half
            and back_axis != axis
            and can_take_shape(own, position, back_facing, world)
        ):
            return (
                "inner_left"
                if back_facing == COUNTER_CLOCKWISE[facing]
                else "inner_right"
            )
    return "straight"


class GalleryGeneratorTest(unittest.TestCase):
    def test_all_80_representative_target_states_have_stable_topology(self) -> None:
        fixtures = [
            fixture
            for fixture in gallery.structural_fixtures()
            if fixture.category == "stairs-state"
        ]
        self.assertEqual(80, len(fixtures))
        expected = set(itertools.product(
            ("east", "north", "south", "west"),
            ("bottom", "top"),
            ("inner_left", "inner_right", "outer_left", "outer_right", "straight"),
            ("false", "true"),
        ))
        actual: set[tuple[str, str, str, str]] = set()
        non_straight_targets = 0
        for fixture in fixtures:
            world = {
                placement.position: parse_block(placement.block)
                for placement in fixture.placements
            }
            target = next(
                placement
                for placement in fixture.placements
                if placement.position == fixture.anchor
            )
            properties = parse_block(target.block)[1]
            state = tuple(properties[key] for key in (
                "facing", "half", "shape", "waterlogged"
            ))
            actual.add(state)
            self.assertEqual(properties["shape"], derived_shape(target.position, world))
            if properties["shape"] == "straight":
                self.assertEqual(1, len(fixture.placements))
            else:
                non_straight_targets += 1
                self.assertEqual(2, len(fixture.placements))
                support = fixture.placements[0]
                self.assertNotEqual(target.position, support.position)
                self.assertEqual("straight", parse_block(support.block)[1]["shape"])
                self.assertLess(
                    fixture.placements.index(support), fixture.placements.index(target)
                )
                self.assertEqual("straight", derived_shape(support.position, world))
        self.assertEqual(expected, actual)
        self.assertEqual(64, non_straight_targets)

    def test_every_structural_stair_placement_matches_vanilla_neighbor_shape(self) -> None:
        fixtures = gallery.structural_fixtures()
        world = {
            placement.position: parse_block(placement.block)
            for fixture in fixtures
            for placement in fixture.placements
        }
        self.assertEqual(
            sum(len(fixture.placements) for fixture in fixtures), len(world)
        )
        non_straight_targets = 0
        ordered_supports = 0
        for fixture in fixtures:
            for placement in fixture.placements:
                block = world[placement.position]
                if not is_stair(block):
                    continue
                self.assertEqual(
                    block[1]["shape"],
                    derived_shape(placement.position, world),
                    fixture.case_id,
                )
                if block[1]["shape"] != "straight":
                    non_straight_targets += 1
                    required = (
                        offset(placement.position, block[1]["facing"])
                        if block[1]["shape"].startswith("outer_")
                        else offset(placement.position, OPPOSITE[block[1]["facing"]])
                    )
                    support_index = next(
                        index
                        for index, candidate in enumerate(fixture.placements)
                        if candidate.position == required
                    )
                    target_index = fixture.placements.index(placement)
                    self.assertLess(support_index, target_index, fixture.case_id)
                    ordered_supports += 1
        self.assertEqual(68, non_straight_targets)
        self.assertEqual(68, ordered_supports)

    def test_generated_counts_and_expectations_include_every_support(self) -> None:
        files, cases, placements = gallery.rendered_files()
        self.assertEqual(1_924, cases)
        self.assertEqual(2_271, placements)
        payload = json.loads(files[Path("cases.json")])
        self.assertEqual(2_271, payload["verified_placement_count"])
        self.assertEqual(
            2_271 - 1_743 - 2,
            sum(len(case["placements"]) for case in payload["structural_cases"]),
        )
        verify = files[
            Path("datapack/data/rechiseled_gallery/function/verify.mcfunction")
        ].decode("utf-8")
        self.assertIn("score #checked rechiseled_gallery matches 2271", verify)


if __name__ == "__main__":
    unittest.main()
