"""End-to-end build for data, analyses, and the static research dashboard."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

from .analysis import add_constructs, analyze_dataset
from .qualitative import annotate_excerpts, load_codebook
from .schema import validate_ema
from .synthetic import generate_demo_cohort


def _frame_digest(frame: pd.DataFrame) -> str:
    payload = frame.to_csv(index=False, lineterminator="\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_demo(root: Path, *, seed: int = 20260814, check_reproducibility: bool = False) -> dict:
    ema, people, excerpts = generate_demo_cohort(seed=seed)
    ema = validate_ema(ema)

    if check_reproducibility:
        ema_again, people_again, excerpts_again = generate_demo_cohort(seed=seed)
        if _frame_digest(ema) != _frame_digest(validate_ema(ema_again)):
            raise RuntimeError("EMA generation is not reproducible")
        if _frame_digest(people) != _frame_digest(people_again):
            raise RuntimeError("Participant generation is not reproducible")
        if _frame_digest(excerpts) != _frame_digest(excerpts_again):
            raise RuntimeError("Excerpt generation is not reproducible")

    codebook = load_codebook(root / "instruments" / "qualitative_codebook.yml")
    annotated = annotate_excerpts(excerpts, codebook)
    analysis = analyze_dataset(ema)
    constructed = add_constructs(ema)

    demo_dir = root / "data" / "demo"
    result_dir = root / "results"
    dashboard_data = root / "docs" / "data"
    for directory in (demo_dir, result_dir, dashboard_data):
        directory.mkdir(parents=True, exist_ok=True)

    ema.to_csv(demo_dir / "ema_observations.csv", index=False)
    people.to_csv(demo_dir / "participants.csv", index=False)
    annotated.to_csv(demo_dir / "interview_excerpts.csv", index=False)
    constructed.to_csv(result_dir / "ema_with_constructs.csv", index=False)

    with (result_dir / "analysis_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(analysis, handle, indent=2, ensure_ascii=False)
    with (dashboard_data / "analysis_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(analysis, handle, indent=2, ensure_ascii=False)

    public_excerpts = annotated[
        [
            "excerpt_id",
            "interview_wave",
            "excerpt_text",
            "human_verified_codes",
            "interpretive_memo",
            "machine_suggested_codes",
            "suggestion_status",
            "synthetic",
        ]
    ].to_dict(orient="records")
    with (dashboard_data / "excerpts.json").open("w", encoding="utf-8") as handle:
        json.dump(public_excerpts, handle, indent=2, ensure_ascii=False)

    manifest = {
        "seed": seed,
        "ema_sha256": _frame_digest(ema),
        "participants_sha256": _frame_digest(people),
        "excerpts_sha256": _frame_digest(excerpts),
        "synthetic": True,
    }
    with (result_dir / "build_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
    return {"analysis": analysis, "manifest": manifest}
