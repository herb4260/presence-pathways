from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from presence_pathways.privacy import pseudonymize_id, suppress_small_cells  # noqa: E402


class PrivacyTests(unittest.TestCase):
    def test_pseudonym_is_stable_but_salt_specific(self) -> None:
        first = pseudonymize_id("raw-17", "study-salt-alpha")
        repeat = pseudonymize_id("raw-17", "study-salt-alpha")
        second_study = pseudonymize_id("raw-17", "study-salt-beta")
        self.assertEqual(first, repeat)
        self.assertNotEqual(first, second_study)
        self.assertNotIn("raw-17", first)

    def test_short_salt_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            pseudonymize_id("raw-17", "short")

    def test_small_cells_are_suppressed(self) -> None:
        table = pd.DataFrame({"group": ["a", "b"], "n": [3, 9]})
        result = suppress_small_cells(table)
        self.assertEqual(result.loc[0, "n"], "<5")
        self.assertEqual(result.loc[1, "n"], 9)


if __name__ == "__main__":
    unittest.main()
