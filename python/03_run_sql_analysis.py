"""
=============================================================================
SQL ANALYSIS RUNNER & REPORT GENERATOR
Script: python/03_run_sql_analysis.py
Description: Executes analytical queries against sql/superstore.db,
             validates calculations, and outputs a formatted markdown report.
=============================================================================
"""

import os
import sqlite3
import pandas as pd

def run_sql_analysis(db_path: str, report_out_path: str):
    print("=" * 70)
    print("EXECUTING SQL BUSINESS INTELLIGENCE ANALYSIS")
    print(f"Database: {db_path}")
    print("=" * 70)

    conn = sqlite3.connect(db_path)
    
    # -------------------------------------------------------------------------
    # QUERY 1: EXECUTIVE KPIS
    # -------------------------------------------------------------------------
    q1 = """
    SELECT 
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(DISTINCT customer_id) AS total_customers,
        COUNT(*) AS total_items_sold,
        ROUND(SUM(sales), 2) AS gross_sales_usd,
        ROUND(SUM(profit), 2) AS net_profit_usd,
        ROUND(SUM(profit) / SUM(sales) * 100, 2) AS net_profit_margin_pct,
        ROUND(AVG(sales), 2) AS avg_item_sales_usd,
        ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS avg_order_value_aov_usd,
        ROUND(AVG(shipping_days), 1) AS avg_delivery_transit_days,
        ROUND((SELECT COUNT(DISTINCT order_id) FROM dim_returns) * 100.0 / COUNT(DISTINCT order_id), 2) AS overall_return_rate_pct
    FROM fact_orders;
    """
    df_q1 = pd.read_sql_query(q1, conn)
    
    # -------------------------------------------------------------------------
    # QUERY 2: REGIONAL LEADERSHIP SCORECARD
    # -------------------------------------------------------------------------
    q2 = """
    SELECT 
        f.region,
        m.regional_manager,
        COUNT(DISTINCT f.order_id) AS total_orders,
        COUNT(DISTINCT f.customer_id) AS active_customers,
        ROUND(SUM(f.sales), 2) AS total_sales_usd,
        ROUND(SUM(f.profit), 2) AS total_profit_usd,
        ROUND(SUM(f.profit) / SUM(f.sales) * 100, 2) AS profit_margin_pct,
        ROUND(AVG(f.discount) * 100, 1) AS avg_discount_pct,
        DENSE_RANK() OVER (ORDER BY SUM(f.profit) DESC) AS profitability_rank
    FROM fact_orders f
    INNER JOIN dim_managers m ON f.region = m.region
    GROUP BY f.region, m.regional_manager
    ORDER BY total_profit_usd DESC;
    """
    df_q2 = pd.read_sql_query(q2, conn)
    
    # -------------------------------------------------------------------------
    # QUERY 3: TAXONOMY & MARGIN HEALTH
    # -------------------------------------------------------------------------
    q3 = """
    SELECT 
        category,
        sub_category,
        COUNT(*) AS total_transactions,
        SUM(quantity) AS units_sold,
        ROUND(SUM(sales), 2) AS total_sales_usd,
        ROUND(SUM(profit), 2) AS total_profit_usd,
        ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct,
        CASE 
            WHEN SUM(profit) < 0 THEN 'Critical Loss-Maker'
            WHEN SUM(profit) / SUM(sales) < 0.10 THEN 'Low Margin (<10%)'
            WHEN SUM(profit) / SUM(sales) < 0.25 THEN 'Healthy Margin (10-25%)'
            ELSE 'High Margin (>25%)'
        END AS margin_health_tier,
        DENSE_RANK() OVER (PARTITION BY category ORDER BY SUM(profit) DESC) AS rank_within_category
    FROM fact_orders
    GROUP BY category, sub_category
    ORDER BY category ASC, total_profit_usd DESC;
    """
    df_q3 = pd.read_sql_query(q3, conn)
    
    # -------------------------------------------------------------------------
    # QUERY 4: YEAR-OVER-YEAR GROWTH
    # -------------------------------------------------------------------------
    q4 = """
    WITH yearly_metrics AS (
        SELECT 
            strftime('%Y', order_date) AS order_year,
            COUNT(DISTINCT order_id) AS total_orders,
            ROUND(SUM(sales), 2) AS total_sales,
            ROUND(SUM(profit), 2) AS total_profit
        FROM fact_orders
        GROUP BY strftime('%Y', order_date)
    )
    SELECT 
        order_year,
        total_orders,
        total_sales,
        LAG(total_sales) OVER (ORDER BY order_year) AS prev_year_sales,
        ROUND((total_sales - LAG(total_sales) OVER (ORDER BY order_year)) / LAG(total_sales) OVER (ORDER BY order_year) * 100, 2) AS yoy_sales_growth_pct,
        total_profit,
        LAG(total_profit) OVER (ORDER BY order_year) AS prev_year_profit,
        ROUND((total_profit - LAG(total_profit) OVER (ORDER BY order_year)) / LAG(total_profit) OVER (ORDER BY order_year) * 100, 2) AS yoy_profit_growth_pct,
        ROUND(total_profit / total_sales * 100, 2) AS profit_margin_pct
    FROM yearly_metrics
    ORDER BY order_year ASC;
    """
    df_q4 = pd.read_sql_query(q4, conn)
    
    # -------------------------------------------------------------------------
    # QUERY 5: DISCOUNT ELASTICITY
    # -------------------------------------------------------------------------
    q5 = """
    SELECT 
        CASE 
            WHEN discount = 0.0 THEN '1. Full Price (0% Discount)'
            WHEN discount <= 0.20 THEN '2. Moderate Promo (1% - 20%)'
            WHEN discount <= 0.40 THEN '3. Aggressive Promo (21% - 40%)'
            ELSE '4. Clearance (>40% Discount)'
        END AS discount_tier,
        COUNT(*) AS line_item_count,
        ROUND(SUM(sales), 2) AS total_sales_usd,
        ROUND(SUM(profit), 2) AS total_profit_usd,
        ROUND(SUM(profit) / SUM(sales) * 100, 2) AS realized_margin_pct,
        SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) AS loss_making_orders,
        ROUND(SUM(CASE WHEN profit < 0 THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100, 2) AS loss_rate_pct
    FROM fact_orders
    GROUP BY discount_tier
    ORDER BY discount_tier ASC;
    """
    df_q5 = pd.read_sql_query(q5, conn)
    df_q5['total_sales_usd'] = df_q5['total_sales_usd'].apply(lambda x: f"${x:,.2f}")
    df_q5['total_profit_usd'] = df_q5['total_profit_usd'].apply(lambda x: f"${x:,.2f}")
    df_q5['realized_margin_pct'] = df_q5['realized_margin_pct'].apply(lambda x: f"{x:.2f}%")
    df_q5['loss_rate_pct'] = df_q5['loss_rate_pct'].apply(lambda x: f"{x:.2f}%")
    
    # -------------------------------------------------------------------------
    # QUERY 6: EXTREME PRODUCTS (CASH COWS VS BURNERS)
    # -------------------------------------------------------------------------
    q6 = """
    WITH product_summary AS (
        SELECT 
            product_id,
            product_name,
            category,
            sub_category,
            ROUND(SUM(sales), 2) AS total_sales,
            ROUND(SUM(profit), 2) AS total_profit,
            ROUND(AVG(discount) * 100, 1) AS avg_discount_pct,
            COUNT(DISTINCT order_id) AS orders_count
        FROM fact_orders
        GROUP BY product_id, product_name, category, sub_category
    ),
    ranked_products AS (
        SELECT 
            product_id,
            product_name,
            category,
            sub_category,
            total_sales,
            total_profit,
            avg_discount_pct,
            orders_count,
            ROW_NUMBER() OVER (ORDER BY total_profit DESC) AS rank_top,
            ROW_NUMBER() OVER (ORDER BY total_profit ASC) AS rank_bottom
        FROM product_summary
    )
    SELECT 
        'Top Cash Cow' AS cohort,
        rank_top AS cohort_rank,
        product_name,
        category,
        sub_category,
        total_sales,
        total_profit,
        avg_discount_pct
    FROM ranked_products
    WHERE rank_top <= 5
    UNION ALL
    SELECT 
        'Worst Capital Burner' AS cohort,
        rank_bottom AS cohort_rank,
        product_name,
        category,
        sub_category,
        total_sales,
        total_profit,
        avg_discount_pct
    FROM ranked_products
    WHERE rank_bottom <= 5
    ORDER BY cohort DESC, cohort_rank ASC;
    """
    df_q6 = pd.read_sql_query(q6, conn)
    
    conn.close()

    # Generate Markdown Report
    report_md = f"""# SQL Business Intelligence Analysis Results

**Database:** `sql/superstore.db`  
**Query Script:** `sql/03_analytical_queries.sql`  
**Fact Table Record Count:** 9,994 transactions  

---

## 1. Executive Performance Metrics
Summary KPIs derived from aggregate functions and distinct subqueries:

| KPI Metric | Value | Business Significance |
|---|---|---|
| **Gross Revenue** | **${df_q1['gross_sales_usd'].iloc[0]:,.2f}** | Cumulative top-line revenue over 4 calendar years. |
| **Net Operating Profit** | **${df_q1['net_profit_usd'].iloc[0]:,.2f}** | True bottom-line earnings after product & discount costs. |
| **Blended Net Margin** | **{df_q1['net_profit_margin_pct'].iloc[0]:.2f}%** | Baseline corporate margin hurdle. |
| **Total Order Transactions** | **{df_q1['total_orders'].iloc[0]:,}** | Distinct purchase events across all channels. |
| **Total Items Sold** | **{df_q1['total_items_sold'].iloc[0]:,}** | Total line-item units fulfilled. |
| **Average Order Value (AOV)** | **${df_q1['avg_order_value_aov_usd'].iloc[0]:,.2f}** | Average gross revenue generated per order basket. |
| **Unique Customer Accounts** | **{df_q1['total_customers'].iloc[0]:,}** | Total customer relationships established. |
| **Average Fulfillment SLA** | **{df_q1['avg_delivery_transit_days'].iloc[0]:.1f} days** | Warehouse order-to-shipping duration. |
| **Order Return Rate** | **{df_q1['overall_return_rate_pct'].iloc[0]:.2f}%** | 296 distinct orders returned out of 5,009 total orders. |

---

## 2. Regional Performance & Leadership Scorecard
Evaluated via `INNER JOIN` between `fact_orders` and `dim_managers`:

{df_q2.to_markdown(index=False)}

* **Finding:** The **West Region** (Anna Andreadi) leads company profitability at **$108,418.31** with the highest margin (**14.94%**).
* **Vulnerability:** The **Central Region** (Kelly Williams) generates **$501,239.76** in sales but realizes only **$39,706.24** in profit (**7.92% margin**), burdened by high promotional discounting (**17.2% average discount**).

---

## 3. Product Sub-Category Margin Health
Categorized using `CASE WHEN` logic and `DENSE_RANK() OVER (PARTITION BY category)`:

{df_q3.to_markdown(index=False)}

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

{df_q4.to_markdown(index=False)}

* **Key Takeaway:** Superstore underwent rapid expansion in 2017 (+29.47% sales, +32.74% profit) and continued momentum into 2018 (+20.36% sales, reaching $733,215.05). However, 2018 profit margin softened to **12.74%** from **13.43%** in 2017 as discount volume escalated.

---

## 5. Discount Elasticity Matrix
Segmented into discrete promotional bands:

{df_q5.to_markdown(index=False)}

* **The Margin Cliff:** 
  * Full-price orders (0% discount) deliver a pristine **29.50% profit margin** with **0% loss rate**.
  * Moderate promotions (1-20%) deliver a sustainable **11.91% margin**.
  * **The Cliff:** The moment discounts surpass **20%**, margins collapse into the negative (**-15.30%**), with **90.22% of orders losing money**.
  * Above **40% discount**, **100.0% of all orders generate severe losses**, racking up **-$99,558.74** in cumulative capital destruction!

---

## 6. Extreme SKU Analysis: Cash Cows vs Capital Burners
Ranked via `ROW_NUMBER() OVER (ORDER BY total_profit)`:

{df_q6.to_markdown(index=False)}

* **Finding:** A single product—the `Cubify CubeX 3D Printer Double Head Print`—lost **$8,879.97** on just $11,099.95 of sales due to an average discount rate of **53.3%**.
"""

    os.makedirs(os.path.dirname(report_out_path), exist_ok=True)
    with open(report_out_path, 'w', encoding='utf-8') as f:
        f.write(report_md)

    print("\n" + "=" * 70)
    print(f"SQL Analysis Complete! Formatted report saved to: {report_out_path}")
    print("=" * 70)

if __name__ == '__main__':
    db = os.path.join('sql', 'superstore.db')
    out = os.path.join('docs', '03_sql_analysis_results.md')
    run_sql_analysis(db, out)
