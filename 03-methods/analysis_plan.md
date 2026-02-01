# Analysis plan

## Objectives
1. Estimate associations between comorbidity burden proxy and balance performance in NHANES cycle C (2003-2004).
2. Evaluate whether dietary micronutrient intake (B12, folate) modifies these associations.

## Data sources and datasets
- `DEMO_C`: demographics and survey design (`RIDAGEYR`, `RIAGENDR`, `RIDRETH1`, `DMDEDUC2`, `INDFMPIR`, `SDMVPSU`, `SDMVSTRA`).
- `BAX_C`: balance exam outcomes (`BAXPFC11`, `BAXPFC21`, `BAXPFC31`, `BAXPFC41`, `BAXFTC11`, `BAXFTC21`, `BAXFTC31`, `BAXFTC41`) and screening items (`BAQ110`, `BAQ130`).
- `DIQ_C`: diabetes status (`DIQ010`).
- `BPQ_C`: hypertension (`BPQ020`) and high cholesterol (`BPQ080`).
- `DR1TOT_C`: day-1 dietary intake (`DR1TVB12`, `DR1TFDFE`, `DR1TKCAL`). **Note: Vitamin D unavailable.**
- `BMX_C`: body mass index (`BMXBMI`).

## Sample construction
1. Merge datasets by participant identifier.
2. Restrict to cycle C and adults aged 60+ years.
3. Require completed balance exam (`BAAEXSTS = 1`) and non-missing primary balance outcome (failure time or pass/fail indicator).
4. Require non-missing comorbidity variables and dietary micronutrient intake components.
5. Require valid survey design variables (`SDMVPSU`, `SDMVSTRA`) and balance subsample weights (`WTSB2YR`).

## Variable derivations
- **Comorbidity burden proxy:** count of `DIQ010`, `BPQ020`, and `BPQ080` (0-3). Create categories 0, 1, 2+ for stability.
- **Micronutrient intake:** dietary intake only for vitamin B12 and folate (DFE). **Supplement data and vitamin D unavailable.**
- **Energy adjustment:** micronutrients per 1,000 kcal using `DR1TKCAL` for sensitivity analyses.
- **Balance outcomes:**
  - Continuous: `BAXFTC41` as primary failure time; additional `BAXFTC11`, `BAXFTC21`, `BAXFTC31` as secondary.
  - Binary: `BAXPFC41` primary pass/fail; additional condition-specific pass/fail indicators.

## Data quality rules
- **Outlier screening:** For all continuous variables, compute z-scores and remove observations with |z| > 4 before modeling.
- **Categorical level exclusion:** Exclude levels with <5% membership from categorical variables.

## Survey design specification
- Use NHANES survey design variables `SDMVPSU` and `SDMVSTRA`.
- Apply balance subsample weights `WTSB2YR` for all BAX analyses.

## Primary models
We will fit survey-weighted regressions with covariate adjustment:
- **Continuous outcomes:** linear regression for failure time (log-transform if skewed).
- **Binary outcomes:** logistic regression for pass/fail indicators.

### Core covariates
Age (`RIDAGEYR`), sex (`RIAGENDR`), race/ethnicity (`RIDRETH1`), education (`DMDEDUC2`), income-to-poverty ratio (`INDFMPIR`), BMI (`BMXBMI`), and energy intake (`DR1TKCAL`).

### Interaction terms
Each model will include interaction terms between comorbidity burden and each available micronutrient (vitamin B12, folate). We will report interaction p-values and marginal effects at low and high intake levels (e.g., 25th/75th percentiles or tertiles).

## Sensitivity analyses
1. Alternative comorbidity burden parameterization: 0-3 count vs 0/1/2+ categories.
2. Micronutrient exposure definitions: absolute vs energy-adjusted intake per 1,000 kcal.
3. Excluding participants who did not meet balance readiness screening (`BAQ110`, `BAQ130`).
4. Complete-case vs models allowing missing covariate categories (when appropriate).

## Limitations
- Vitamin D intake data unavailable in cycle C.
- Dietary supplement data unavailable; analyses restricted to dietary micronutrient intake only.

## Reporting
- Produce weighted descriptive statistics for all variables.
- Report adjusted model coefficients (or odds ratios) with 95% confidence intervals.
- Construct a STROBE flow diagram documenting sample derivation, exclusions (including outlier and categorical exclusions), and the final analytic sample.
