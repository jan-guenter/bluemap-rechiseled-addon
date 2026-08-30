# SPDX-License-Identifier: MIT
"""Static release-boundary regression coverage."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class ReleaseContractTest(unittest.TestCase):
    def test_alpha2_candidate_locks_module_and_all_publication_payloads(self) -> None:
        release = json.loads((ROOT / "provenance/release.json").read_text())
        self.assertEqual("owner-accepted-release-candidate", release["status"])
        self.assertEqual("0.1.0-alpha.2", release["version"])
        self.assertEqual("v0.1.0-alpha.2", release["tag"])
        self.assertEqual(
            {
                "production_jar": {
                    "file_name": "bluemap-rechiseled-addon-0.1.0-alpha.2.jar",
                    "size": 647_540,
                    "sha256": "083425a0bbaf7e4c99673fb169b63e452af9aea2621a4831664680a544f9695a",
                },
                "sources_jar": {
                    "file_name": "bluemap-rechiseled-addon-0.1.0-alpha.2-sources.jar",
                    "size": 581_629,
                    "sha256": "09687fd9c0f4f3c30d6eb98eb312a0a5c233b3fb0e34f91f527e01d6955461d7",
                },
                "pom": {
                    "file_name": "bluemap-rechiseled-addon-0.1.0-alpha.2.pom",
                    "size": 1_359,
                    "sha256": "2866efd132e69c2547031f6fc5a82a7ebf58f550fe090b8efd3139f0136a2e79",
                },
                "gradle_module": {
                    "file_name": "bluemap-rechiseled-addon-0.1.0-alpha.2.module.json",
                    "size": 2_841,
                    "sha256": "14870408c317c5c2b205cd71d466ab0cb3b61995cea2fe94aa072d52707fea35",
                },
            },
            release["final_release_artifacts"],
        )
        migration = release["fusion_model_migration"]
        self.assertEqual(
            "3ddd5d39bb7cc8664c242aedd849a636316075c2",
            migration["module_commit"],
        )
        self.assertEqual(
            "6e85031ff2f0e7417a7a2fb0babbf7ed5a4f218a",
            migration["module_source_tree"],
        )
        self.assertFalse(migration["renderer_or_gallery_behavior_change"])


if __name__ == "__main__":
    unittest.main()
