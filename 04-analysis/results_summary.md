# Analysis Results Summary

## Study Overview
**Title:** Comorbidity Burden, Micronutrient Intake, and Balance Performance in Older Adults  
**NHANES Cycle:** C (2003-2004)  
**Population:** Adults aged 60+ years  
**Final Analytic Sample:** 788 participants

---

## Sample Derivation (STROBE Flow)

| Step | N |
|------|---|
| Initial merge (BAX_C + DEMO_C) | 3,086 |
| Age 60+ years | 1,750 |
| Balance exam complete | 1,343 |
| Valid balance outcome (BAXFTC41) | 930 |
| Valid survey design variables | 930 |
| Valid comorbidity data | 812 |
| Valid micronutrient data | 802 |
| After outlier removal (|z| > 4) | **788** |

---

## Key Findings

### 1. Descriptive Statistics (Weighted)

**Demographics:**
- Mean age: 70.9 years (SD 7.1)
- Sex: 42.7% male, 57.3% female
- Race/ethnicity: 83.6% Non-Hispanic White, 6.1% Non-Hispanic Black, 5.2% Hispanic

**Health Characteristics:**
- Mean BMI: 27.8 kg/m² (SD 5.0)
- Comorbidity burden: 1.33 conditions on average (SD 0.88)
  - 0 conditions: 18.5%
  - 1 condition: 40.4%
  - 2+ conditions: 41.1%

**Micronutrient Intake (Dietary Only):**
- Vitamin B12: Mean 4.50 mcg/day (SD 3.69)
- Folate (DFE): Mean 482.21 mcg/day (SD 256.04)

**Balance Outcome:**
- Failure time (BAXFTC41): Mean 7.01 seconds (SD 5.65)

### 2. Regression Results

**Main Effects Model:**
- Comorbidity burden: β = -0.032, p = 0.340 (NS)
- Vitamin B12: β = 0.039, p = 0.215 (NS)
- Folate: β = 0.015, p = 0.627 (NS)
- **Age: β = -0.020, p < 0.001** (significant - older age associated with worse balance)

**Interaction Model:**
- Comorbidity × B12 interaction: β = -0.012, p = 0.773 (NS)
- Comorbidity × Folate interaction: β = -0.023, p = 0.542 (NS)

### 3. Conclusions

1. **No significant association** between comorbidity burden and balance performance after adjusting for age, sex, BMI, and micronutrient intake.

2. **No significant associations** between dietary vitamin B12 or folate intake and balance performance.

3. **No significant interactions** between comorbidity burden and micronutrient intake, suggesting that micronutrient status does not modify the relationship between comorbidity burden and balance.

4. **Age was the only significant predictor**, with older age associated with shorter balance failure times (worse performance).

---

## Limitations

1. **Vitamin D unavailable:** Dietary vitamin D data was not available in NHANES cycle C and could not be included.

2. **Dietary intake only:** Supplement data was unavailable for cycle C; analyses were restricted to dietary micronutrient intake only.

3. **Cross-sectional design:** Cannot establish causal relationships or temporal ordering.

4. **Survivorship bias:** Sample includes only adults who were able to complete the balance exam, potentially excluding those with severe balance impairment.

5. **Measurement limitations:** Dietary recall may not accurately reflect long-term micronutrient status.

---

## Files Generated

- `tables/strobe_counts.csv`: Sample derivation counts
- `tables/regression_results.csv`: Full regression output
- `figures/balance_by_comorbidity.png`: Boxplots showing balance by comorbidity burden and B12 scatter
- `figures/interaction_plots.png`: Interaction visualization by comorbidity level

---

## Interpretation

The null findings suggest that in this sample of community-dwelling older adults, comorbidity burden and dietary micronutrient intake (B12, folate) were not independently or interactively associated with objective balance performance as measured by the modified Romberg test. The strong effect of age suggests that chronological aging may be the dominant factor in balance decline in this population, overshadowing the effects of comorbidity burden and dietary micronutrient intake within the observed ranges.

Future research should:
1. Include serum biomarkers of micronutrient status (not just dietary intake)
2. Examine additional cycles where vitamin D data is available
3. Consider longitudinal designs to assess change in balance over time
4. Explore whether specific comorbidities (rather than count) have differential effects

---

*Analysis completed: 2026-02-01*  
*Analyst: Elwood Research*
