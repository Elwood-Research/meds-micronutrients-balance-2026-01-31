# Variables

## Outcomes (balance/physical performance)
- `BAX_C`
  - Balance test pass/fail: `BAXPFC11`, `BAXPFC21`, `BAXPFC31`, `BAXPFC41`.
  - Failure time (seconds): `BAXFTC11`, `BAXFTC21`, `BAXFTC31`, `BAXFTC41`.
  - Screening readiness: `BAQ110` (stand on your own), `BAQ130` (dizziness/lightheadedness).

## Primary exposure (medication burden proxy)
- `DIQ_C`
  - `DIQ010` (diabetes)
- `BPQ_C`
  - `BPQ020` (ever told high blood pressure)
  - `BPQ080` (ever told high cholesterol)
- Construct comorbidity count (0-3 conditions); consider 0, 1, 2+ categories for stability.

## Micronutrient status (diet only)
- `DR1TOT_C` (dietary intake)
  - `DR1TVB12` (vitamin B12, mcg)
  - `DR1TFDFE` (folate DFE, mcg)
  - `DR1TKCAL` (energy, kcal)
- **Note: Vitamin D intake is unavailable in cycle C and cannot be included. Dietary supplement data (`DSQTOT`) is also unavailable for cycle C.**

## Covariates
- `DEMO_C`
  - `RIDAGEYR` (age)
  - `RIAGENDR` (sex)
  - `RIDRETH1` (race/ethnicity - cycle C uses RIDRETH1)
  - `DMDEDUC2` (education)
  - `INDFMPIR` (income-to-poverty ratio)
  - `SDMVPSU`, `SDMVSTRA` (survey design)
- `BMX_C`
  - `BMXBMI` (BMI)

## Weights
- `BAX_C`: `WTSB2YR` for balance subsample analyses.
