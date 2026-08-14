# Exploratory analysis plan

## Research questions

1. On days when a participant reports stronger felt presence than usual for that person, what else changes in attention, emotion, relational experience, narrative coherence, community connection, distress, and functioning?
2. Does stronger felt presence on one day co-occur with a changed recovery index on the next consecutive observed day?
3. How do interviews and fieldnotes explain cases that do not follow the average quantitative pattern?
4. Which changes persist when the peak embodied intensity no longer does?

## Constructs

| Construct | Demonstration operationalization | Important limitation |
| --- | --- | --- |
| Felt presence | Single 0–10 participant-interpreted item | Intensity does not capture quality, meaning, or metaphysical truth |
| Attentional pathway | Mean of peace and loosening of worry's attentional hold | Overlaps with affect and must be interpreted with narrative data |
| Emotional pathway | Mean of peace and gratitude | Positive emotion is not identical to healing |
| Relational pathway | Feeling loved or personally known | Does not represent every religious model of divine relationship |
| Narrative pathway | Life-story coherence | Coherence can conceal conflict; ambiguity may be valuable |
| Communal pathway | Connection to faith community or trusted others | High connection is not always supportive or non-coercive |
| Recovery index | Peace, worry relief, functioning, and reverse-coded distress | A descriptive composite, not a clinical endpoint |

## Quantitative model

For exposure \(x_{it}\) and outcome \(y_{it}\), the demo estimates a person-centered slope:

\[
\hat\beta = \frac{\sum_i\sum_t(x_{it}-\bar{x}_i)(y_{it}-\bar{y}_i)}{\sum_i\sum_t(x_{it}-\bar{x}_i)^2}
\]

Confidence intervals use a participant-level cluster bootstrap. The unit tests verify that the implementation recovers known directions in synthetic data.

This estimate is not causal. A real study should preregister covariates, assess time-varying confounding, model measurement error, examine missingness, and use multilevel sensitivity analyses.

## Qualitative analysis

1. Read full interviews before fragmenting text into codes.
2. Write a case memo for each participant.
3. Apply a provisional deductive codebook.
4. Add inductive codes and record when definitions change.
5. Compare high-intensity/low-persistence and low-intensity/high-persistence cases.
6. Search actively for negative cases and rival explanations.
7. Return from excerpts to full sequence, scene, and relationship.

The keyword helper records only transparent candidate matches. It must never produce the final analytic code, clinical label, or interpretation.

## Integration

Create a joint display with one row per case and columns for trajectory, key scenes, community response, rival explanation, and researcher memo. Use numbers to locate cases for deeper reading; use ethnography to revise the meaning of the numerical constructs.

## Claims not supported by this design

- that divine action was proved or disproved;
- that felt presence caused recovery;
- that one religious practice is clinically superior;
- that an intense spiritual experience is inherently healthy or pathological;
- that a synthetic demonstration is an empirical result.
