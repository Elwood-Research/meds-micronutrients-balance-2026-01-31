# Research plan: Medication burden x micronutrients and balance (NHANES)

## Study design
- Cross-sectional analysis using NHANES 2003-2004 (cycle C) to maximize documented overlap between balance testing and dietary intake.
- Primary analytic population: adults 60+ years (BAX balance exam target age range in cycle C is 40-150 years; older adults defined as 60+).

## Data sources and candidate datasets (processed data + docs confirmed)
- Demographics and survey design: `DEMO_C` (age, sex, race/ethnicity, education, income-to-poverty, strata/PSU).
- Balance examination outcomes: `BAX_C` (balance test pass/fail and failure time variables; subsample weights `WTSB2YR`).
- Dietary intake (micronutrients): `DR1TOT_C` (vitamin B12, folate as dietary intake; energy). **Note: Vitamin D intake is not available in cycle C and will be omitted.**
- Body size: `BMX_C` (BMI).
- Diabetes status: `DIQ_C` (self-reported diabetes).
- Hypertension status: `BPQ_C` (self-reported high blood pressure).

## Exposure definition (medication burden proxy)
- Primary exposure: cardiometabolic comorbidity burden as a proxy for medication burden.
- Construct a count of self-reported conditions with documented questionnaires:
  - Diabetes (`DIQ010` from `DIQ_C`)
  - Hypertension (`BPQ020` from `BPQ_C`)
  - High cholesterol (`BPQ080` from `BPQ_C`)
- Scale: 0-3 conditions (also consider categories 0, 1, 2+ for stability).

## Micronutrient status (diet only)
- **Vitamin D: Unavailable in cycle C. Omitted from analysis and documented as a limitation.**
- Vitamin B12 intake (mcg): `DR1TVB12` (dietary from `DR1TOT_C`).
- Folate intake (mcg DFE): `DR1TFDFE` (dietary from `DR1TOT_C`).
- Primary micronutrient metric: continuous dietary intake (also consider tertiles/quartiles for interaction visualization).

## Outcomes (physical performance and balance)
- Objective balance performance from `BAX`:
  - Pass/fail indicators for test conditions (e.g., `BAXPFC11`, `BAXPFC21`, `BAXPFC31`, `BAXPFC41`).
  - Failure time in seconds (e.g., `BAXFTC11`, `BAXFTC21`, `BAXFTC31`, `BAXFTC41`).
- Self-reported standing/balance readiness from `BAX` screening items (e.g., `BAQ110`, `BAQ130`).
- Primary outcome: failure time in the most challenging condition (foam pad, eyes closed) and/or composite balance failure indicator across conditions.

## Covariates
- Demographics: age (`RIDAGEYR`), sex (`RIAGENDR`), race/ethnicity (`RIDRETH3`).
- Socioeconomic: education (`DMDEDUC2`), income-to-poverty ratio (`INDFMPIR`).
- Body size: BMI (`BMXBMI`).
- Health conditions: diabetes (`DIQ010`), hypertension (`BPQ020`).
- Dietary energy intake: `DR1TKCAL`.

## Eligibility and inclusion criteria
- Age 60-69 years (older adults within BAX target range).
- Completed balance exam (`BAAEXSTS = 1`) and non-missing primary balance outcome.
- Reliable day-1 dietary recall (`DR1DRSTZ = 1`) for dietary micronutrients.
- Non-missing supplement intake variables for total intake (allow zero).
- Non-missing comorbidity variables used to construct burden.

## Exclusion criteria
- Missing survey design variables (`SDMVPSU`, `SDMVSTRA`) or balance subsample weights (`WTSBA2YR`).
- Implausible intake values flagged in dietary recall status (if any additional NHANES reliability flags apply).

## Analysis plan
- Use survey-weighted regression with BAX subsample weights (`WTSB2YR`), `SDMVPSU`, and `SDMVSTRA`.
- Model outcomes as:
  - Continuous: failure time (seconds) using linear regression (or log-transform if skewed).
  - Binary: pass/fail using logistic regression.
- Main effects: comorbidity burden and each micronutrient (B12, folate). **Vitamin D omitted due to unavailability.**
- Interaction tests: comorbidity burden x each micronutrient (B12, folate).
- Report marginal effects and stratified estimates at low vs high comorbidity burden.

## Missing data strategy
- Use complete-case analysis for primary models; report missingness by variable.
- Sensitivity analyses with multiple imputation if missingness exceeds 10% for key exposures.

## Feasibility checks completed
- Confirmed dietary micronutrient variables in `DR1TOT_C` dictionary (B12, folate available; vitamin D unavailable).
- Confirmed balance outcomes in `BAX_C` dictionary with weights `WTSB2YR`.
- Confirmed comorbidity variables in `DIQ_C` and `BPQ_C` dictionaries for proxy burden.
- Confirmed all datasets have documentation in `Processed Data/Doc`.
