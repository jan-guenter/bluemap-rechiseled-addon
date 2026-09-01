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
                    "size": 650_002,
                    "sha256": "e28b83c30e56b8f779751093008e9d49ea1a7d9e08ea54cb384780c1eac938d8",
                },
                "sources_jar": {
                    "file_name": "bluemap-rechiseled-addon-0.1.0-alpha.3-sources.jar",
                    "size": 584_004,
                    "sha256": "aca2d9521f3742a8b361e67591c7945308ad9a122fa42bbdc5a3c21cf4351b55",
                },
                "pom": {
                    "file_name": "bluemap-rechiseled-addon-0.1.0-alpha.3.pom",
                    "size": 1_359,
                    "sha256": "72120cd6ac5233e7dd2ed49cf003ae462efd85009ef70391b9972ca410b101d9",
                },
                "gradle_module": {
                    "file_name": "bluemap-rechiseled-addon-0.1.0-alpha.3.module.json",
                    "size": 2_841,
                    "sha256": "7b49972d42c64ad02dad2abd7db90c8954c20cce630deaac6e1fa1451aaa18d9",
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
        verification = release["verification"]
        self.assertEqual(
            "5243f0ff9d12e7fb1087eac1f63e9a63e74ba2c9",
            verification["authoritative_pr_ci_source_commit"],
        )
        self.assertEqual(33_473_228_909, verification["authoritative_pr_ci_run_id"])
        self.assertTrue(verification["release_identity_sealed"])


if __name__ == "__main__":
    unittest.main()
