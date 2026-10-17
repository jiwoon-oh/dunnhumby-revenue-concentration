# Did High-Spending Households Drive Growth? Spending Concentration, Reactivation, and Rank Decline

[한국어](README.ko.md)

## Question and hypotheses

When a retailer's sales increase, does that growth come from its already valuable customers buying more? Or from other households becoming more active? Using Dunnhumby transaction data, I **fixed the high-spending group at the beginning of the observation period** and tracked what happened to its spending later.

I evaluated two hypotheses:

- **H4-1:** Households in the initially defined top X% increase both their share of total sales and their absolute spending later on.
- **H4-2:** Initial high-spender status is associated with being a new or reactivated household.

The first hypothesis did not hold. **Spending and revenue share fell for the initial top 20%, while spending rose among the remaining 80%.** I tested how sensitive that result was to the baseline period, examined whether new and reactivated households accounted for the growth, and finally built a model to predict which initial top-20% households would lose their high-spending rank.

Here, *rank decline* is not the same as a customer completely stopping purchases. The modeling target was whether a household **remained in the top 20% later**, not whether it churned.

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

![Early-period rank stability — original Korean chart](../src/image.png)

## 3. Choose the top X%: spending concentration

Using the first 10 weeks, I sorted households by total spending and calculated cumulative revenue shares.

| Measure | Value |
|---|---:|
| Gini coefficient | **0.532** |
| Top 1% of households | 6.1% of sales |
| Top 10% | 36.1% of sales |
| Top 20% | **55.4% of sales** |
| Top 30% | 68.9% of sales |
| Elbow suggested by `kneed` | Top 18% |

The familiar claim that 20% of customers account for 80% of sales did not describe this dataset. Sales were concentrated, but not nearly that much. The cumulative curve declined smoothly without an obvious single cutoff.

Because the algorithm suggested **18%** and the more interpretable conventional cutoff was **20%**, I fixed the baseline high-spending group at the **top 20%**.

![Cumulative spending concentration — original Korean chart](../src/image-1.png)

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

![Spending changes by initial group — original Korean chart](../src/image-4.png)

## 7. Distribution assumptions

- **Shapiro–Wilk:** normality was rejected for both the top 20% and remaining 80%.
- **Levene:** equal variances were rejected; variance in the top 20% was more than **three times** as large.

I therefore used rank-based tests to compare within-group and between-group changes.

## 8. Test H4-1: absolute spending versus sales share

I treated absolute spending and the group's share of total revenue as separate outcomes. The three main household-level tests used a Bonferroni-adjusted threshold of `α = 0.05/3 ≈ 0.0167`.

### Test A — spending within the initial top 20% (Wilcoxon)

- **p = 0.00002**
- Effect size **r = −0.209**, in the negative direction
- Median spending change **−131.45**
- 95% confidence interval entirely below zero

Spending in the initial high-spending group fell significantly.

### Test B — spending within the remaining 80% (Wilcoxon)

- **p ≈ 0.0000** (rounded output, not literally a zero probability)
- Median spending change **+36.49**
- 95% confidence interval **[24.3, 50.1]**

Spending among the remaining households increased significantly.

### Test C — difference in changes between the two groups (Mann–Whitney U)

- **p ≈ 0.0000**
- Effect size **r = 0.290**
- Common-language effect size **0.355**
- 95% interval for the group difference **[−227.7, −116.0]**

Changes in the initially high-spending group tended to be lower. The common-language effect size must be read with the direction of the pairwise comparison; a value near 0.5 indicates little separation between groups.

### Test D — change in the high-spending group's revenue share

A revenue share is a group-level ratio, not a separate observation for every household. I used **5,000 bootstrap resamples** to quantify uncertainty in its change.

| Period | Share of total sales from initial top 20% |
|---|---:|
| Early | **54.87%** |
| Late | **41.96%** |
| Change | **−12.91 percentage points** |
| Bootstrap 95% CI | **[−14.74, −11.09] percentage points** |

The interval excludes zero. Both the group's total revenue share and household-level spending declined.

## 9. Conclusion for H4-1

The hypothesis that initial top spenders drove subsequent revenue growth was **not supported**. Their spending and share of revenue both fell, while the remaining households increased spending.

I describe this as a pattern of **reduced concentration or convergence in spending**. The same evidence does not tell us whether high spenders fully stopped shopping, gradually reduced spending, or were simply outpaced by other households. That question motivated the next analysis.

## 10. Define new, reactivated, and existing households

I wanted to know whether spending growth among the remaining 80% primarily came from customers entering or returning to the retailer.

- **New:** first recorded purchase occurred after the stable period began in Week 17.
- **Reactivated:** not new, but had at least one purchase gap of **13 weeks (91 days)** or more.
- **Existing:** neither of the above.

I checked that these categories were mutually exclusive and that they covered all 2,500 households.

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
- Chi-square p-value: extremely small (`≈ 0.000000` when rounded).
- **Cramér's V = 0.246**.

New/reactivated status was clearly associated with baseline spending rank. Yet this association alone did not establish that newly active households caused most of the sales growth.

## 12. H4-2: break down the actual spending increase

I calculated how much of the positive spending change among the remaining 80% came from existing versus new/reactivated households.

| Status within remaining 80% | Share of households | Share of spending increase | Median change |
|---|---:|---:|---:|
| Existing | 56.5% | **70.0%** | **51.78** |
| New/reactivated | 43.5% | **30.0%** | **10.26** |

New/reactivated households represented 43.5% of the group but contributed only 30% of its observed spending increase. Existing households accounted for the remaining 70%.

Comparing the distributions of change within the remaining 80%:

- Mann–Whitney U **p = 0.000928**, significant after Bonferroni adjustment
- Rank-biserial effect size **0.086**, small
- Common-language effect size **0.457**, close to 0.5
- Comparison included **1,993 households**

The difference was detectable statistically, but its effect size was small. This is a useful example of why **statistical significance and practical importance are different questions**.

![Spending-growth contributions by customer status — original Korean chart](../src/image-6.png)

## 13. H4-2 conclusion

New/reactivated status and high-spender status were associated, but **existing households accounted for 70% of the spending growth** within the remaining 80%. New/reactivated households did not dominate the observed growth.

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

1. **Demographic missingness:** kept a distinct missing-data category for the 180 households. The original category `Unknown` is different from an entirely absent survey record.
2. **Outcome balance:** **44.7%** dropped out of the top tier and **55.3%** remained; there was no severe class imbalance.
3. **Quantity anomalies:** `QUANTITY` sums of **7,660** and **2,559** appeared for some households, possibly because quantity units differed across products. I replaced quantity-sum-based `avg_qty_per_basket` with **`avg_items_per_basket`**, based on distinct items.
4. **Promotion exposure:** the raw `exposure_ratio` was higher among households that later fell out of the top tier, so I checked its conditional direction in the regression model.

## 17. Feature encoding

- Standardized **five numeric features** for logistic regression: `sales_early`, `n_baskets`, `avg_items_per_basket`, `category_diversity`, `exposure_ratio`.
- Represented demographic-data availability using a separate binary variable, **`has_demo`**.
- Encoded **four ordinal features** while retaining their order; missing values were handled with reference to observed modes.
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
| Logistic regression PR-AUC | **0.674** |
| Actual households leaving the top tier | 223 |
| False negatives | **86, or roughly 39%** of actual declines |

The model improved on random ranking, but it still missed roughly two out of five households that later fell out of the top spending group.

![Logistic regression model evaluation — original Korean chart](../src/image-9.png)

### Odds-ratio interpretation

- **`has_demo` (OR ≈ 0.35):** households with demographic records were less likely to leave the top spending group. This might proxy customer engagement; it is not proof that completing a survey prevents rank decline.
- **`sales_early` and `category_diversity`:** higher starting spending and broader purchases were associated with a lower probability of falling out.
- **`exposure_ratio`:** unlike the raw group comparison, its conditional coefficient leaned in a protective direction after accounting for other variables.
- **`n_baskets`:** greater visit frequency conditional on spending could signal smaller baskets and a less stable high-spending rank.
- **Some housing categories:** coefficient estimates may be unstable because of limited samples.

All odds ratios describe associations conditional on included variables, not causal responses to changing a feature.

## 21. Model 2: random forest and SHAP

The random forest had noticeably lower recall than logistic regression. A dataset with only 499 households may not give a more flexible tree model enough observations to learn reliable nonlinear patterns. For this setting, I preferred **logistic regression as the main predictive model**.

Top SHAP-ranked features were:

1. `has_demo`
2. `sales_early`
3. `category_diversity`
4. `INCOME_DESC`
5. `avg_items_per_basket`

The most important predictors overlapped considerably with the logistic results. SHAP also suggested saturation: beyond some level, greater initial spending or category diversity did not correspond to equally large additional changes in the model prediction.

That is interesting for customer prioritization, but it does not prove that targeting households near those thresholds produces the greatest campaign lift.

![Feature importance — original Korean chart](../src/image-14.png)

## 22. Why false negatives and false positives have different costs

- **False negative (FN):** a household likely to lose top-spender status is predicted to remain; the retailer could miss an opportunity to contact it.
- **False positive (FP):** a household that would remain is flagged as at risk, potentially generating unnecessary marketing cost.

If missing an at-risk valuable household is more expensive than sending an extra retention message, recall should carry more weight. But campaign costs and incremental treatment effects were not available, so I did not claim to have identified the profit-optimal classification threshold.

## 23. Additional validation

- **Permutation test:** `p = 0.001`, suggesting performance beyond randomly permuted outcomes.
- **Dummy classifier:** the logistic model exceeded a simple baseline.
- **Learning curve:** no clear large train/validation gap, but performance had not fully plateaued.

The model appears to have learned a real predictive association in this sample. Still, **more observations may improve it**, and performance on a genuinely future period or a different dataset remains untested.

## Summary and next questions

| Question | Answer from this analysis |
|---|---|
| Did the initial top 20% drive growth? | **No.** Their spending and revenue share fell. |
| Where did growth in the other 80% come from? | **70%** of observed increases came from existing households; **30%** from new/reactivated households. |
| Is new/reactivated status associated with spending tier? | Yes; **Cramér's V = 0.246**. |
| Can later top-tier decline be predicted? | Partly; logistic PR-AUC **0.674**, but substantial false negatives remain. |

For a practical retention strategy, I would look beyond the highest historical spenders and examine **basket frequency, category diversity, and growth among existing mid- and lower-spending households**. Before introducing interventions, I would also distinguish top-tier rank decline from actual purchase inactivity and measure campaign response relative to an appropriate control.

## Limitations

- Rank-based group selection can introduce regression-to-the-mean effects even with the baseline period fixed and sensitivity-tested.
- Spending comparisons describe observed change, not its cause.
- New/reactivated labels depend on the available transaction history; earlier activity may not be observed.
- Demographic-data availability may be a proxy for unobserved customer engagement.
- The predictive model uses **499 households**, limiting the precision of reported performance.
- The target is **retention of high-spending rank**, not direct customer churn or lifetime value.

**Bottom line:** The initial top 20% did not account for the later spending growth. Most of the increase among other households came from existing customers, not the new/reactivated group. Predicting high-spender rank decline was possible to a degree, but those predictions should not be presented as churn or causal marketing effects.
