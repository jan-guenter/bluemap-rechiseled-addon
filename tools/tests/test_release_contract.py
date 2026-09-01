# SPDX-License-Identifier: MIT
"""Static release-boundary regression coverage."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class ReleaseContractTest(unittest.TestCase):
    def test_alpha3_candidate_is_owner_accepted_and_preserves_alpha2(self) -> None:
        release = json.loads((ROOT / "provenance/release.json").read_text())
        self.assertEqual("owner-accepted-release-candidate", release["status"])
        self.assertFalse(release["published"])
        self.assertEqual("0.1.0-alpha.3", release["version"])
        self.assertEqual("v0.1.0-alpha.3", release["tag"])
        self.assertEqual(
            {
                "production_jar": {
                    "file_name": "bluemap-rechiseled-addon-0.1.0-alpha.3.jar",
                    "size": 650_048,
                    "sha256": "95c9e026b4b2826be67b594390c69b1c4d2d5c1036152fa5a36271a82a66ff33",
                },
                "sources_jar": {
                    "file_name": "bluemap-rechiseled-addon-0.1.0-alpha.3-sources.jar",
                    "size": 584_128,
                    "sha256": "a009811922b22f0a6b8fa43beabe624a4d811ff2208c2bf6be76ae8617c9a258",
                },
                "pom": {
                    "file_name": "bluemap-rechiseled-addon-0.1.0-alpha.3.pom",
                    "size": 1_359,
                    "sha256": "72120cd6ac5233e7dd2ed49cf003ae462efd85009ef70391b9972ca410b101d9",
                },
                "gradle_module": {
                    "file_name": "bluemap-rechiseled-addon-0.1.0-alpha.3.module.json",
                    "size": 2_841,
                    "sha256": "9e4f33e73606964fd2421db2d9ab6149d810fe0383d303f21626230a4da2de73",
                },
                "sha256sums": {
                    "file_name": "SHA256SUMS",
                    "size": 460,
                    "sha256": "65c3e50f26e5605dcec3001d5302b1fd4d3d1209c92b6391c1ba94ad6be27e31",
                },
            },
            release["candidate_artifacts"],
        )
        acceptance = release["owner_acceptance"]
        self.assertEqual(94, acceptance["release_candidate_equivalence"]["entry_count"])
        self.assertTrue(
            acceptance["release_candidate_equivalence"]["entry_payloads_byte_identical"]
        )
        self.assertEqual(
            "b85a128b6ab1b73f4accdd967c43f3b12a2816894217436f94207a10b2d80bca",
            acceptance["reviewed_entrypoint"]["class_sha256"],
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
            "b8ad0dea2a46f361489c097deb75a4090d302914",
            verification["authoritative_pr_ci_source_commit"],
        )
        self.assertEqual(33_528_747_904, verification["authoritative_pr_ci_run_id"])
        self.assertTrue(verification["release_identity_sealed"])


if __name__ == "__main__":
    unittest.main()
