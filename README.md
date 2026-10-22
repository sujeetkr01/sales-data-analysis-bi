# Global Superstore Sales Performance & Profitability Intelligence

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Desktop-F2C811.svg?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![DAX](https://img.shields.io/badge/DAX-Advanced_Modeling-orange.svg)](https://learn.microsoft.com/en-us/dax/)
[![Pandas](https://img.shields.io/badge/Pandas-Vectorized_ETL-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Status](https://img.shields.io/badge/Project-Production_Ready-success.svg)]()

> **An end-to-end, enterprise-grade business intelligence and analytics engineering portfolio project.**  
> Investigates **$2,297,200.65 in gross sales** and **$286,396.54 in net profit** across 9,994 transactions to uncover critical margin leakage, diagnose severe promotional discount decay, model a Kimball Star Schema warehouse, and deliver an interactive 4-page Power BI executive suite.

---

## 📌 Executive Summary & Key Results

| Enterprise Metric | Value | Cross-Tool Reconciliation Status |
|:---|---:|:---:|
| **Gross Revenue Analyzed** | **$2,297,200.65** | 100% Match across SQL, Python, Power BI ($0.0000 delta) |
| **Net Operating Profit** | **$286,396.54** | 100% Match across SQL, Python, Power BI ($0.0000 delta) |
| **Blended Net Margin** | **12.47%** | 100% Match across SQL, Python, Power BI |
| **Total Fulfilled Orders** | **5,009 orders** (9,994 line items) | 100% Match across SQL, Python, Power BI |
| **Identified Profit Recovery Levers** | **+$101,000 – $136,000 / year** | Data-backed operational initiatives |

---

## 🏗️ Analytics Engineering Architecture

The project follows a standard enterprise data lifecycle:

```
[Raw Multi-Sheet Export] 
        │
        ▼ (Python/OpenPyXL ETL & Cleaning)
[Normalized Staging Datasets] 
        ├── orders_cleaned.csv (9,994 Fact rows)
        ├── people_cleaned.csv (4 Managers)
        └── returns_cleaned.csv (296 Deduplicated Returns)
        │
        ├────────────────────────────────┬────────────────────────────────┐
        ▼                                ▼                                ▼
[Relational SQL Warehouse]      [Python Statistical EDA]      [Power BI Star Schema]
  - SQLite DDL Schema             - Parametric / Non-Parametric   - Kimball Star Model
  - Window Functions & CTEs       - Hypothesis Testing (ANOVA)    - 25+ DAX Measures
  - P&L Aggregations              - High-Res Visuals (300 DPI)    - Interactive 4-Page App
        │                                │                                │
        └────────────────────────────────┴────────────────────────────────┘
                                         │
                                         ▼
                   [Automated Cross-Engine Reconciliation]
                     (12/12 KPIs Verified with $0.00 Variance)
```

---

## 🧠 Top 5 Business Findings & Strategic Recommendations

### 1. The 20% Promotional Discount Cliff
* **Finding:** Full-price orders deliver **29.50% profit margin**. Moderate discounts (1–20%) generate **11.91% margin**. However, past **20% discount**, margins collapse to **-15.30%**, with **90.22% of transactions losing money**. Discounts >40% destroy capital on **100.0% of orders**, burning **-$99,558.74**.
* **Recommendation:** Implement a hard 20% discount cap in the CRM/ERP system. Require Regional Director sign-off for quotes between 21% and 30%.
* **Potential Value:** **+$45,000 – $65,000 / year**.

### 2. Systemic Product Drag in Furniture (`Tables` & `Bookcases`)
* **Finding:** Exactly three sub-categories operate at a net financial loss across company history: `Tables` (**-$17,725.57 loss**), `Bookcases` (**-$3,472.59 loss**), and `Supplies` (**-$1,189.08 loss**), creating a **-$22.4K capital drag**.
* **Recommendation:** Unbundle delivery costs for heavy furniture, institute freight surcharges, and transition tables to a Made-to-Order / direct drop-ship model.
* **Potential Value:** **+$18,000 – $22,000 / year**.

### 3. Central Region Margin Compression & Discount Over-Reliance
* **Finding:** The West Region (Anna Andreadi) leads company profitability at **14.94% margin** with 10.9% average discount. The Central Region (Kelly Williams) realizes only **7.92% margin** due to an aggressive **24.0% average discount rate**, with Texas alone losing **-$25,729.39**.
* **Recommendation:** Restructure sales incentives from gross volume quotas to **Gross Margin Dollar Contribution ($)**.
* **Potential Value:** **+$20,000 – $25,000 / year**.

### 4. The Top-Customer Revenue Mirage (Sean Miller vs. Tamara Chand)
* **Finding:** #1 Customer by Revenue, **Sean Miller** ($25,043 spent), generated a **-$1,980.75 net loss (-7.91% margin)** due to steep discounts on technology hardware. Conversely, #2 Customer **Tamara Chand** ($19,052 spent) delivered **+$8,981.32 in profit (+47.14% margin)**.
* **Recommendation:** Shift account tiering from revenue spend to Customer Profit Contribution scoring; enforce minimum 15% margin hurdles on high-volume accounts.
* **Potential Value:** **+$8,000 – $12,000 / year**.

### 5. Return Rate Spikes in Expedited Technology Logistics
* **Finding:** While overall order returns average 5.91%, **Technology orders shipped via Same Day have a 12.66% return rate**, and First Class has a **10.40% return rate**.
* **Recommendation:** Enforce automated pre-dispatch configuration confirmation for expedited electronics orders over $500, and introduce a 10% restocking fee.
* **Potential Value:** **+$10,000 – $12,000 / year**.

---

## 📊 Visual Artifacts & Interactive Dashboard Preview

| Visual Artifact | Chart Type & Focus | Preview File |
|---|---|:---:|
| **Monthly Run Rate** | Dual-Axis Combo Line/Area (Sales vs Profit) | [`visuals/01_monthly_sales_profit_trend.png`](visuals/01_monthly_sales_profit_trend.png) |
| **The Discount Cliff** | Scatter Plot + Polynomial Fit (Margin Collapse past 20%) | [`visuals/02_discount_profit_cliff.png`](visuals/02_discount_profit_cliff.png) |
| **Sub-Category Divergence** | Divergent Bar Chart (Profitable vs Loss Sub-Categories) | [`visuals/03_subcat_profitability_divergence.png`](visuals/03_subcat_profitability_divergence.png) |
| **Territory Scorecard** | Dual-Panel Grouped Bar Chart (Sales, Profit, Margin %) | [`visuals/04_regional_performance_manager_scorecard.png`](visuals/04_regional_performance_manager_scorecard.png) |
| **Correlation Heatmap** | Annotated Spearman Rank Correlation Matrix | [`visuals/05_correlation_heatmap.png`](visuals/05_correlation_heatmap.png) |
| **Logistics & Segments** | Boxplots of Segment Margins & Transit Duration SLAs | [`visuals/06_customer_segment_and_logistics.png`](visuals/06_customer_segment_and_logistics.png) |

> 🌐 **Interactive Power BI Dashboard Prototype:** Open [`powerbi/dashboard_wireframe.html`](powerbi/dashboard_wireframe.html) in any modern browser for a live preview of the 4-page dashboard interface.

---

## 🗄️ Relational Data Model (Kimball Star Schema)

```
        Dim_Managers (1:N) ──► Dim_Geography (1:N) ──┐
                                                    ▼
   Dim_Date (1:N Active / Inactive) ───────────► Fact_Orders (9,994 rows)
                                                    ▲          ▲
        Dim_Customers (1:N) ────────────────────────┘          │
        Dim_Products (1:N) ────────────────────────────────────┤
        Dim_Returns (1:1 / 1:N) ───────────────────────────────┘
```

---

## 💻 Technical Code Highlights

### SQL: Discount Sensitivity Matrix & Loss Rate Analysis
```sql
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
    ROUND(SUM(CASE WHEN profit < 0 THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100, 2) AS loss_rate_pct
FROM fact_orders
GROUP BY discount_tier
ORDER BY discount_tier ASC;
```

### DAX: Time Intelligence with Safe Blank Handling
```dax
// Prior Year Sales & YoY Growth Rate
Sales PY = 
CALCULATE (
    [Total Sales],
    SAMEPERIODLASTYEAR ( Dim_Date[Date] )
)

Sales YoY % = 
DIVIDE ( [Total Sales] - [Sales PY], [Sales PY], BLANK () )

// Role-Playing Relationship for Dispatch Fulfillment Date
Sales by Ship Date = 
CALCULATE (
    [Total Sales],
    USERELATIONSHIP ( Fact_Orders[Ship Date], Dim_Date[Date] )
)
```

---

## ⚡ Quickstart: Reproducing the Project

Clone the repository and run the end-to-end analytics pipeline:

```bash
# 1. Clone repository
git clone https://github.com/sujeetkr01/sales-data-analysis-bi.git
cd sales-data-analysis-bi

# 2. Run Data Quality Audit & Schema Inspection
python python/01_data_quality_audit.py

# 3. Execute Excel Transformation & Staging Generation
python python/02_excel_cleaning_pipeline.py

# 4. Initialize SQLite Warehouse & Load Tables
python sql/02_load_data.py

# 5. Execute Analytical SQL Suite
python python/03_run_sql_analysis.py

# 6. Run Python Statistical EDA & Generate Visuals
python python/04_exploratory_data_analysis.py

# 7. Export Power BI Star Schema Model
python python/05_export_powerbi_data_model.py

# 8. Run 3-Way Cross-Tool Mathematical Reconciliation
python python/06_cross_tool_validation.py
```

---

## 📁 Repository Directory Structure

```
sales-data-analysis-bi/
│
├── data/
│   ├── raw/                           # Immutable raw source export
│   └── processed/                     # Cleaned Excel workbook & CSV staging files
├── sql/
│   ├── 01_schema_ddl.sql              # Normalized DDL table definitions & indexes
│   ├── 02_load_data.py                # Automated database ingestion pipeline
│   ├── 03_analytical_queries.sql      # Advanced SQL analytical suite
│   └── superstore.db                  # Portable production SQLite database
├── python/
│   ├── 01_data_quality_audit.py       # Data quality and missing values audit
│   ├── 02_excel_cleaning_pipeline.py  # Excel transformation pipeline
│   ├── 03_run_sql_analysis.py         # Automated SQL query execution & markdown builder
│   ├── 04_exploratory_data_analysis.py# Statistical EDA, ANOVA tests & chart generation
│   ├── 05_export_powerbi_data_model.py# Kimball Star Schema model exporter
│   └── 06_cross_tool_validation.py    # 3-way cross-engine reconciliation audit
├── powerbi/
│   ├── 01_dax_measures.dax            # 25+ production DAX measures & Date table script
│   ├── dashboard_wireframe.html       # Interactive 4-page prototype
│   └── model_data/                    # Star Schema CSV dimension and fact tables
├── visuals/                           # 300 DPI publication-quality charts
├── docs/                              # Comprehensive audit logs, specifications & reports
├── .gitignore                         # Standard Python & OS ignore rules
└── README.md                          # Project documentation
```

---

## 📄 Resume Bullet Points for Data Analyst Roles

* **Sales Performance & Profitability Intelligence Project | Excel, SQL, Python, Power BI, DAX**
  * Engineered an end-to-end retail BI solution analyzing **$2.30M in revenue** and **$286K in profit** across **9,994 transactions**, delivering actionable business strategies to recover **+$101K–$136K** in lost annual profit.
  * Designed a normalized relational database in **SQL (SQLite)** and dimensional Star Schema in **Power BI**, writing complex queries with CTEs, window functions (`DENSE_RANK`, `LAG`), and 25+ **DAX measures** (`SAMEPERIODLASTYEAR`, `USERELATIONSHIP`).
  * Discovered the **20% promotional discount cliff** where transaction loss rates surge from **13.8% to 90.2%**, isolating **-$135K in capital destruction** and defining executive discount governance rules.
  * Conducted inferential hypothesis testing (**One-Way ANOVA**, Pearson/Spearman correlations) in **Python (Scipy, Pandas, Seaborn)**, disproving segment profitability assumptions ($p=0.0548$) and identifying three chronic loss-making sub-categories (`Tables`, `Bookcases`, `Supplies`).
  * Implemented an automated cross-engine reconciliation test in Python, validating **100% calculation parity ($0.0000 variance)** across SQL, Python, and Power BI DAX calculations across all 12 corporate KPIs.
