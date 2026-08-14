# Project overview

Presence Pathways is an independent mixed-methods research software prototype for studying how experiences interpreted as divine presence may relate to psychological change over time.

## Research question

How do attentional, emotional, relational, narrative, and communal processes vary around experiences of felt divine presence, and how can those changes be followed over time without reducing participants' interpretations to a single score?

## Design

The prototype combines:

- a 21-day experience-sampling structure;
- bilingual English–Korean EMA items;
- phenomenological interview prompts;
- synthetic longitudinal data generation;
- within-person quantitative summaries;
- researcher-reviewed qualitative coding support;
- privacy checks for public outputs;
- unit tests and reproducible build scripts; and
- a static dashboard for inspecting synthetic results.

## Interpretation principles

The project does not attempt to prove or disprove divine action. It also does not treat unusual spiritual experiences as diagnoses. Quantitative results are descriptive and exploratory, and qualitative coding suggestions require human review.

## Reproducibility

All public demonstration data are synthetic. Running `python scripts/build_demo.py` regenerates the demo dataset and machine-readable result files from a fixed seed. Tests can be run with `python -m unittest discover -s tests -v`.

## Boundaries for real research

A real study would require ethics review, informed consent, community consultation, secure data handling, and a context-sensitive safety protocol. Identifiable narratives, exact locations, raw timestamps, audio, and linkage keys should not be committed to a public repository.
