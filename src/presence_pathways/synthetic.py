"""Reproducible synthetic data for public demonstrations.

The generator encodes plausible patterns only to exercise the software. Its
outputs are not estimates of real religious or psychological phenomena.
"""

from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
import pandas as pd


PRACTICES = np.array(
    ["none", "silent_prayer", "scripture_reflection", "worship", "communal_prayer"]
)


def _bounded(value: float, low: float = 0.0, high: float = 10.0) -> float:
    return round(float(np.clip(value, low, high)), 1)


def generate_demo_cohort(
    participants: int = 36,
    days: int = 21,
    seed: int = 20260814,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Generate EMA, participant, and interview-excerpt tables."""

    rng = np.random.default_rng(seed)
    start = datetime(2026, 1, 12, 20, 0)
    ema_rows: list[dict] = []
    participant_rows: list[dict] = []

    for number in range(1, participants + 1):
        pid = f"SYN{number:03d}"
        absorption = float(rng.normal(0, 0.9))
        baseline_distress = float(np.clip(rng.normal(5.3, 1.4), 1.5, 8.8))
        community_orientation = float(rng.normal(0, 0.8))
        presence_tendency = float(rng.normal(0, 0.9))
        field_context = rng.choice(
            ["urban_congregation", "campus_fellowship", "small_group_network"],
            p=[0.45, 0.25, 0.30],
        )
        participant_rows.append(
            {
                "participant_id": pid,
                "field_context": field_context,
                "age_band": rng.choice(["20s", "30s", "40s", "50plus"], p=[0.25, 0.38, 0.24, 0.13]),
                "baseline_distress": round(baseline_distress, 1),
                "absorption_z": round(absorption, 2),
                "community_orientation_z": round(community_orientation, 2),
            }
        )

        previous_peace = 4.5
        for day in range(1, days + 1):
            if rng.random() > 0.89:
                continue

            weekend = (start + timedelta(days=day - 1)).weekday() >= 5
            practice_probs = np.array([0.17, 0.29, 0.22, 0.18, 0.14])
            if weekend:
                practice_probs = np.array([0.10, 0.20, 0.18, 0.27, 0.25])
            mode = str(rng.choice(PRACTICES, p=practice_probs))
            base_minutes = {
                "none": 0,
                "silent_prayer": 19,
                "scripture_reflection": 24,
                "worship": 31,
                "communal_prayer": 37,
            }[mode]
            minutes = 0 if mode == "none" else int(np.clip(rng.normal(base_minutes, 11), 3, 80))
            communal = 1.0 if mode in {"worship", "communal_prayer"} else 0.0
            practice_signal = np.log1p(minutes) / np.log(81)

            daily_stressor = float(rng.normal(0, 1.0))
            presence = _bounded(
                4.0
                + 1.15 * practice_signal
                + 0.62 * absorption
                + 0.35 * communal
                + 0.42 * presence_tendency
                - 0.28 * daily_stressor
                + rng.normal(0, 1.05)
            )
            warmth = _bounded(1.3 + 0.63 * presence + 0.25 * absorption + rng.normal(0, 1.25))
            tears = int(
                np.clip(
                    rng.gamma(shape=1.2 + presence / 5.5, scale=1.9) - 1.1,
                    0,
                    25,
                )
            )
            loved = _bounded(1.1 + 0.76 * presence + 0.20 * communal + rng.normal(0, 1.05))
            gratitude = _bounded(1.6 + 0.64 * presence + 0.14 * previous_peace + rng.normal(0, 1.05))
            peace = _bounded(
                1.7
                + 0.57 * presence
                + 0.14 * previous_peace
                - 0.34 * daily_stressor
                + rng.normal(0, 1.0)
            )
            worry_relief = _bounded(
                1.4 + 0.55 * presence + 0.22 * peace - 0.42 * daily_stressor + rng.normal(0, 1.0)
            )
            narrative = _bounded(2.0 + 0.47 * presence + 0.16 * day / days + rng.normal(0, 1.05))
            community = _bounded(
                3.0
                + 1.65 * communal
                + 0.46 * community_orientation
                + 0.22 * presence
                + rng.normal(0, 1.15)
            )
            distress = _bounded(
                baseline_distress
                + 0.80 * daily_stressor
                - 0.31 * peace
                - 0.16 * worry_relief
                + rng.normal(0, 0.9)
            )
            functioning = _bounded(4.0 + 0.29 * peace - 0.31 * distress + 0.06 * day + rng.normal(0, 0.9))
            control = _bounded(3.1 + 0.28 * peace + 0.21 * narrative - 0.19 * distress + rng.normal(0, 0.9))
            sleep = round(float(np.clip(rng.normal(6.7 - 0.12 * daily_stressor, 0.9), 3.5, 9.5)), 1)
            timestamp = start + timedelta(days=day - 1, minutes=int(rng.normal(0, 45)))

            ema_rows.append(
                {
                    "participant_id": pid,
                    "study_day": day,
                    "timestamp": timestamp.isoformat(timespec="minutes"),
                    "practice_mode": mode,
                    "practice_minutes": minutes,
                    "presence_intensity": presence,
                    "embodied_warmth": warmth,
                    "tears_minutes": tears,
                    "peace": peace,
                    "feeling_loved": loved,
                    "gratitude": gratitude,
                    "worry_relief": worry_relief,
                    "narrative_coherence": narrative,
                    "community_connection": community,
                    "distress": distress,
                    "daily_functioning": functioning,
                    "sense_of_control": control,
                    "sleep_hours": sleep,
                }
            )
            previous_peace = peace

    ema = pd.DataFrame(ema_rows)
    people = pd.DataFrame(participant_rows)
    excerpts = generate_synthetic_excerpts(people["participant_id"].tolist(), rng)
    return ema, people, excerpts


def generate_synthetic_excerpts(participant_ids: list[str], rng: np.random.Generator) -> pd.DataFrame:
    """Create fictional excerpts with researcher-verified example codes."""

    templates = [
        (
            "I first noticed warmth across my chest. The situation had not changed, but my attention was no longer trapped by the worry.",
            "embodied_change|attentional_shift",
            "Body sensation and attentional movement are narrated together.",
        ),
        (
            "The tears came before I could explain anything. I understood them as relief and as being known by God.",
            "embodied_change|relational_presence",
            "Tears acquire meaning through a perceived relationship.",
        ),
        (
            "During prayer I felt loved rather than judged. That changed the story I had been telling about myself.",
            "relational_presence|narrative_reframing",
            "Divine relationship supports a revised self-narrative.",
        ),
        (
            "The peace was intense that evening, but what made it last was talking about it with people who knew me well.",
            "emotional_change|communal_validation|persistence",
            "Community is described as a mechanism of durability.",
        ),
        (
            "I was grateful the next morning, although the old fear returned later. Recovery felt more like a rhythm than a single cure.",
            "emotional_change|nonlinear_change",
            "The account resists a simple permanent-transformation story.",
        ),
        (
            "I could choose whether to continue the prayer and I remained able to work. That sense of control mattered to how I understood it.",
            "agency|functioning|interpretive_boundary",
            "Agency and functioning help describe, not diagnose, the experience.",
        ),
        (
            "A scripture phrase became personally vivid. It did not sound audible, but it felt addressed to my exact situation.",
            "attentional_shift|relational_presence|sensory_quality",
            "The participant carefully distinguishes vividness from external sound.",
        ),
        (
            "At first I kept the experience private because I was unsure what others would call it. The small group gave me language for it.",
            "ambiguity|communal_validation|narrative_reframing",
            "Shared language organizes an initially ambiguous event.",
        ),
        (
            "I still had difficult days, but the memory of being accompanied changed how alone the difficulty felt.",
            "relational_presence|persistence|nonlinear_change",
            "Persistence lies in a changed relation to distress, not its disappearance.",
        ),
        (
            "The experience became frightening when I could not sleep and felt pushed to act. I sought help from both a clinician and my pastor.",
            "distress_signal|agency|community_care",
            "The synthetic case demonstrates a dual clinical and community response.",
        ),
        (
            "Singing with other people made the presence feel stronger than when I prayed alone, though the quiet prayer felt more intimate.",
            "communal_validation|relational_presence|practice_comparison",
            "Different practices shape distinct qualities rather than a single intensity scale.",
        ),
        (
            "Weeks later I could not reproduce the same warmth. What remained was a more patient way of responding to fear.",
            "embodied_change|persistence|behavioral_integration",
            "A transient sensation is distinguished from longer behavioral integration.",
        ),
    ]

    rows: list[dict] = []
    selected_ids = participant_ids[: min(30, len(participant_ids))]
    for index, pid in enumerate(selected_ids, start=1):
        text, codes, memo = templates[(index - 1) % len(templates)]
        rows.append(
            {
                "excerpt_id": f"EX{index:03d}",
                "participant_id": pid,
                "interview_wave": "follow_up" if index % 2 else "midpoint",
                "excerpt_text": text,
                "human_verified_codes": codes,
                "interpretive_memo": memo,
                "synthetic": True,
            }
        )
    return pd.DataFrame(rows)
