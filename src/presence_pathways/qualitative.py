"""Auditable suggestion helpers for researcher-led qualitative coding."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml


def load_codebook(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        content = yaml.safe_load(handle)
    return content["codes"]


def suggest_codes(text: str, codebook: dict, limit: int = 3) -> list[dict]:
    """Return transparent keyword matches as candidates, never final labels."""

    lowered = text.lower()
    candidates: list[dict] = []
    for code, spec in codebook.items():
        matched = [keyword for keyword in spec.get("keywords", []) if keyword.lower() in lowered]
        if matched:
            candidates.append(
                {
                    "code": code,
                    "matched_terms": matched,
                    "match_count": len(matched),
                    "status": "candidate_requires_human_review",
                }
            )
    candidates.sort(key=lambda item: (-item["match_count"], item["code"]))
    return candidates[:limit]


def annotate_excerpts(excerpts: pd.DataFrame, codebook: dict) -> pd.DataFrame:
    """Attach suggestions while preserving human codes and memos separately."""

    output = excerpts.copy()
    output["machine_suggested_codes"] = output["excerpt_text"].map(
        lambda text: "|".join(item["code"] for item in suggest_codes(text, codebook))
    )
    output["suggestion_status"] = "candidate_only_not_research_finding"
    return output
