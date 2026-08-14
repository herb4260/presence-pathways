from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from presence_pathways.schema import SchemaError, validate_ema  # noqa: E402
from presence_pathways.synthetic import generate_demo_cohort  # noqa: E402


class SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ema, _, _ = generate_demo_cohort(participants=4, days=7, seed=12)

    def test_synthetic_data_passes_schema(self) -> None:
        validated = validate_ema(self.ema)
        self.assertEqual(len(validated), len(self.ema))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(validated["timestamp"]))

    def test_out_of_range_value_fails(self) -> None:
        broken = self.ema.copy()
        broken.loc[broken.index[0], "presence_intensity"] = 12
        with self.assertRaisesRegex(SchemaError, "outside"):
            validate_ema(broken)

    def test_duplicate_participant_day_fails(self) -> None:
        broken = pd.concat([self.ema, self.ema.iloc[[0]]], ignore_index=True)
        with self.assertRaisesRegex(SchemaError, "Duplicate"):
            validate_ema(broken)


if __name__ == "__main__":
    unittest.main()
