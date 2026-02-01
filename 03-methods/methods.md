# Methods

## Study design and data source
We will conduct a cross-sectional analysis of NHANES cycle C (2003-2004). The analytic sample will be restricted to participants eligible for balance testing and with complete balance examination data. All analyses will follow NHANES analytic guidance, accounting for complex survey design, primary sampling units (PSU), and strata.

## Study population
We will include adults aged 60+ years. Participants must have completed the balance exam and have valid balance outcomes and dietary recall data (day 1). We will exclude participants missing balance subsample weights (`WTSB2YR`) or survey design variables (`SDMVPSU`, `SDMVSTRA`).

## Outcomes: balance performance
Balance outcomes will be derived from `BAX_C` exam variables. Primary outcomes will include:
- Failure time (seconds) for the most challenging balance condition (`BAXFTC41`).
- Pass/fail indicators for each balance condition (`BAXPFC11`, `BAXPFC21`, `BAXPFC31`, `BAXPFC41`).
Secondary outcomes will include composite pass/fail indicators across conditions and additional failure time measures (`BAXFTC11`, `BAXFTC21`, `BAXFTC31`).

## Exposures
### Comorbidity burden proxy
Comorbidity burden will be constructed as a count (0-3) of self-reported cardiometabolic conditions from `DIQ_C` and `BPQ_C`:
- Diabetes (`DIQ010`)
- Hypertension (`BPQ020`)
- High cholesterol (`BPQ080`)
We will use the count as a continuous exposure and, for interpretability, also categorize as 0, 1, and 2+ conditions.

### Micronutrient intake
Dietary micronutrient intake will be obtained from `DR1TOT_C`:
- Vitamin B12: `DR1TVB12`
- Folate (DFE): `DR1TFDFE`
**Note: Vitamin D intake is unavailable in cycle C. Dietary supplement data is also unavailable, so analyses use dietary intake only.**
Primary analyses will use continuous intake measures. For visualization and interaction interpretation, we will also evaluate tertiles of intake and energy-adjusted intake per 1,000 kcal (`DR1TKCAL`).

## Covariates
Models will adjust for key demographic and health-related covariates:
- Age (`RIDAGEYR`), sex (`RIAGENDR`), race/ethnicity (`RIDRETH1` - cycle C uses RIDRETH1)
- Education (`DMDEDUC2`), income-to-poverty ratio (`INDFMPIR`)
- Body mass index (`BMXBMI`)
- Dietary energy intake (`DR1TKCAL`)

## Survey design and weights
All analyses will incorporate NHANES survey design variables (`SDMVPSU`, `SDMVSTRA`). The balance exam uses a subsample design, so we will apply `WTSB2YR` as the primary analysis weight. We will use the appropriate survey-weighted estimation procedures to compute population-representative estimates and robust standard errors.

## Data cleaning and exclusion rules
- **Outlier screening:** For all continuous variables, we will compute z-scores and remove observations with |z| > 4 prior to modeling.
- **Categorical level exclusion:** For categorical variables, levels with <5% membership will be excluded to avoid unstable estimates.

## Statistical analysis
We will fit survey-weighted regression models to evaluate associations between comorbidity burden, micronutrient intake, and balance outcomes:
- **Continuous outcomes:** Survey-weighted linear regression for failure time outcomes. If outcomes are right-skewed, we will use log-transformed times and report back-transformed estimates.
- **Binary outcomes:** Survey-weighted logistic regression for pass/fail indicators.

### Interaction terms
To test whether micronutrient intake modifies the association between comorbidity burden and balance, we will include interaction terms between comorbidity burden and each available micronutrient (vitamin B12, folate). We will report interaction p-values and present marginal estimates at clinically relevant intake levels (e.g., tertiles or 25th/75th percentiles).

## Sensitivity and robustness analyses
We will conduct the following sensitivity analyses:
- Alternative comorbidity burden parameterizations (0-3 count vs 0/1/2+ categories).
- Energy-adjusted micronutrient intake (per 1,000 kcal) vs absolute intake.
- Excluding participants who did not meet balance readiness screening criteria (`BAQ110`, `BAQ130`).
- Complete-case analysis vs models allowing missing covariate categories (when appropriate).

## Limitations
Vitamin D intake data is unavailable in NHANES cycle C and cannot be included in analyses. Dietary supplement data is also unavailable for this cycle, restricting analyses to dietary micronutrient intake only.

## Reporting standards
We will construct a STROBE flow diagram detailing sample selection, exclusions (including outlier removal and categorical exclusions), and the final analytic sample. All methods and results will be reported in accordance with STROBE recommendations for cross-sectional studies.
