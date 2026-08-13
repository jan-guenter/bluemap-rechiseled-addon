# SPDX-License-Identifier: MIT
"""Unit coverage for deterministic fail-closed profile generation."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "generate_profile", ROOT / "tools/generate_profile.py"
)
assert SPEC is not None and SPEC.loader is not None
generate_profile = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generate_profile)


class ProfileHelpersTest(unittest.TestCase):
    def test_roster_digest_is_sorted_and_newline_terminated(self) -> None:
        self.assertEqual(
            generate_profile.roster_digest(["z", "a"]),
            generate_profile.digest_bytes(b"a\nz\n"),
        )

    def test_resource_path_rejects_parent_escape(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsafe resource key"):
            generate_profile.resource_path("rechiseled:../escape", "models", ".json")

    def test_identity_gate_rejects_wrong_filename_before_hashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wrong.jar"
            path.write_bytes(b"")
            with self.assertRaisesRegex(ValueError, "unexpected artifact path"):
                generate_profile._verify_identity(  # noqa: SLF001 - exact helper test
                    path,
                    filename="expected.jar",
                    size=0,
                    sha1="",
                    sha256="",
                    sha512="",
                )

    def test_canonical_json_is_order_independent(self) -> None:
        self.assertEqual(
            generate_profile.canonical_json({"b": 2, "a": 1}),
            b'{\n  "a": 1,\n  "b": 2\n}\n',
        )

    def test_full_profile_constants_lock_exact_closure(self) -> None:
        self.assertEqual(1_743, generate_profile.ROUTED_COUNT)
        self.assertEqual(50_571, generate_profile.ROUTED_STATE_COUNT)
        self.assertEqual(5_825, generate_profile.MODEL_COUNT)
        self.assertEqual(8_751, generate_profile.RESOURCE_COUNT)
        self.assertEqual(7, generate_profile.HOST_MODEL_COUNT)
        host_rows = "".join(
            f"model\t{path}\t{size}\t{sha256}\n"
            for path, size, sha256 in generate_profile.HOST_MODELS
        ).encode("ascii")
        self.assertEqual(
            "99575da08068de74de57bdd47281195b58c679966ea68ebea89597dd3c2b83fb",
            generate_profile.digest_bytes(host_rows),
        )
        self.assertEqual(
            "8ebc0ffb63cd675afa5aa3d0f8bb90e3861b3286efb42950bee0a38a812609d3",
            generate_profile.PATH_CLOSURE_DIGEST,
        )


if __name__ == "__main__":
    unittest.main()
