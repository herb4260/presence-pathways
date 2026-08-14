"""Small privacy utilities for research-data release preparation."""

from __future__ import annotations

import hashlib

import pandas as pd


def pseudonymize_id(raw_id: str, salt: str) -> str:
    """Create a stable, non-reversible display identifier within one study."""

    if not salt or len(salt) < 8:
        raise ValueError("Use a study-specific salt of at least 8 characters")
    digest = hashlib.sha256(f"{salt}:{raw_id}".encode("utf-8")).hexdigest()
    return f"P-{digest[:10]}"


def suppress_small_cells(
    table: pd.DataFrame,
    count_column: str = "n",
    minimum: int = 5,
    suppression_label: str = "<5",
) -> pd.DataFrame:
    """Replace counts below a public-release threshold."""

    output = table.copy()
    mask = output[count_column] < minimum
    output[count_column] = output[count_column].astype(object)
    output.loc[mask, count_column] = suppression_label
    return output


def public_ema_view(frame: pd.DataFrame) -> pd.DataFrame:
    """Drop high-risk fields from an EMA table before public visualization."""

    permitted = [
        "participant_id",
        "study_day",
        "practice_mode",
        "presence_intensity",
        "peace",
        "gratitude",
        "worry_relief",
        "distress",
        "daily_functioning",
    ]
    missing = set(permitted) - set(frame.columns)
    if missing:
        raise ValueError(f"Cannot create public view; missing {sorted(missing)}")
    return frame[permitted].copy()
