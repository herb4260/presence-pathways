from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from presence_pathways.analysis import add_constructs, analyze_dataset, within_person_association  # noqa: E402
from presence_pathways.schema import validate_ema  # noqa: E402
from presence_pathways.synthetic import generate_demo_cohort  # noqa: E402


class AnalysisTests(unittest.TestCase):
    def test_constructs_have_expected_bounds(self) -> None:
        ema, _, _ = generate_demo_cohort(participants=8, days=10, seed=9)
        data = add_constructs(validate_ema(ema))
        for column in [
            "attentional_pathway",
            "emotional_pathway",
            "relational_pathway",
            "narrative_pathway",
            "communal_pathway",
            "recovery_index",
        ]:
            self.assertTrue(data[column].between(0, 10).all(), column)

    def test_within_person_slope_recovers_known_direction(self) -> None:
        rng = np.random.default_rng(4)
        rows = []
        for participant in range(20):
            intercept = rng.normal(0, 4)
            for day in range(12):
                x = rng.normal()
                y = intercept + 0.8 * x + rng.normal(0, 0.25)
                rows.append({"participant_id": participant, "x": x, "y": y})
        result = within_person_association(
            pd.DataFrame(rows), "x", "y", bootstrap_samples=150, seed=2
        )
        self.assertGreater(result.estimate, 0.65)
        self.assertLess(result.estimate, 0.95)
        self.assertGreater(result.ci_low, 0)

    def test_full_analysis_is_json_ready(self) -> None:
        ema, _, _ = generate_demo_cohort(participants=10, days=12, seed=101)
        results = analyze_dataset(validate_ema(ema))
        self.assertEqual(results["metadata"]["participants"], 10)
        self.assertEqual(len(results["associations"]), 6)
        self.assertFalse(results["metadata"]["causal_claim"])


if __name__ == "__main__":
    unittest.main()
