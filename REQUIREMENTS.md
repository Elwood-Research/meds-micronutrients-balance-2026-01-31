# Data requirements

## Core datasets (to confirm availability)
- DEMO: age, sex, race/ethnicity, education, income, survey design variables, weights
- Prescription medications: medication name list and count (e.g., RXQ_RX or equivalent)
- Vitamin D labs (e.g., VID or equivalent)
- Vitamin B12 labs (e.g., B12)
- Folate labs (e.g., FOLATE)
- Physical performance outcomes (e.g., gait speed, grip, or functional tests)
- Balance outcomes (e.g., balance exam questionnaire/exam: BAX/BAQ)

## Covariates (expected)
- BMI or body measures (BMX)
- Smoking status (SMQ) or cotinine biomarkers (COT/COTNAL)
- Physical activity (PAQ) if available in selected cycles
- Chronic conditions (e.g., DIQ, BPQ)

## Notes
- Prefer NHANES cycles where all required lab and performance/balance measures overlap.
- Older adults only; handle survey weights appropriately for MEC/lab subsamples.
- Apply outlier screen for continuous variables: remove |z| > 4.
- Exclude categorical levels with <5% membership.
