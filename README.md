# Did High-Spending Households Drive Growth? Spending Concentration, Reactivation, and Rank Decline

[한국어](README.ko.md)

Full case study: https://jiwoon-oh.github.io/portfolio/projects/dunnhumby-customer/case1/

## Question and hypotheses

When a retailer's sales increase, does that growth come from its already valuable customers buying more? Or from other households becoming more active? Using Dunnhumby transaction data, I **fixed the high-spending group at the beginning of the observation period** and tracked what happened to its spending later.

I evaluated two hypotheses:

- **H4-1:** Households in the initially defined top X% increase both their share of total sales and their absolute spending later on.
- **H4-2:** Initial high-spender status is associated with being a new or reactivated household.

The first hypothesis did not hold. **Spending and revenue share fell for the initial top 20%, while spending rose among the remaining 80%.** I tested how sensitive that result was to the baseline period, examined whether new and reactivated households accounted for the growth, and finally built a model to predict which initial top 20% households would lose their high-spending rank.

Here, *rank decline* is not the same as a customer completely stopping purchases. The modeling target was whether a household **remained in the top 20% later**, not whether it churned.

### Which "top 20%"?

The analysis uses three related but different populations. The figures differ slightly because the denominators differ, not because of an error.

| Name | Population | Households | Top 20% | Used for |
|---|---|---:|---|---|
| **Concentration sample** | Households with at least one transaction in weeks 17–26 | 2,272 | Top 20% of households on the Lorenz curve (interpolated, no hard cutoff) | Section 3: Lorenz curve, Gini, 55.4% |
| **H4-1 panel** | Households with transactions in both weeks 17–26 and weeks 90–99 | 2,095 | **419** (early spend ≥ 582.35) | Sections 5–9: group changes, tests A–D, 54.87% → 41.96% |
| **Wide panel** | All households with any transaction in weeks 17–99; early spend set to 0 if none | 2,492 | **499** (early spend ≥ 535.29) | Sections 10–13: new-or-reactivated cross-tab; section 14 onward: prediction model |

Of the 2,500 households in the data, 8 have no transaction in weeks 17–99 (seven existing, one reactivated). They are in the status counts of section 10 but not in the wide panel.

---

## 1. Define the high-spending group using early data only

Defining high spenders after observing the later period would create circular reasoning: it would select households based on the outcome and then report that the selected households spent more. I therefore fixed the group before measuring later outcomes.

I did not immediately assume an 80/20 Pareto split. First, I examined how long a baseline period was needed to rank households consistently and how concentrated spending actually was.

## 2. Choose the early-period length: rank stability

The stable observation interval covered **Weeks 17–99 (83 weeks)**. For a candidate baseline of N weeks, I ranked each household twice—once based on odd weeks and once based on even weeks—and calculated the **Spearman rank correlation**. Increasing N made the ranks more stable, though it also used more of the available period.

I limited the initial period to roughly **10–15%** of the stable interval, or **8–12 weeks**, to avoid defining the baseline using too much of the period I wanted to study.

- The `kneed` procedure identified **N = 10 weeks** as a possible elbow.
- Rank correlation at N = 10: **ρ = 0.697**.
- There was no sharp elbow, and the ranking still contained noise.

I chose **10 weeks** for the main analysis and planned checks using **8 and 12 weeks**.

![Spearman rank correlation between odd-week and even-week household ranks by baseline length: 0.40 at 2 weeks, 0.697 at the chosen 10 weeks (kneed elbow), 0.82 at 20 weeks](images/rank-stability.png)

## 3. Choose the top X%: spending concentration

Using the first 10 weeks, I sorted households by total spending and calculated cumulative revenue shares.

| Measure | Value |
|---|---:|
| Gini coefficient | **0.532** |
| Top 1% of households | 6.2% of sales |
| Top 10% | 36.1% of sales |
| Top 20% | **55.4% of sales** |
| Top 30% | 68.9% of sales |
| Elbow suggested by `kneed` | Top 18% |

The familiar claim that 20% of customers account for 80% of sales did not describe this dataset. Sales were concentrated, but not nearly that much. The cumulative curve declined smoothly without an obvious single cutoff.

Because the algorithm suggested **18%** and the more interpretable conventional cutoff was **20%**, I fixed the baseline high-spending group at the **top 20%**.

![Lorenz curve of household spending in weeks 17-26: the top 10%, 20% and 30% of households hold 36.1%, 55.4% and 68.9% of revenue, Gini = 0.532](images/lorenz-curve.png)

## 4. How I handled unusual transactions

An IQR screen classified around **7.34%** of `SALES_VALUE` observations as outliers. Spending data tend to be right-skewed: many small transactions coexist with a smaller number of large baskets.

Because the research question concerned high-spending households, automatically deleting large transactions could remove the signal I was trying to examine. I kept the records and used nonparametric tests where normality was not a credible assumption.

## 5. The first result contradicted the hypothesis

I calculated spending changes between the early and late periods for each household, then compared the two groups fixed at baseline.

| Initial group | Mean spending change (late − early) |
|---|---:|
| Top 20% | **−111.49** |
| Remaining 80% | **+102.74** |

The high-spending group did not expand its spending. It contracted, while the rest grew.

However, high initial performers often move closer to the average on a later measurement. Before calling this a meaningful pattern, I checked whether the result changed when I selected a different number of baseline weeks.

## 6. Sensitivity: 8, 10, and 12 baseline weeks

| Baseline | Mean change, remaining 80% | Mean change, top 20% |
|---|---:|---:|
| 8 weeks | +92.42 | −97.16 |
| **10 weeks** | **+102.74** | **−111.49** |
| 12 weeks | +117.85 | −120.21 |

- The directions remained the same with all three baseline windows.
- Jaccard overlap between the high-spender lists was **0.76–0.86**, suggesting a fairly stable group definition.

This finding was not solely due to picking exactly 10 weeks. Still, changing the window does **not completely rule out regression to the mean**. It is a sensitivity check, not a full identification strategy.

![Box plots of each household's spending change (late minus early): initial top 20% median −131.45 and mean −111.49 (n = 419); remaining 80% median +36.49 and mean +102.74 (n = 1,676)](images/spend-change-box.png)

## 7. Distribution assumptions

- **Shapiro–Wilk:** normality was rejected for both the top 20% and remaining 80%.
- **Levene:** equal variances were rejected; variance in the top 20% was more than **three times** as large.

I therefore used rank-based tests to compare within-group and between-group changes.

## 8. Test H4-1: absolute spending versus sales share

I treated absolute spending and the group's share of total revenue as separate outcomes. The three main household-level tests used a Bonferroni-corrected threshold of `α = 0.05/3 ≈ 0.0167`.

### Test A — spending within the initial top 20% (Wilcoxon)

- **p = 0.00002**
- Effect size **r = −0.209**, in the negative direction
- Median spending change **−131.45**
- 95% confidence interval entirely below zero

Spending in the initial high-spending group fell significantly.

### Test B — spending within the remaining 80% (Wilcoxon)

- **p = 8.8 × 10⁻³¹**
- Median spending change **+36.49**
- 95% confidence interval **[23.9, 49.8]**

Spending among the remaining households increased significantly.

### Test C — difference in changes between the two groups (Mann–Whitney U)

- **p = 3.3 × 10⁻²⁰**
- Effect size **r = 0.290**
- Common-language effect size **0.355**
- 95% interval for the group difference **[−229.3, −116.0]**

Changes in the initially high-spending group tended to be lower. The common-language effect size must be read with the direction of the pairwise comparison; a value near 0.5 indicates little separation between groups.

### Test D — change in the high-spending group's revenue share

A revenue share is a group-level ratio, not a separate observation for every household. I used **5,000 bootstrap resamples** (seed 42) to quantify uncertainty in its change. These shares are computed on the H4-1 panel (419 of 2,095 households), so the early share (54.87%) is slightly below the 55.4% concentration in section 3, which uses all 2,272 households active in weeks 17–26.

| Period | Share of total sales from initial top 20% |
|---|---:|
| Early | **54.87%** |
| Late | **41.96%** |
| Change | **−12.91 percentage points (pp)** |
| Bootstrap 95% CI | **[−14.81, −11.07] pp** |

The interval excludes zero. Both the group's total revenue share and household-level spending declined.

![Revenue share of the initial top 20% fell from 54.87% to 41.96% (−12.91 pp); the 95% bootstrap interval runs from −14.81 to −11.07](images/share-bootstrap.png)

## 9. Conclusion for H4-1

The hypothesis that initial top spenders drove subsequent revenue growth was **not supported**. Their spending and share of revenue both fell, while the remaining households increased spending.

I describe this as a pattern of **reduced concentration or convergence in spending**. The same evidence does not tell us whether high spenders fully stopped shopping, gradually reduced spending, or were simply outpaced by other households. That question motivated the next analysis.

## 10. Define new, reactivated, and existing households

I wanted to know whether spending growth among the remaining 80% primarily came from customers entering or returning to the retailer.

- **New:** first recorded purchase occurred after the stable period began in Week 17.
- **Reactivated:** not new, but had at least one purchase gap of **13 weeks (91 days)** or more.
- **Existing:** neither of the above.

I checked that these categories were mutually exclusive and that they covered all 2,500 households. The 2×2 table below covers the 2,492 households with any transaction in weeks 17–99; the other eight (seven existing, one reactivated) only shopped before week 17 or after week 99.

## 11. H4-2: contingency table and chi-square test

| Household status | Count |
|---|---:|
| Existing | 1,565 |
| Reactivated | 726 |
| New | 209 |
| **Total** | **2,500** |

| Baseline tier | Existing | New or reactivated |
|---|---:|---:|
| Remaining 80% | 1,127 (56.5%) | **866 (43.5%)** |
| Top 20% | 431 (86.4%) | **68 (13.6%)** |

- Minimum expected cell count: **187**, meeting the usual chi-square approximation requirement.
- Chi-square p-value: **1.5 × 10⁻³⁴**.
- **Cramér's V = 0.246**.

New-or-reactivated status was clearly associated with baseline spending rank. Yet this association alone did not establish that newly active households caused most of the sales growth.

## 12. H4-2: break down the actual spending increase

I calculated how much of the positive spending change among the remaining 80% came from existing versus new or reactivated households.

| Status within remaining 80% | Share of households | Share of spending increase | Median change |
|---|---:|---:|---:|
| Existing | 56.5% | **70.0%** | **51.78** |
| New or reactivated | 43.5% | **30.0%** | **10.26** |

New or reactivated households represented 43.5% of the group but contributed only 30% of its observed spending increase. Existing households accounted for the remaining 70%.

![Share of households against share of the net spending increase: existing 56.5% of households and 70.0% of the increase, new or reactivated 43.5% of households and 30.0% of the increase](images/contribution-split.png)

Comparing the distributions of change within the remaining 80%:

- Mann–Whitney U **p = 0.000928**, significant after Bonferroni correction
- Rank-biserial effect size **0.086**, small
- Common-language effect size **0.457**, close to 0.5
- Comparison included **1,993 households**

The difference was detectable statistically, but its effect size was small. This is a useful example of why **statistical significance and practical importance are different questions**.

![Left: existing households contributed 70.0% and new or reactivated households 30.0% of the net spending increase in the remaining 80%. Right: median change per household +51.78 for existing and +10.26 for new or reactivated households](images/cohort-contribution.png)

## 13. H4-2 conclusion

New-or-reactivated status and high-spender status were associated, but **existing households accounted for 70% of the spending growth** within the remaining 80%. New or reactivated households did not dominate the observed growth.

Here, 'contribution' is an **accounting decomposition of observed spending changes**, not a causal estimate of the effect of acquiring or reactivating customers.

---

## 14. Follow-up: predict decline from the top 20%

The statistical analysis described what happened. I then built a small predictive exercise to identify households likely to fall out of the high-spending group.

- **Population:** 499 households in the top 20% during **Weeks 17–26**.
- **Outcome:** top-20% status during **Weeks 90–99**; remain (0) or fall out (1).
- **Models:** interpretable logistic regression and random forest with SHAP.
- **Validation:** **five-fold StratifiedKFold**, chosen because the sample was small.
- **Metrics:** PR-AUC and recall, with accuracy as supporting information.

A household dropping out of the top spending quintile is not necessarily an inactive or churned customer. That distinction matters before attaching business actions to the model output.

## 15. Explore additional source tables

| Table | Checks and decisions |
|---|---|
| `hh_demographic` | Missing for **180 of 499 households (36.1%)**. Demographic coverage: 32.1% overall, 63.9% among initial top spenders |
| `causal_data` | No missing values or duplicates. DISPLAY/MAILER code 0 treated as no exposure |
| `product` | Verified one-to-one mapping for `product_id` |
| `coupon_redempt` | Activity began after DAY 225; no overlap with early feature period (DAY 111–180), so excluded |
| `campaign_table`, `campaign_desc` | No campaigns in the early feature window, so excluded from baseline features |

I avoided using campaign history that would only become available after the prediction point.

## 16. Feature engineering

1. **Demographic missingness:** kept a distinct missing-data category for the 180 households. The original category `Unknown` is different from an entirely absent demographic record.
2. **Outcome balance:** **44.7%** dropped out of the top 20% and **55.3%** remained; there was no severe class imbalance.
3. **Quantity anomalies:** among the 499 households, the average `QUANTITY` per basket in the early window reached **9,021** at most (for example **7,660** for one household), and a single transaction line reached **41,686** units, possibly because quantity units differ across products (weight- or volume-based items). I replaced the quantity-based `avg_qty_per_basket` with **`avg_items_per_basket`**, based on distinct items.
4. **Promotion exposure:** the raw `exposure_ratio` was higher among households that later fell out of the top 20%, so I checked its conditional direction in the regression model. After adjusting for the other variables the association disappeared (section 20).

## 17. Feature encoding

- Standardized **eight features** for logistic regression: the five numeric ones (`sales_early`, `n_baskets`, `avg_items_per_basket`, `category_diversity`, `exposure_ratio`) and three ordinal ones (`AGE_DESC`, `INCOME_DESC`, `HOUSEHOLD_SIZE_DESC`). Binary variables (`has_demo`, one-hot dummies) were left unscaled.
- Represented demographic-data availability using a separate binary variable, **`has_demo`**.
- Encoded **four ordinal features** while retaining their order; missing values were handled with reference to observed modes. `KID_CATEGORY_DESC` was dropped at the VIF step (section 18), leaving three.
- One-hot encoded **two nominal variables**, preserving `HH_COMP_DESC = Unknown` as its own category.

## 18. Multicollinearity and feature selection

| Feature | VIF before removal |
|---|---:|
| `KID_CATEGORY_DESC_encoded` | **26.68** |
| `HOUSEHOLD_SIZE_DESC_encoded` | **26.49** |

Household size and children category carried overlapping information. I removed `KID_CATEGORY_DESC_encoded`, after which all VIFs were below 5. The VIF for `HOUSEHOLD_SIZE_DESC_encoded` fell to **4.8**. The model ended up with **18 features**.

## 19. Train/test evaluation design

With only **499 households**, I used **five-fold stratified cross-validation** instead of reporting a single random split. The outcome balance (44.7% positive, 55.3% negative) was maintained across folds.

The model should use **one row per household** to prevent data from the same household entering training and validation separately. Even properly performed cross-validation does not guarantee that results will transfer to another period or retailer.

## 20. Model 1: logistic regression

| Measure | Result |
|---|---:|
| Random-classifier reference PR-AUC | approx. **0.447** (positive prevalence) |
| Logistic regression PR-AUC | **0.685** |
| Actual households leaving the top 20% | 223 |
| False negatives | **89, or roughly 40%** of actual declines |

The model improved on random ranking, but it still missed roughly two out of five households that later fell out of the top 20%.

![Logistic regression confusion matrix: 207 true negatives, 69 false positives, 89 false negatives and 134 true positives](images/confusion-matrix.png)

![Cross-validation PR-AUC and recall by fold: mean PR-AUC 0.685 (SD 0.049), mean recall 0.601 (SD 0.084)](images/cv-folds.png)

![Precision–recall curve of the logistic regression, above the stratified dummy classifier at 0.433; at threshold 0.5 recall is 0.601 and precision 0.660](images/pr-curve.png)

### Odds-ratio interpretation

Odds ratios for numeric features are per one standard deviation (SD). Intervals are 95% percentile bootstrap intervals (1,000 household resamples, seed 42) for the penalized model used for prediction; p-values come from an unpenalized refit of the same model. An interval that excludes 1 means an association was found; an interval that includes 1 means none was established.

| Variable | Unit | Odds ratio | 95% CI | p | Reading |
|---|---|---:|---|---:|---|
| `has_demo` | demographic record present vs absent | 0.32 | 0.19–0.51 | 5 × 10⁻⁵ | Association found (the clearest) |
| `sales_early` | per 1 SD (≈ $429) | 0.64 | 0.42–0.85 | 0.009 | Association found |
| Income band (`INCOME_DESC`) | per 1 SD (≈ 2.0 of 12 ordered bands) | 0.73 | 0.55–0.92 | 0.007 | Association found |
| `category_diversity` | per 1 SD (≈ 20.6 categories) | 0.74 | 0.55–1.00 | 0.047 | Association found (borderline: upper bound 0.998) |
| `n_baskets` | per 1 SD (≈ 23.1 baskets) | 1.29 | 0.91–1.87 | 0.07 | Not established |
| `exposure_ratio` | per 1 SD (≈ 0.079) | 0.96 | 0.78–1.18 | 0.71 | Not established |

- **`has_demo`:** households with demographic records were less likely to leave the top 20%. It might proxy customer engagement; it is not proof that having a demographic record prevents rank decline.
- **Income band:** this is an ordered code, not a category compared with a reference level: 12 ordered bands from Under 15K (0) to 250K+ (11). The odds ratio compares households one SD (about two bands) apart, and higher-income households were less likely to drop out. The 180 households without a demographic record were assigned the most common band (50–74K); `has_demo` identifies them.
- **`sales_early` and `category_diversity`:** higher starting spending and broader purchases were associated with a lower probability of falling out. The `category_diversity` interval only just excludes 1.
- **`exposure_ratio` and `n_baskets`:** no association was established after accounting for the other variables. The point estimate for visit frequency (1.29) leans toward higher risk, but its interval includes 1 and should not be read as a risk factor.
- **Housing categories:** some cells are very small, so I do not interpret their estimates.

All odds ratios describe associations conditional on included variables, not causal responses to changing a feature.

![Forest plot of odds ratios with 95% bootstrap intervals on a log scale: demographic record present 0.32, baseline spend 0.64, income band 0.73 and category diversity 0.74 have intervals that exclude 1; visit frequency 1.29 and promotion exposure 0.96 do not](images/odds-ratios.png)

## 21. Model 2: random forest and SHAP

The random forest had noticeably lower recall than logistic regression (0.529 vs 0.601 in cross-validation). A dataset with only 499 households may not give a more flexible tree model enough observations to learn reliable nonlinear patterns. For this setting, I preferred **logistic regression as the main predictive model**.

Top SHAP-ranked features were:

1. `has_demo`
2. `sales_early`
3. `category_diversity`
4. `INCOME_DESC`
5. `avg_items_per_basket`

The most important predictors overlapped considerably with the logistic results. SHAP also showed nonlinear patterns. For `sales_early`, the mean SHAP value fell from +0.091 in the lowest decile to −0.082 in the ninth and −0.084 in the top decile: above roughly 1,250 in early spend, more spending no longer moved the prediction. For `category_diversity` the pattern was different: the mean SHAP value was flat (about +0.03) below roughly 77 categories and kept falling at the high end (−0.061 in the top decile), so there was no saturation at the top.

That is interesting for customer prioritization, but it does not prove that targeting households near those thresholds produces the greatest campaign lift.

![Random forest SHAP importance: demographic record present 0.082, baseline spend 0.049, category diversity 0.029, income band 0.024 and items per basket 0.017 are the top five](images/shap-importance.png)

![Mean SHAP value by decile of the feature: baseline spend falls from +0.091 in the lowest decile to −0.082 in the ninth and −0.084 in the tenth, flat above 1,246; category diversity keeps falling to −0.061 in the top decile](images/shap-saturation.png)

## 22. Why false negatives and false positives have different costs

- **False negative (FN):** a household likely to lose top-spender status is predicted to remain; the retailer could miss an opportunity to contact it.
- **False positive (FP):** a household that would remain is flagged as at risk, potentially generating unnecessary marketing cost.

If missing an at-risk valuable household is more expensive than sending an extra retention message, recall should carry more weight. But campaign costs and incremental treatment effects were not available, so I did not claim to have identified the profit-optimal classification threshold.

## 23. Additional validation

- **Permutation test:** `p = 0.001` (1,000 permutations, the smallest attainable value), suggesting performance beyond randomly permuted outcomes.
- **Dummy classifier:** the logistic model exceeded a stratified dummy classifier (PR-AUC 0.685 vs 0.433).
- **Learning curve:** validation PR-AUC rose from 0.652 with 119 training households to between 0.680 and 0.687 over the last five training sizes, and the training and validation scores converged (0.682 vs 0.685 at the full size). There is no sign of a large train/validation gap.

The model appears to have learned a real predictive association in this sample. The flat validation curve does not suggest that many more households would change the picture for this model, and performance on a genuinely future period or a different dataset remains untested.

## Summary and next questions

| Question | Answer from this analysis |
|---|---|
| Did the initial top 20% drive growth? | **No.** Their spending and revenue share fell. |
| Where did growth in the other 80% come from? | **70%** of observed increases came from existing households; **30%** from new or reactivated households. |
| Is new-or-reactivated status associated with baseline spending rank? | Yes; **Cramér's V = 0.246**. |
| Can a later fall out of the top 20% be predicted? | Partly; logistic PR-AUC **0.685**, but substantial false negatives remain. |

For a practical retention strategy, I would look beyond the highest historical spenders and examine **basket frequency, category diversity, and growth among existing medium- and lower-spending households**. Before introducing interventions, I would also distinguish rank decline from the top 20% from actual purchase inactivity and measure campaign response relative to an appropriate control.

## How to run

```
pip install -r requirements.txt
pip install jupyter
```

The pinned versions are those of the Python 3.11 environment the notebooks were run in.

1. Download the Dunnhumby *The Complete Journey* CSVs into `data/` (see `data/README.md`; `transaction_data`, `hh_demographic`, `product`, `causal_data`, `campaign_table`, `campaign_desc`, `coupon`, `coupon_redempt`). They are git-ignored.
2. Run the notebooks from the repository root in this order. `config.py` sets all paths and `SEED = 42`.

   ```
   python -m nbconvert --to notebook --execute --inplace <notebook>.ipynb
   ```

   | # | Notebook | Writes |
   |---|---|---|
   | 1 | `dunnhumby_data_overview` | `outputs/`: weekly revenue and trend fit |
   | 2 | `gap_analysis` | — |
   | 3 | `h4_transaction_eda` | `outputs/`: rank stability, Lorenz, Gini, concentration, household counts |
   | 4 | `h4_normality_variance` | `outputs/`: panel summary, normality and Levene tests, sensitivity, Jaccard |
   | 5 | `h4_nonparametric_tests` | `outputs/`: tests A–C, share bootstrap (test D), Bonferroni table |
   | 6 | `h4_2_crosstab` | `outputs/`: status counts, cross-tabs, chi-square, contribution, excluded households |
   | 7 | `ml_tables_eda` | `outputs/`: source-table checks and facts |
   | 8 | `h4_ml_feature_engineering` | `outputs/`: label summary; feature table in `outputs/intermediate/` |
   | 9 | `h4_ml_encoding` | `outputs/`: VIF, encoding summary; encoded table in `outputs/intermediate/` |
   | 10 | `h4_ml_model_training` | `outputs/`: CV metrics, confusion matrix, odds ratios, baselines, thresholds |
   | 11 | `h4_ml_rf_shap` | `outputs/`: random forest CV, SHAP summary and saturation deciles |
   | 12 | `h4_figures` | `images/`: every figure, drawn from `outputs/` (set `TRANSPARENT = True` for transparent versions) |

   Notebooks 3–6 are independent of each other; 8 → 9 → 10 → 11 must run in order; 12 runs last.
3. Every number in this README comes from a CSV in `outputs/`. Household-level intermediate files go to `outputs/intermediate/` and are not committed. Running the notebooks twice from a fresh kernel produces identical CSVs.

## Limitations

- Rank-based group selection can introduce regression-to-the-mean effects even with the baseline period fixed and sensitivity-tested.
- Spending comparisons describe observed change, not its cause.
- New or reactivated labels depend on the available transaction history; earlier activity may not be observed.
- Demographic-data availability may be a proxy for unobserved customer engagement.
- The predictive model uses **499 households**, limiting the precision of reported performance.
- The target is **retention of high-spending rank**, not direct customer churn or lifetime value.

**Bottom line:** The initial top 20% did not account for the later spending growth. Most of the increase among other households came from existing customers, not the new or reactivated group. Predicting high-spender rank decline was possible to a degree, but those predictions should not be presented as churn or causal marketing effects.
