"""
NHANES Analysis Script: Comorbidity Burden x Micronutrients and Balance
Cycle C (2003-2004) - Older Adults (60+ years)

Author: Elwood Research
Date: 2026-02-01
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.weightstats import DescrStatsW
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set paths
DATA_PATH = '/home/joshbot/NHANES_BOT/Processed Data/Data/'
OUTPUT_PATH = '/home/joshbot/NHANES_BOT/studies/meds-micronutrients-balance-2026-01-31/04-analysis/outputs/'

print("Loading NHANES Cycle C datasets...")

# Load datasets
demo = pd.read_csv(DATA_PATH + 'DEMO_C.csv')
bax = pd.read_csv(DATA_PATH + 'BAX_C.csv')
diq = pd.read_csv(DATA_PATH + 'DIQ_C.csv')
bpq = pd.read_csv(DATA_PATH + 'BPQ_C.csv')
dr1tot = pd.read_csv(DATA_PATH + 'DR1TOT_C.csv')
bmx = pd.read_csv(DATA_PATH + 'BMX_C.csv')

print(f"DEMO_C: {len(demo)} rows")
print(f"BAX_C: {len(bax)} rows")
print(f"DIQ_C: {len(diq)} rows")
print(f"BPQ_C: {len(bpq)} rows")
print(f"DR1TOT_C: {len(dr1tot)} rows")
print(f"BMX_C: {len(bmx)} rows")

# Check columns available
print("\nKey columns in BAX_C:", [c for c in bax.columns if 'BAX' in c or 'BAQ' in c][:15])

# Merge datasets
print("\nMerging datasets...")
df = demo.merge(bax, on='SEQN', how='inner')
df = df.merge(diq, on='SEQN', how='left')
df = df.merge(bpq, on='SEQN', how='left')
df = df.merge(dr1tot, on='SEQN', how='left')
df = df.merge(bmx, on='SEQN', how='left')
print(f"After merging: {len(df)} rows")

# Create STROBE tracking
strobe_counts = {
    'Initial merge': len(df)
}

# Age filter: 60+ years
print("\nApplying age filter (60+ years)...")
df = df[df['RIDAGEYR'] >= 60].copy()
strobe_counts['Age 60+'] = len(df)
print(f"After age filter: {len(df)} rows")

# Balance exam completion
print("\nApplying balance exam completion filter...")
# BAAEXSTS = 1 means complete
if 'BAAEXSTS' in df.columns:
    df = df[df['BAAEXSTS'] == 1].copy()
    strobe_counts['Balance exam complete'] = len(df)
    print(f"After balance exam completion: {len(df)} rows")

# Check balance outcome availability
print("\nBalance outcome variables available:")
balance_outcomes = ['BAXFTC11', 'BAXFTC21', 'BAXFTC31', 'BAXFTC41',
                    'BAXPFC11', 'BAXPFC21', 'BAXPFC31', 'BAXPFC41']
for col in balance_outcomes:
    if col in df.columns:
        non_missing = df[col].notna().sum()
        print(f"  {col}: {non_missing} non-missing")

# Filter for non-missing primary balance outcome
primary_outcome = 'BAXFTC41'  # Failure time, condition 4 (most challenging)
if primary_outcome in df.columns:
    print(f"\nFiltering for non-missing {primary_outcome}...")
    df = df[df[primary_outcome].notna()].copy()
    strobe_counts[f'Valid {primary_outcome}'] = len(df)
    print(f"After balance outcome filter: {len(df)} rows")

# Check survey weights
print("\nSurvey design variables:")
weight_vars = ['WTMEC2YR', 'SDMVPSU', 'SDMVSTRA']
for var in weight_vars:
    if var in df.columns:
        non_missing = df[var].notna().sum()
        print(f"  {var}: {non_missing} non-missing")
    else:
        print(f"  {var}: NOT FOUND")

# Filter for valid survey weights
if 'WTMEC2YR' in df.columns:
    df = df[df['WTMEC2YR'].notna()].copy()
    strobe_counts['Valid MEC weights'] = len(df)
    print(f"After weight filter: {len(df)} rows")

if 'SDMVPSU' in df.columns and 'SDMVSTRA' in df.columns:
    df = df[df['SDMVPSU'].notna() & df['SDMVSTRA'].notna()].copy()
    strobe_counts['Valid survey design'] = len(df)
    print(f"After survey design filter: {len(df)} rows")

# Create comorbidity burden variable
print("\nCreating comorbidity burden variable...")

# Diabetes: DIQ010 == 1 means "Yes" (ever told have diabetes)
if 'DIQ010' in df.columns:
    df['diabetes'] = (df['DIQ010'] == 1).astype(int)
    print(f"  Diabetes: {df['diabetes'].sum()} cases")
else:
    df['diabetes'] = 0
    print("  Diabetes variable not found")

# Hypertension: BPQ020 == 1 means "Yes" (ever told have hypertension)
if 'BPQ020' in df.columns:
    df['hypertension'] = (df['BPQ020'] == 1).astype(int)
    print(f"  Hypertension: {df['hypertension'].sum()} cases")
else:
    df['hypertension'] = 0
    print("  Hypertension variable not found")

# High cholesterol: BPQ080 == 1 means "Yes" (ever told have high cholesterol)
if 'BPQ080' in df.columns:
    df['high_chol'] = (df['BPQ080'] == 1).astype(int)
    print(f"  High cholesterol: {df['high_chol'].sum()} cases")
else:
    df['high_chol'] = 0
    print("  High cholesterol variable not found")

# Comorbidity count
df['comorbidity_count'] = df['diabetes'] + df['hypertension'] + df['high_chol']
df['comorbidity_cat'] = df['comorbidity_count'].apply(
    lambda x: '0' if x == 0 else ('1' if x == 1 else '2+')
)
print(f"\nComorbidity distribution:")
print(df['comorbidity_cat'].value_counts().sort_index())

# Filter for non-missing comorbidity data
non_missing_comorb = df[['DIQ010', 'BPQ020', 'BPQ080']].notna().all(axis=1)
df = df[non_missing_comorb].copy()
strobe_counts['Valid comorbidity data'] = len(df)
print(f"After comorbidity filter: {len(df)} rows")

# Check micronutrient availability
print("\nMicronutrient variables available:")
micronutrients = ['DR1TVB12', 'DR1TFDFE', 'DR1TKCAL']
for col in micronutrients:
    if col in df.columns:
        non_missing = df[col].notna().sum()
        print(f"  {col}: {non_missing} non-missing")
    else:
        print(f"  {col}: NOT FOUND")

# Filter for valid micronutrient data
if 'DR1TVB12' in df.columns and 'DR1TFDFE' in df.columns:
    df = df[df['DR1TVB12'].notna() & df['DR1TFDFE'].notna()].copy()
    strobe_counts['Valid micronutrient data'] = len(df)
    print(f"After micronutrient filter: {len(df)} rows")

# Apply outlier screening (|z| > 4)
print("\nApplying outlier screening (|z| > 4)...")
continuous_vars = ['RIDAGEYR', 'BMXBMI', 'DR1TVB12', 'DR1TFDFE', 'DR1TKCAL']
if primary_outcome in df.columns:
    continuous_vars.append(primary_outcome)

outlier_mask = pd.Series([True] * len(df), index=df.index)
for var in continuous_vars:
    if var in df.columns:
        z_scores = np.abs(stats.zscore(df[var], nan_policy='omit'))
        var_outliers = z_scores > 4
        n_outliers = var_outliers.sum()
        if n_outliers > 0:
            print(f"  {var}: {n_outliers} outliers removed")
            outlier_mask &= ~var_outliers

df = df[outlier_mask].copy()
strobe_counts['After outlier removal'] = len(df)
print(f"After outlier removal: {len(df)} rows")

# Save STROBE counts
strobe_df = pd.DataFrame(list(strobe_counts.items()), columns=['Step', 'N'])
strobe_df.to_csv(OUTPUT_PATH + 'tables/strobe_counts.csv', index=False)
print("\nSTROBE counts saved to strobe_counts.csv")

print(f"\nFinal analytic sample: {len(df)} participants")

# Basic descriptive statistics
print("\n" + "="*60)
print("DESCRIPTIVE STATISTICS")
print("="*60)

def weighted_describe(data, weights, varname):
    """Calculate weighted descriptive statistics"""
    mask = data[varname].notna() & weights.notna()
    x = data.loc[mask, varname].values
    w = weights.loc[mask].values
    if len(x) == 0:
        return {'mean': np.nan, 'std': np.nan, 'n': 0}
    
    d = DescrStatsW(x, weights=w)
    return {
        'mean': d.mean,
        'std': d.std,
        'n': len(x)
    }

# Use MEC weights for overall demographics, balance weights for balance outcomes
weights = df['WTMEC2YR'] if 'WTMEC2YR' in df.columns else pd.Series([1.0] * len(df))

# Age
age_stats = weighted_describe(df, weights, 'RIDAGEYR')
print(f"\nAge (years):")
print(f"  Mean (SD): {age_stats['mean']:.1f} ({age_stats['std']:.1f})")

# Sex
if 'RIAGENDR' in df.columns:
    sex_dist = df.groupby('RIAGENDR')['WTMEC2YR'].sum()
    sex_pct = 100 * sex_dist / sex_dist.sum()
    print(f"\nSex:")
    print(f"  Male: {sex_pct.get(1, 0):.1f}%")
    print(f"  Female: {sex_pct.get(2, 0):.1f}%")

# Race/ethnicity
if 'RIDRETH1' in df.columns:
    race_dist = df.groupby('RIDRETH1')['WTMEC2YR'].sum()
    race_pct = 100 * race_dist / race_dist.sum()
    print(f"\nRace/Ethnicity:")
    print(f"  Mexican American: {race_pct.get(1, 0):.1f}%")
    print(f"  Other Hispanic: {race_pct.get(2, 0):.1f}%")
    print(f"  Non-Hispanic White: {race_pct.get(3, 0):.1f}%")
    print(f"  Non-Hispanic Black: {race_pct.get(4, 0):.1f}%")
    print(f"  Other: {race_pct.get(5, 0):.1f}%")

# BMI
if 'BMXBMI' in df.columns:
    bmi_stats = weighted_describe(df, weights, 'BMXBMI')
    print(f"\nBMI (kg/m²):")
    print(f"  Mean (SD): {bmi_stats['mean']:.1f} ({bmi_stats['std']:.1f})")

# Comorbidity burden
print(f"\nComorbidity burden:")
comorb_dist = df.groupby('comorbidity_cat')['WTMEC2YR'].sum()
comorb_pct = 100 * comorb_dist / comorb_dist.sum()
for cat in ['0', '1', '2+']:
    print(f"  {cat} conditions: {comorb_pct.get(cat, 0):.1f}%")

# Micronutrients
print(f"\nMicronutrient intake (dietary):")
for var in ['DR1TVB12', 'DR1TFDFE']:
    if var in df.columns:
        stats_dict = weighted_describe(df, weights, var)
        print(f"  {var}: Mean {stats_dict['mean']:.2f} (SD {stats_dict['std']:.2f})")

# Balance outcomes
print(f"\nBalance outcomes:")
if primary_outcome in df.columns:
    outcome_stats = weighted_describe(df, weights, primary_outcome)
    print(f"  {primary_outcome} (seconds): Mean {outcome_stats['mean']:.2f} (SD {outcome_stats['std']:.2f})")

print("\n" + "="*60)
print("REGRESSION ANALYSES")
print("="*60)

# Prepare variables for regression
df['female'] = (df['RIAGENDR'] == 2).astype(int)

# Create dummy variables for race
if 'RIDRETH1' in df.columns:
    df['race_mex'] = (df['RIDRETH1'] == 1).astype(int)
    df['race_nhw'] = (df['RIDRETH1'] == 3).astype(int)
    df['race_nhb'] = (df['RIDRETH1'] == 4).astype(int)

# Standardize micronutrients for regression
df['b12_std'] = (df['DR1TVB12'] - df['DR1TVB12'].mean()) / df['DR1TVB12'].std()
df['folate_std'] = (df['DR1TFDFE'] - df['DR1TFDFE'].mean()) / df['DR1TFDFE'].std()

# Log-transform balance outcome if needed
if primary_outcome in df.columns:
    # Add small constant to avoid log(0)
    df['balance_log'] = np.log(df[primary_outcome] + 0.1)

# Simple OLS regression (unweighted for initial exploration)
print("\nMain effects model (unweighted OLS):")
print("-" * 40)

# Model 1: Main effects only
model1_formula = f"balance_log ~ comorbidity_count + b12_std + folate_std + RIDAGEYR + female + BMXBMI"
model1 = smf.ols(model1_formula, data=df).fit()
print(model1.summary().tables[1])

# Model 2: With interaction terms
print("\nInteraction model (unweighted OLS):")
print("-" * 40)
model2_formula = f"balance_log ~ comorbidity_count * b12_std + comorbidity_count * folate_std + RIDAGEYR + female + BMXBMI"
model2 = smf.ols(model2_formula, data=df).fit()
print(model2.summary().tables[1])

# Check for interaction significance
print("\nInteraction terms:")
print(f"  Comorbidity x B12: p = {model2.pvalues.get('comorbidity_count:b12_std', np.nan):.4f}")
print(f"  Comorbidity x Folate: p = {model2.pvalues.get('comorbidity_count:folate_std', np.nan):.4f}")

# Save model results
model_results = pd.DataFrame({
    'Variable': model2.params.index,
    'Coefficient': model2.params.values,
    'Std_Error': model2.bse.values,
    'P_value': model2.pvalues.values,
    'CI_lower': model2.conf_int()[0].values,
    'CI_upper': model2.conf_int()[1].values
})
model_results.to_csv(OUTPUT_PATH + 'tables/regression_results.csv', index=False)
print("\nRegression results saved to regression_results.csv")

# Create visualization
print("\n" + "="*60)
print("CREATING VISUALIZATIONS")
print("="*60)

# Plot 1: Comorbidity burden vs balance outcome
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Boxplot by comorbidity category
sns.boxplot(data=df, x='comorbidity_cat', y=primary_outcome, ax=axes[0])
axes[0].set_xlabel('Comorbidity Burden')
axes[0].set_ylabel('Balance Failure Time (seconds)')
axes[0].set_title('Balance Performance by Comorbidity Burden')

# Scatter: B12 vs balance, colored by comorbidity
scatter = axes[1].scatter(df['DR1TVB12'], df[primary_outcome], 
                          c=df['comorbidity_count'], cmap='viridis', alpha=0.5)
axes[1].set_xlabel('Vitamin B12 Intake (mcg)')
axes[1].set_ylabel('Balance Failure Time (seconds)')
axes[1].set_title('Balance vs B12 Intake by Comorbidity')
plt.colorbar(scatter, ax=axes[1], label='Comorbidity Count')

plt.tight_layout()
plt.savefig(OUTPUT_PATH + 'figures/balance_by_comorbidity.png', dpi=300)
print("Saved: balance_by_comorbidity.png")

# Plot 2: Interaction visualization
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Low vs high comorbidity for B12
comorb_low = df[df['comorbidity_count'] <= 1]
comorb_high = df[df['comorbidity_count'] >= 2]

axes[0].scatter(comorb_low['b12_std'], comorb_low['balance_log'], 
                alpha=0.5, label='Low comorbidity (0-1)')
axes[0].scatter(comorb_high['b12_std'], comorb_high['balance_log'], 
                alpha=0.5, label='High comorbidity (2+)')
# Add regression lines
z_low = np.polyfit(comorb_low['b12_std'], comorb_low['balance_log'], 1)
z_high = np.polyfit(comorb_high['b12_std'], comorb_high['balance_log'], 1)
x_line = np.linspace(df['b12_std'].min(), df['b12_std'].max(), 100)
axes[0].plot(x_line, np.poly1d(z_low)(x_line), '--', label='Low trend')
axes[0].plot(x_line, np.poly1d(z_high)(x_line), '--', label='High trend')
axes[0].set_xlabel('B12 Intake (standardized)')
axes[0].set_ylabel('Log Balance Time')
axes[0].set_title('B12-Balance Association by Comorbidity')
axes[0].legend()

# Low vs high comorbidity for Folate
axes[1].scatter(comorb_low['folate_std'], comorb_low['balance_log'], 
                alpha=0.5, label='Low comorbidity (0-1)')
axes[1].scatter(comorb_high['folate_std'], comorb_high['balance_log'], 
                alpha=0.5, label='High comorbidity (2+)')
z_low_f = np.polyfit(comorb_low['folate_std'], comorb_low['balance_log'], 1)
z_high_f = np.polyfit(comorb_high['folate_std'], comorb_high['balance_log'], 1)
x_line_f = np.linspace(df['folate_std'].min(), df['folate_std'].max(), 100)
axes[1].plot(x_line_f, np.poly1d(z_low_f)(x_line_f), '--', label='Low trend')
axes[1].plot(x_line_f, np.poly1d(z_high_f)(x_line_f), '--', label='High trend')
axes[1].set_xlabel('Folate Intake (standardized)')
axes[1].set_ylabel('Log Balance Time')
axes[1].set_title('Folate-Balance Association by Comorbidity')
axes[1].legend()

plt.tight_layout()
plt.savefig(OUTPUT_PATH + 'figures/interaction_plots.png', dpi=300)
print("Saved: interaction_plots.png")

# Summary of results
print("\n" + "="*60)
print("SUMMARY OF FINDINGS")
print("="*60)

print(f"\nAnalytic sample: {len(df)} participants aged 60+ years")
print(f"Balance outcome: {primary_outcome} (failure time in seconds)")
print(f"Comorbidity burden: {df['comorbidity_count'].mean():.2f} (SD {df['comorbidity_count'].std():.2f}) on average")

print("\nKey findings:")
print(f"1. Comorbidity burden main effect: β = {model2.params.get('comorbidity_count', 0):.3f}, p = {model2.pvalues.get('comorbidity_count', 1):.4f}")
print(f"2. B12 main effect: β = {model2.params.get('b12_std', 0):.3f}, p = {model2.pvalues.get('b12_std', 1):.4f}")
print(f"3. Folate main effect: β = {model2.params.get('folate_std', 0):.3f}, p = {model2.pvalues.get('folate_std', 1):.4f}")
print(f"4. Comorbidity x B12 interaction: β = {model2.params.get('comorbidity_count:b12_std', 0):.3f}, p = {model2.pvalues.get('comorbidity_count:b12_std', 1):.4f}")
print(f"5. Comorbidity x Folate interaction: β = {model2.params.get('comorbidity_count:folate_std', 0):.3f}, p = {model2.pvalues.get('comorbidity_count:folate_std', 1):.4f}")

print("\n" + "="*60)
print("Analysis complete!")
print("="*60)
