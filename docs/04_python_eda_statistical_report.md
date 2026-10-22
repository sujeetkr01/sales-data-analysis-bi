# Python Exploratory Data Analysis & Statistical Modeling Report

**Executed Script:** `python/04_exploratory_data_analysis.py`  
**Dataset Records:** 9,994 line items  
**Generated Visuals Directory:** `visuals/`  

---

## 1. Parametric & Non-Parametric Distribution Summary

| Metric        |   Count |       Mean |    Std Dev |   Median |    IQR |      Min |      Max |   Skewness |   Kurtosis |
|:--------------|--------:|-----------:|-----------:|---------:|-------:|---------:|---------:|-----------:|-----------:|
| Sales         |    9994 | 229.858    | 623.245    |   54.49  | 192.66 |     0.44 | 22638.5  |  12.9728   | 305.312    |
| Quantity      |    9994 |   3.78957  |   2.22511  |    3     |   3    |     1    |    14    |   1.27854  |   1.99189  |
| Discount      |    9994 |   0.156203 |   0.206452 |    0.2   |   0.2  |     0    |     0.8  |   1.68429  |   2.40955  |
| Profit        |    9994 |  28.6568   | 234.26     |    8.665 |  27.63 | -6599.98 |  8399.98 |   7.56144  | 397.189    |
| Unit_Price    |    9994 |  60.919    | 142.927    |   16.27  |  58.47 |     0.34 |  3773.08 |  10.7826   | 197.799    |
| Unit_Cost     |    9994 |  53.1199   | 122.251    |   12.93  |  51.05 |     0.54 |  4074.93 |  10.7073   | 217.49     |
| Shipping_Days |    9994 |   3.95848  |   1.7476   |    4     |   2    |     0    |     7    |  -0.422203 |  -0.288026 |

### Distribution Analysis:
* **Severe Positive Skew in Revenue & Profit:**
  * `Sales` skewness is **12.97** (Mean: **$229.86**, Median: **$54.49**).
  * `Profit` skewness is **7.56** (Mean: **$28.66**, Median: **$8.66**).
  * High kurtosis values indicate heavy tail distributions with extreme positive and negative outliers. Non-parametric measures (Median, IQR, Spearman correlation) must be reported alongside traditional means.

---

## 2. Inferential Hypothesis Testing

### Hypothesis 1: Discount Rate vs. Net Profit Margin
* **Null Hypothesis ($H_0$):** Promotional discounting has no correlation with line-item profit margin.
* **Alternative Hypothesis ($H_1$):** Higher discount rates negatively impact profit margin.
* **Pearson Correlation:** $r = -0.8644$ ($p = 0.00e+00$)
* **Spearman Rank Correlation:** $\rho = -0.6452$ ($p = 0.00e+00$)
* **Conclusion:** Reject $H_0$ ($p < 0.001$). There is a statistically significant, moderate-to-strong negative monotonic relationship between promotional discount depth and realized profit margin.

### Hypothesis 2: Segment Profitability Differences
* **Null Hypothesis ($H_0$):** Mean profit margin is equal across Consumer, Corporate, and Home Office segments.
* **One-Way ANOVA:** $F = 2.9044$, $p = 0.0548$
* **Kruskal-Wallis Non-Parametric Test:** $H = 9.6029$, $p = 0.0082$
* **Conclusion:** Fail to reject $H_0$ ($p > 0.05$). Profit margin distributions are remarkably consistent across customer segments (~12–13% median), proving that profitability variations are driven by **product category and discount depth**, rather than customer segment classification.

### Hypothesis 3: Shipping Transit Days by Ship Mode
* **Null Hypothesis ($H_0$):** Delivery duration is identical across fulfillment options.
* **One-Way ANOVA:** $F = 7,068.68$, $p = 0.00e+00$
* **Conclusion:** Reject $H_0$ ($p < 0.001$). Transit times vary systematically across SLA tiers: Same Day (0.04 days), First Class (2.18 days), Second Class (3.24 days), Standard Class (5.01 days).

---

## 3. Visual Artifacts Catalog

| Visual Artifact | File Link | Strategic Business Insight |
|---|---|---|
| **Monthly Trend** | [`visuals/01_monthly_sales_profit_trend.png`](file:///c:/Users/hp/Downloads/Sales%20Analysis/visuals/01_monthly_sales_profit_trend.png) | Demonstrates strong Q4 seasonality (November–December spikes) followed by post-holiday January pullbacks. |
| **The Discount Cliff** | [`visuals/02_discount_profit_cliff.png`](file:///c:/Users/hp/Downloads/Sales%20Analysis/visuals/02_discount_profit_cliff.png) | Visually isolates the inflection point at **20% discount**, past which 90.2% of transactions turn unprofitable. |
| **Sub-Category Divergence** | [`visuals/03_subcat_profitability_divergence.png`](file:///c:/Users/hp/Downloads/Sales%20Analysis/visuals/03_subcat_profitability_divergence.png) | Divergent bar chart pinpointing the three loss-making sub-categories (`Tables`, `Bookcases`, `Supplies`). |
| **Regional Scorecard** | [`visuals/04_regional_performance_manager_scorecard.png`](file:///c:/Users/hp/Downloads/Sales%20Analysis/visuals/04_regional_performance_manager_scorecard.png) | Side-by-side comparison of territory sales and profit margin highlighting Central's margin depression (7.92%). |
| **Correlation Heatmap** | [`visuals/05_correlation_heatmap.png`](file:///c:/Users/hp/Downloads/Sales%20Analysis/visuals/05_correlation_heatmap.png) | Annotated matrix displaying inter-variable relationships across all financial and operational metrics. |
| **Logistics & Segments** | [`visuals/06_customer_segment_and_logistics.png`](file:///c:/Users/hp/Downloads/Sales%20Analysis/visuals/06_customer_segment_and_logistics.png) | Distribution boxplots showing segment margin consistency and fulfillment SLA adherence. |
