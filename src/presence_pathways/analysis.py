"""Transparent longitudinal summaries for Presence Pathways."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Association:
    exposure: str
    outcome: str
    estimate: float
    ci_low: float
    ci_high: float
    observations: int
    participants: int
    interpretation: str


def add_constructs(frame: pd.DataFrame) -> pd.DataFrame:
    """Add theory-linked composite scores without changing raw measures."""

    data = frame.copy()
    data["attentional_pathway"] = data[["worry_relief", "peace"]].mean(axis=1)
    data["emotional_pathway"] = data[["peace", "gratitude"]].mean(axis=1)
    data["relational_pathway"] = data["feeling_loved"]
    data["narrative_pathway"] = data["narrative_coherence"]
    data["communal_pathway"] = data["community_connection"]
    data["recovery_index"] = pd.concat(
        [
            data["peace"],
            data["worry_relief"],
            data["daily_functioning"],
            10 - data["distress"],
        ],
        axis=1,
    ).mean(axis=1)
    return data


def _center_within(data: pd.DataFrame, column: str, group: str = "participant_id") -> pd.Series:
    return data[column] - data.groupby(group)[column].transform("mean")


def within_person_association(
    data: pd.DataFrame,
    exposure: str,
    outcome: str,
    *,
    seed: int = 41,
    bootstrap_samples: int = 600,
    interpretation: str = "Same-day within-person association",
) -> Association:
    """Estimate a person-centered slope with a participant cluster bootstrap.

    This is an exploratory association. It is intentionally not labeled as a
    causal effect or mediation estimate.
    """

    clean = data[["participant_id", exposure, outcome]].dropna().copy()
    clean["x_centered"] = _center_within(clean, exposure)
    clean["y_centered"] = _center_within(clean, outcome)
    clean["numerator"] = clean["x_centered"] * clean["y_centered"]
    clean["denominator"] = clean["x_centered"] ** 2
    by_person = clean.groupby("participant_id")[["numerator", "denominator"]].sum()
    denominator = float(by_person["denominator"].sum())
    if denominator <= 0:
        raise ValueError(f"No within-person variation in {exposure}")
    estimate = float(by_person["numerator"].sum() / denominator)

    rng = np.random.default_rng(seed)
    values = by_person.to_numpy()
    boot = np.empty(bootstrap_samples)
    for index in range(bootstrap_samples):
        sample = values[rng.integers(0, len(values), len(values))]
        boot[index] = sample[:, 0].sum() / sample[:, 1].sum()

    return Association(
        exposure=exposure,
        outcome=outcome,
        estimate=round(estimate, 3),
        ci_low=round(float(np.quantile(boot, 0.025)), 3),
        ci_high=round(float(np.quantile(boot, 0.975)), 3),
        observations=len(clean),
        participants=clean["participant_id"].nunique(),
        interpretation=interpretation,
    )


def next_day_association(data: pd.DataFrame, outcome: str = "recovery_index") -> Association:
    """Associate today's felt presence with the next observed consecutive day."""

    ordered = data.sort_values(["participant_id", "study_day"]).copy()
    ordered["next_day"] = ordered.groupby("participant_id")["study_day"].shift(-1)
    ordered["next_outcome"] = ordered.groupby("participant_id")[outcome].shift(-1)
    pairs = ordered.loc[ordered["next_day"] == ordered["study_day"] + 1].copy()
    return within_person_association(
        pairs,
        "presence_intensity",
        "next_outcome",
        seed=77,
        interpretation="Today's presence and next-day recovery; exploratory, non-causal",
    )


def analyze_dataset(frame: pd.DataFrame) -> dict:
    """Return public-facing, JSON-compatible summaries."""

    data = add_constructs(frame)
    outcomes = [
        "attentional_pathway",
        "emotional_pathway",
        "relational_pathway",
        "narrative_pathway",
        "communal_pathway",
        "recovery_index",
    ]
    associations = [
        within_person_association(
            data,
            "presence_intensity",
            outcome,
            seed=100 + index,
        )
        for index, outcome in enumerate(outcomes)
    ]
    lagged = next_day_association(data)

    daily = (
        data.groupby("study_day")
        .agg(
            presence_intensity=("presence_intensity", "mean"),
            recovery_index=("recovery_index", "mean"),
            peace=("peace", "mean"),
            distress=("distress", "mean"),
            observations=("participant_id", "size"),
        )
        .reset_index()
        .round(2)
    )
    trajectories = (
        data.loc[data["participant_id"].isin(sorted(data["participant_id"].unique())[:8])]
        [["participant_id", "study_day", "presence_intensity", "recovery_index", "peace", "distress"]]
        .round(2)
    )

    return {
        "metadata": {
            "participants": int(data["participant_id"].nunique()),
            "observations": int(len(data)),
            "study_days": int(data["study_day"].max()),
            "synthetic": True,
            "causal_claim": False,
        },
        "associations": [asdict(item) for item in associations],
        "lagged_association": asdict(lagged),
        "daily_summary": daily.to_dict(orient="records"),
        "trajectories": trajectories.to_dict(orient="records"),
    }
