"""Validation rules for longitudinal experience-sampling data."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


class SchemaError(ValueError):
    """Raised when a dataset violates a documented research-data contract."""


@dataclass(frozen=True)
class ScaleRule:
    minimum: float
    maximum: float


REQUIRED_COLUMNS = {
    "participant_id",
    "study_day",
    "timestamp",
    "practice_mode",
    "practice_minutes",
    "presence_intensity",
    "embodied_warmth",
    "tears_minutes",
    "peace",
    "feeling_loved",
    "gratitude",
    "worry_relief",
    "narrative_coherence",
    "community_connection",
    "distress",
    "daily_functioning",
    "sense_of_control",
    "sleep_hours",
}

SCALE_RULES = {
    "study_day": ScaleRule(1, 60),
    "practice_minutes": ScaleRule(0, 240),
    "presence_intensity": ScaleRule(0, 10),
    "embodied_warmth": ScaleRule(0, 10),
    "tears_minutes": ScaleRule(0, 120),
    "peace": ScaleRule(0, 10),
    "feeling_loved": ScaleRule(0, 10),
    "gratitude": ScaleRule(0, 10),
    "worry_relief": ScaleRule(0, 10),
    "narrative_coherence": ScaleRule(0, 10),
    "community_connection": ScaleRule(0, 10),
    "distress": ScaleRule(0, 10),
    "daily_functioning": ScaleRule(0, 10),
    "sense_of_control": ScaleRule(0, 10),
    "sleep_hours": ScaleRule(0, 18),
}

ALLOWED_PRACTICES = {
    "none",
    "silent_prayer",
    "scripture_reflection",
    "worship",
    "communal_prayer",
}


def validate_ema(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate EMA data and return a normalized copy.

    Validation is intentionally strict because silent range errors can create
    convincing but invalid longitudinal results.
    """

    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise SchemaError(f"Missing required columns: {', '.join(sorted(missing))}")

    data = frame.copy()
    data["participant_id"] = data["participant_id"].astype(str).str.strip()
    if data["participant_id"].eq("").any():
        raise SchemaError("participant_id cannot be empty")

    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    if data["timestamp"].isna().any():
        raise SchemaError("timestamp contains invalid values")

    duplicate = data.duplicated(["participant_id", "study_day"], keep=False)
    if duplicate.any():
        pairs = data.loc[duplicate, ["participant_id", "study_day"]].head(3)
        raise SchemaError(f"Duplicate participant-day rows: {pairs.to_dict('records')}")

    for column, rule in SCALE_RULES.items():
        data[column] = pd.to_numeric(data[column], errors="coerce")
        if data[column].isna().any():
            raise SchemaError(f"{column} contains missing or non-numeric values")
        invalid = ~data[column].between(rule.minimum, rule.maximum)
        if invalid.any():
            bad = data.loc[invalid, column].iloc[0]
            raise SchemaError(
                f"{column}={bad} is outside [{rule.minimum}, {rule.maximum}]"
            )

    unknown = set(data["practice_mode"].dropna()) - ALLOWED_PRACTICES
    if unknown:
        raise SchemaError(f"Unknown practice_mode values: {', '.join(sorted(unknown))}")

    return data.sort_values(["participant_id", "study_day"]).reset_index(drop=True)
