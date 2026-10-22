-- =============================================================================
-- SUPERSTORE ADVANCED BUSINESS INTELLIGENCE ANALYTICAL QUERIES
-- File: sql/03_analytical_queries.sql
-- Database: superstore.db
-- Techniques Demonstrated:
--   - Multi-Table JOINs (INNER, LEFT)
--   - Aggregations with GROUP BY & HAVING
--   - Conditional Logic with CASE WHEN
--   - Common Table Expressions (CTEs)
--   - Correlated and Inline Subqueries
--   - Window Functions (ROW_NUMBER, DENSE_RANK, LAG, SUM OVER)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- QUERY 1: EXECUTIVE KPI SUMMARY
-- Techniques: Aggregate Functions, Distinct Counting, Subqueries
-- Business Objective: High-level health check of sales volume, net margin, and customer reach.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- QUERY 2: REGIONAL PERFORMANCE & LEADERSHIP ACCOUNTABILITY SCORECARD
-- Techniques: INNER JOIN with Dimension Table, GROUP BY, Window Function DENSE_RANK()
-- Business Objective: Rank sales territories and evaluate regional manager effectiveness.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- QUERY 3: PRODUCT TAXONOMY & MARGIN HEALTH AUDIT
-- Techniques: GROUP BY, CASE WHEN Classification, Window Ranking
-- Business Objective: Identify sub-categories that drive margins vs those draining capital.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- QUERY 4: YEAR-OVER-YEAR (YoY) SALES & PROFIT GROWTH TRENDS
-- Techniques: CTEs, Date Extraction, Window Function LAG()
-- Business Objective: Track multi-year trajectory and annual growth percentages.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- QUERY 5: MONTH-OVER-MONTH (MoM) TRAILING 12 MONTH RUN RATE
-- Techniques: CTEs, String Formatting, Window Function LAG()
-- Business Objective: Uncover seasonality and short-term operational fluctuations.
-- -----------------------------------------------------------------------------
WITH monthly_metrics AS (
    SELECT 
        strftime('%Y-%m', order_date) AS order_month,
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(SUM(sales), 2) AS monthly_sales,
        ROUND(SUM(profit), 2) AS monthly_profit
    FROM fact_orders
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT 
    order_month,
    total_orders,
    monthly_sales,
    LAG(monthly_sales) OVER (ORDER BY order_month) AS prev_month_sales,
    ROUND((monthly_sales - LAG(monthly_sales) OVER (ORDER BY order_month)) / LAG(monthly_sales) OVER (ORDER BY order_month) * 100, 2) AS mom_sales_growth_pct,
    monthly_profit,
    ROUND((monthly_profit - LAG(monthly_profit) OVER (ORDER BY order_month)) / LAG(monthly_profit) OVER (ORDER BY order_month) * 100, 2) AS mom_profit_growth_pct,
    ROUND(monthly_profit / monthly_sales * 100, 2) AS monthly_margin_pct
FROM monthly_metrics
ORDER BY order_month DESC
LIMIT 12;


-- -----------------------------------------------------------------------------
-- QUERY 6: DISCOUNT ELASTICITY & PROFIT EROSION SENSITIVITY MATRIX
-- Techniques: CASE WHEN Bucketing, Conditional Aggregation, Ratio Analysis
-- Business Objective: Prove the inflection point where discount promotions destroy profit.
-- -----------------------------------------------------------------------------
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


-- -----------------------------------------------------------------------------
-- QUERY 7: CUSTOMER LIFETIME VALUE (CLV) & TOP 10 PROFIT VALUE DRIVERS
-- Techniques: CTEs, GROUP BY, Window Function DENSE_RANK() & Running Total
-- Business Objective: Differentiate top revenue accounts from true profit contributors.
-- -----------------------------------------------------------------------------
WITH customer_aggregates AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(*) AS total_items_purchased,
        ROUND(SUM(sales), 2) AS total_revenue,
        ROUND(SUM(profit), 2) AS total_profit,
        ROUND(SUM(profit) / SUM(sales) * 100, 2) AS customer_margin_pct
    FROM fact_orders
    GROUP BY customer_id, customer_name, segment
)
SELECT 
    DENSE_RANK() OVER (ORDER BY total_profit DESC) AS profit_rank,
    customer_name,
    segment,
    total_orders,
    total_revenue,
    total_profit,
    customer_margin_pct
FROM customer_aggregates
ORDER BY profit_rank ASC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- QUERY 8: EXTREME PRODUCT DRILLDOWN: TOP 5 CASH COWS VS TOP 5 CAPITAL BURNERS
-- Techniques: Window Ranking (ROW_NUMBER), CTEs, UNION ALL
-- Business Objective: Isolate high-impact SKUs for inventory and pricing strategy.
-- -----------------------------------------------------------------------------
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
