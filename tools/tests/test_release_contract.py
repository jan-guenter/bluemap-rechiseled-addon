# SPDX-License-Identifier: MIT
"""Static release-boundary regression coverage."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class ReleaseContractTest(unittest.TestCase):
    def test_alpha3_candidate_is_unpublished_and_preserves_alpha2(self) -> None:
        release = json.loads((ROOT / "provenance/release.json").read_text())
        self.assertEqual("unpublished-migration-candidate", release["status"])
        self.assertFalse(release["published"])
        self.assertEqual("0.1.0-alpha.3", release["version"])
        self.assertEqual("v0.1.0-alpha.3", release["tag"])
        self.assertEqual(
            {
                "production_jar": {
                    "file_name": "bluemap-rechiseled-addon-0.1.0-alpha.3.jar",
                    "size": None,
                    "sha256": "PENDING",
                },
                "sources_jar": {
                    "file_name": "bluemap-rechiseled-addon-0.1.0-alpha.3-sources.jar",
                    "size": None,
                    "sha256": "PENDING",
                },
                "pom": {
                    "file_name": "bluemap-rechiseled-addon-0.1.0-alpha.3.pom",
                    "size": None,
                    "sha256": "PENDING",
                },
                "gradle_module": {
                    "file_name": "bluemap-rechiseled-addon-0.1.0-alpha.3.module.json",
                    "size": None,
                    "sha256": "PENDING",
                },
            },
            release["candidate_artifacts"],
        )
        baseline = release["baseline_release"]
        self.assertEqual("0.1.0-alpha.2", baseline["version"])
        self.assertEqual(
            "083425a0bbaf7e4c99673fb169b63e452af9aea2621a4831664680a544f9695a",
            baseline["production_jar_sha256"],
        )
        adapter = release["adapter_api_migration"]
        self.assertEqual(
            "e81f08bc4bfbf02d810ec8949a019130e2e61634",
            adapter["release_target_commit"],
        )
        self.assertEqual(
            "2f974c9bb2ba13888d69682f86f30f58922d30eb",
            adapter["source_tree"],
        )
        self.assertFalse(release["preserved_contract"]["renderer_behavior_changed"])


if __name__ == "__main__":
    unittest.main()
