# Manuscript: Comorbidity Burden, Micronutrient Intake, and Balance Performance in Older Adults

## Overview

This directory contains the LaTeX manuscript and compiled PDF for the study examining associations between comorbidity burden, dietary micronutrient intake (vitamin B12, folate), and balance performance in older adults using NHANES 2003-2004 data.

## Files

- **manuscript.tex** - LaTeX source file containing the complete manuscript
- **manuscript.pdf** - Compiled PDF output (15 pages)
- **README.md** - This file

## Study Summary

- **Title:** Comorbidity Burden, Micronutrient Intake, and Balance Performance in Older Adults: NHANES 2003-2004
- **Authors:** Elwood Research
- **Study Design:** Cross-sectional analysis
- **Population:** 788 adults aged 60+ years
- **Data Source:** NHANES Cycle C (2003-2004)
- **Key Finding:** No significant associations between comorbidity burden or dietary micronutrients (B12, folate) and balance; age was the only significant predictor

## Manuscript Structure

1. **Title Page** - Study title and author information
2. **Abstract** (~280 words) - Background, methods, results, and conclusions
3. **Introduction** - Literature review on comorbidity, micronutrients, and balance
4. **Methods** - Detailed study design, population, variables, and statistical analysis
5. **Results** - Sample characteristics, regression results, and visual patterns
6. **Discussion** - Interpretation of findings, strengths, limitations, and implications
7. **Conclusion** - Summary of key takeaways and recommendations
8. **References** - 17 citations using natbib numbered format

## Key Tables and Figures

- **Table 1:** Sample characteristics (weighted)
- **Table 2:** Survey-weighted linear regression results
- **Figure 1:** STROBE flow diagram showing sample derivation
- **Figure 2:** Interaction plots for comorbidity × micronutrient effects

## Compilation Details

The manuscript was compiled using:
- **Engine:** pdfLaTeX (TinyTeX)
- **Bibliography:** BibTeX with unsrtnat style
- **Passes:** 4 pdflatex runs with 1 bibtex run
- **Output:** 15-page PDF with numbered citations

## Dependencies

Required LaTeX packages:
- inputenc, fontenc, geometry
- setspace, graphicx, booktabs
- amsmath, caption, subcaption
- array, longtable, url
- natbib (numbered citations)
- hyperref (loaded last with colorlinks)
- multirow, float

## References

All citations are included via `../01-literature/references.bib` using the external bibliography file.

---

*Manuscript created: February 2026*  
*Analysis completed: February 1, 2026*  
*Analyst: Elwood Research*
