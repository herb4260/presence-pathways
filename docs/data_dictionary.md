# Data dictionary

All demonstration rows are synthetic.

## EMA observations

| Variable | Type | Range / values | Meaning |
| --- | --- | --- | --- |
| participant_id | string | `SYN001`… | Synthetic identifier |
| study_day | integer | 1–21 | Day in the sampling period |
| timestamp | ISO datetime | synthetic | Exact timestamps must not be public in a real study |
| practice_mode | category | none, silent prayer, scripture reflection, worship, communal prayer | Main practice since prior prompt |
| practice_minutes | integer | 0–240 allowed | Approximate duration |
| presence_intensity | float | 0–10 | Participant's felt intensity of presence or grace |
| embodied_warmth | float | 0–10 | Warmth in chest or body |
| tears_minutes | integer | 0–120 allowed | Approximate duration of tears |
| peace | float | 0–10 | Current peace |
| feeling_loved | float | 0–10 | Feeling loved or personally known by God |
| gratitude | float | 0–10 | Current gratitude |
| worry_relief | float | 0–10 | Loosening of worry's hold on attention |
| narrative_coherence | float | 0–10 | Fit within the participant's life story |
| community_connection | float | 0–10 | Connection to faith community or trusted others |
| distress | float | 0–10 | Current distress or overwhelm |
| daily_functioning | float | 0–10 | Ability to carry out needed activities |
| sense_of_control | float | 0–10 | Choice or control in relation to the experience |
| sleep_hours | float | 0–18 allowed | Prior night's sleep |

## Derived constructs

| Variable | Formula |
| --- | --- |
| attentional_pathway | mean(worry_relief, peace) |
| emotional_pathway | mean(peace, gratitude) |
| relational_pathway | feeling_loved |
| narrative_pathway | narrative_coherence |
| communal_pathway | community_connection |
| recovery_index | mean(peace, worry_relief, daily_functioning, 10 − distress) |

## Interview excerpts

`machine_suggested_codes` are auditable keyword matches only. `human_verified_codes` and `interpretive_memo` represent a fictional researcher's review in the synthetic demonstration.
