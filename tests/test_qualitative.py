from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from presence_pathways.qualitative import load_codebook, suggest_codes  # noqa: E402


class QualitativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.codebook = load_codebook(ROOT / "instruments" / "qualitative_codebook.yml")

    def test_suggestions_expose_matches_and_review_status(self) -> None:
        suggestions = suggest_codes(
            "I felt warmth in my chest and the worry loosened its hold.", self.codebook
        )
        codes = {item["code"] for item in suggestions}
        self.assertIn("embodied_change", codes)
        self.assertIn("attentional_shift", codes)
        self.assertTrue(
            all(item["status"] == "candidate_requires_human_review" for item in suggestions)
        )

    def test_no_match_does_not_invent_a_code(self) -> None:
        self.assertEqual(suggest_codes("A neutral sentence with no matching terms.", self.codebook), [])


if __name__ == "__main__":
    unittest.main()
