# SQL Business Intelligence Analysis Results

**Database:** `sql/superstore.db`  
**Query Script:** `sql/03_analytical_queries.sql`  
**Fact Table Record Count:** 9,994 transactions  

---

## 1. Executive Performance Metrics
Summary KPIs derived from aggregate functions and distinct subqueries:

| KPI Metric | Value | Business Significance |
|---|---|---|
| **Gross Revenue** | **$2,297,200.65** | Cumulative top-line revenue over 4 calendar years. |
| **Net Operating Profit** | **$286,396.54** | True bottom-line earnings after product & discount costs. |
| **Blended Net Margin** | **12.47%** | Baseline corporate margin hurdle. |
| **Total Order Transactions** | **5,009** | Distinct purchase events across all channels. |
| **Total Items Sold** | **9,994** | Total line-item units fulfilled. |
| **Average Order Value (AOV)** | **$458.61** | Average gross revenue generated per order basket. |
| **Unique Customer Accounts** | **793** | Total customer relationships established. |
| **Average Fulfillment SLA** | **4.0 days** | Warehouse order-to-shipping duration. |
| **Order Return Rate** | **5.91%** | 296 distinct orders returned out of 5,009 total orders. |

---

## 2. Regional Performance & Leadership Scorecard
Evaluated via `INNER JOIN` between `fact_orders` and `dim_managers`:

| region   | regional_manager   |   total_orders |   active_customers |   total_sales_usd |   total_profit_usd |   profit_margin_pct |   avg_discount_pct |   profitability_rank |
|:---------|:-------------------|---------------:|-------------------:|------------------:|-------------------:|--------------------:|-------------------:|---------------------:|
| West     | Anna Andreadi      |           1611 |                686 |            725458 |           108418   |               14.94 |               10.9 |                    1 |
| East     | Chuck Magee        |           1401 |                674 |            678781 |            91522.5 |               13.48 |               14.5 |                    2 |
| South    | Cassandra Brandow  |            822 |                512 |            391722 |            46749.5 |               11.93 |               14.7 |                    3 |
| Central  | Kelly Williams     |           1175 |                629 |            501240 |            39706.2 |                7.92 |               24   |                    4 |

* **Finding:** The **West Region** (Anna Andreadi) leads company profitability at **$108,418.31** with the highest margin (**14.94%**).
* **Vulnerability:** The **Central Region** (Kelly Williams) generates **$501,239.76** in sales but realizes only **$39,706.24** in profit (**7.92% margin**), burdened by high promotional discounting (**17.2% average discount**).

---

## 3. Product Sub-Category Margin Health
Categorized using `CASE WHEN` logic and `DENSE_RANK() OVER (PARTITION BY category)`:

| category        | sub_category   |   total_transactions |   units_sold |   total_sales_usd |   total_profit_usd |   profit_margin_pct | margin_health_tier      |   rank_within_category |
|:----------------|:---------------|---------------------:|-------------:|------------------:|-------------------:|--------------------:|:------------------------|-----------------------:|
| Furniture       | Chairs         |                  617 |         2356 |         328449    |           26590.1  |                8.1  | Low Margin (<10%)       |                      1 |
| Furniture       | Furnishings    |                  957 |         3563 |          91705.1  |           13059.2  |               14.24 | Healthy Margin (10-25%) |                      2 |
| Furniture       | Bookcases      |                  228 |          868 |         114880    |           -3472.59 |               -3.02 | Critical Loss-Maker     |                      3 |
| Furniture       | Tables         |                  319 |         1241 |         206966    |          -17725.6  |               -8.56 | Critical Loss-Maker     |                      4 |
| Office Supplies | Paper          |                 1370 |         5178 |          78479.2  |           34053.1  |               43.39 | High Margin (>25%)      |                      1 |
| Office Supplies | Binders        |                 1523 |         5974 |         203413    |           30221.5  |               14.86 | Healthy Margin (10-25%) |                      2 |
| Office Supplies | Storage        |                  846 |         3158 |         223844    |           21278.9  |                9.51 | Low Margin (<10%)       |                      3 |
| Office Supplies | Appliances     |                  466 |         1729 |         107532    |           18138    |               16.87 | Healthy Margin (10-25%) |                      4 |
| Office Supplies | Envelopes      |                  254 |          906 |          16476.4  |            6964.06 |               42.27 | High Margin (>25%)      |                      5 |
| Office Supplies | Art            |                  796 |         3000 |          27118.8  |            6527.84 |               24.07 | Healthy Margin (10-25%) |                      6 |
| Office Supplies | Labels         |                  364 |         1400 |          12486.3  |            5546.18 |               44.42 | High Margin (>25%)      |                      7 |
| Office Supplies | Fasteners      |                  217 |          914 |           3024.25 |             949.52 |               31.4  | High Margin (>25%)      |                      8 |
| Office Supplies | Supplies       |                  190 |          647 |          46673.5  |           -1189.08 |               -2.55 | Critical Loss-Maker     |                      9 |
| Technology      | Copiers        |                   68 |          234 |         149528    |           55617.9  |               37.2  | High Margin (>25%)      |                      1 |
| Technology      | Phones         |                  889 |         3289 |         330007    |           44516.1  |               13.49 | Healthy Margin (10-25%) |                      2 |
| Technology      | Accessories    |                  775 |         2976 |         167380    |           41936.8  |               25.05 | High Margin (>25%)      |                      3 |
| Technology      | Machines       |                  115 |          440 |         189239    |            3384.72 |                1.79 | Low Margin (<10%)       |                      4 |

* **Critical Loss-Makers:**
  1. `Tables` (Furniture): **-$17,725.57** loss on $206,965.53 in sales (**-8.56% margin**).
  2. `Bookcases` (Furniture): **-$3,472.59** loss on $114,879.98 in sales (**-3.02% margin**).
  3. `Supplies` (Office Supplies): **-$1,189.08** loss on $46,673.52 in sales (**-2.55% margin**).
* **Cash Cow Sub-Categories:**
  * `Copiers`: **$55,617.88 profit** on 68 transactions (**37.20% margin**).
  * `Phones`: **$44,516.06 profit** on $330,007.10 sales.
  * `Paper`: **$34,053.11 profit** on $78,479.24 sales (**43.39% margin**).

---

## 4. Multi-Year Trajectory & YoY Growth
Computed using Common Table Expressions and `LAG()` window functions:

|   order_year |   total_orders |   total_sales |   prev_year_sales |   yoy_sales_growth_pct |   total_profit |   prev_year_profit |   yoy_profit_growth_pct |   profit_margin_pct |
|-------------:|---------------:|--------------:|------------------:|-----------------------:|---------------:|-------------------:|------------------------:|--------------------:|
|         2015 |            969 |        484247 |               nan |                 nan    |        49543.9 |              nan   |                  nan    |               10.23 |
|         2016 |           1038 |        470532 |            484247 |                  -2.83 |        61618.4 |            49543.9 |                   24.37 |               13.1  |
|         2017 |           1315 |        609206 |            470532 |                  29.47 |        81794.9 |            61618.4 |                   32.74 |               13.43 |
|         2018 |           1687 |        733215 |            609206 |                  20.36 |        93439.3 |            81794.9 |                   14.24 |               12.74 |

* **Key Takeaway:** Superstore underwent rapid expansion in 2017 (+29.47% sales, +32.74% profit) and continued momentum into 2018 (+20.36% sales, reaching $733,215.05). However, 2018 profit margin softened to **12.74%** from **13.43%** in 2017 as discount volume escalated.

---

## 5. Discount Elasticity Matrix
Segmented into discrete promotional bands:

| discount_tier                   |   line_item_count | total_sales_usd   | total_profit_usd   | realized_margin_pct   |   loss_making_orders | loss_rate_pct   |
|:--------------------------------|------------------:|:------------------|:-------------------|:----------------------|---------------------:|:----------------|
| 1. Full Price (0% Discount)     |              4798 | $1,087,908.47     | $320,987.01        | 29.50%                |                    0 | 0.00%           |
| 2. Moderate Promo (1% - 20%)    |              3803 | $846,522.11       | $100,785.81        | 11.91%                |                  523 | 13.75%          |
| 3. Aggressive Promo (21% - 40%) |               460 | $234,137.95       | $-35,817.54        | -15.30%               |                  415 | 90.22%          |
| 4. Clearance (>40% Discount)    |               933 | $128,632.12       | $-99,558.74        | -77.40%               |                  933 | 100.00%         |

* **The Margin Cliff:** 
  * Full-price orders (0% discount) deliver a pristine **29.50% profit margin** with **0% loss rate**.
  * Moderate promotions (1-20%) deliver a sustainable **11.91% margin**.
  * **The Cliff:** The moment discounts surpass **20%**, margins collapse into the negative (**-15.30%**), with **90.22% of orders losing money**.
  * Above **40% discount**, **100.0% of all orders generate severe losses**, racking up **-$99,558.74** in cumulative capital destruction!

---

## 6. Extreme SKU Analysis: Cash Cows vs Capital Burners
Ranked via `ROW_NUMBER() OVER (ORDER BY total_profit)`:

| cohort               |   cohort_rank | product_name                                                                | category        | sub_category   |   total_sales |   total_profit |   avg_discount_pct |
|:---------------------|--------------:|:----------------------------------------------------------------------------|:----------------|:---------------|--------------:|---------------:|-------------------:|
| Worst Capital Burner |             1 | Cubify CubeX 3D Printer Double Head Print                                   | Technology      | Machines       |      11100    |       -8879.97 |               53.3 |
| Worst Capital Burner |             2 | Lexmark MX611dhe Monochrome Laser Printer                                   | Technology      | Machines       |      16829.9  |       -4589.97 |               40   |
| Worst Capital Burner |             3 | Cubify CubeX 3D Printer Triple Head Print                                   | Technology      | Machines       |       7999.98 |       -3839.99 |               50   |
| Worst Capital Burner |             4 | Chromcraft Bull-Nose Wood Oval Conference Tables & Bases                    | Furniture       | Tables         |       9917.64 |       -2876.11 |               28   |
| Worst Capital Burner |             5 | Bush Advantage Collection Racetrack Conference Table                        | Furniture       | Tables         |       9544.72 |       -1934.4  |               35   |
| Top Cash Cow         |             1 | Canon imageCLASS 2200 Advanced Copier                                       | Technology      | Copiers        |      61599.8  |       25199.9  |               12   |
| Top Cash Cow         |             2 | Fellowes PB500 Electric Punch Plastic Comb Binding Machine with Manual Bind | Office Supplies | Binders        |      27453.4  |        7753.04 |               24   |
| Top Cash Cow         |             3 | Hewlett Packard LaserJet 3310 Copier                                        | Technology      | Copiers        |      18839.7  |        6983.89 |               20   |
| Top Cash Cow         |             4 | Canon PC1060 Personal Laser Copier                                          | Technology      | Copiers        |      11619.8  |        4570.94 |               15   |
| Top Cash Cow         |             5 | HP Designjet T520 Inkjet Large Format Printer - 24" Color                   | Technology      | Machines       |      18374.9  |        4094.98 |               16.7 |

* **Finding:** A single product—the `Cubify CubeX 3D Printer Double Head Print`—lost **$8,879.97** on just $11,099.95 of sales due to an average discount rate of **53.3%**.
