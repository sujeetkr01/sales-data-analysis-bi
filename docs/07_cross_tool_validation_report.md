# Cross-Tool Reconciliation & Mathematical Validation Report

**Verification Date:** 2026-10-23  
**Engines Audited:**  
1. **SQL:** Relational Engine (`sql/superstore.db`)  
2. **Python:** Analytical Pandas Pipeline (`data/processed/orders_cleaned.csv`)  
3. **Power BI:** Star Schema Model Data (`powerbi/model_data/`)  

---

## 1. Executive Reconciliation Matrix

| KPI Metric | SQL Query Result | Python Pandas Result | Power BI DAX Result | Variance (SQL - Py) | Variance (SQL - PBI) | Audit Status |
|:---|---:|---:|---:|---:|---:|:---:|
| **Gross Revenue ($)** | `2,297,200.65` | `2,297,200.65` | `2,297,200.65` | `0.0000` | `0.0000` | **100% MATCH (PASS)** |
| **Net Operating Profit ($)** | `286,396.54` | `286,396.54` | `286,396.54` | `0.0000` | `0.0000` | **100% MATCH (PASS)** |
| **Profit Margin (%)** | `12.47` | `12.47` | `12.47` | `0.0000` | `0.0000` | **100% MATCH (PASS)** |
| **Total Orders Count** | `5,009.00` | `5,009.00` | `5,009.00` | `0.0000` | `0.0000` | **100% MATCH (PASS)** |
| **Total Line Items Fulfilled** | `9,994.00` | `9,994.00` | `9,994.00` | `0.0000` | `0.0000` | **100% MATCH (PASS)** |
| **Total Physical Quantity Sold** | `37,873.00` | `37,873.00` | `37,873.00` | `0.0000` | `0.0000` | **100% MATCH (PASS)** |
| **Unique Customer Accounts** | `793.00` | `793.00` | `793.00` | `0.0000` | `0.0000` | **100% MATCH (PASS)** |
| **Average Order Value ($)** | `458.61` | `458.61` | `458.61` | `0.0000` | `0.0000` | **100% MATCH (PASS)** |
| **Loss-Making Transactions Count** | `1,871.00` | `1,871.00` | `1,871.00` | `0.0000` | `0.0000` | **100% MATCH (PASS)** |
| **Loss-Making Transaction (%)** | `18.72` | `18.72` | `18.72` | `0.0000` | `0.0000` | **100% MATCH (PASS)** |
| **Returned Orders Count** | `296.00` | `296.00` | `296.00` | `0.0000` | `0.0000` | **100% MATCH (PASS)** |
| **Overall Return Rate (%)** | `5.91` | `5.91` | `5.91` | `0.0000` | `0.0000` | **100% MATCH (PASS)** |

---

## 2. Dimensional Slicing & Sub-Aggregate Reconciliation

### Territory / Regional Breakdown (Sales & Profit)
* **Central Region:** SQL: `$501,239.76` / `$39,706.24` | Python: `$501,239.76` / `$39,706.24` | Power BI: `$501,239.76` / `$39,706.24` ➜ **100% MATCH**
* **East Region:** SQL: `$678,781.30` / `$91,522.50` | Python: `$678,781.30` / `$91,522.50` | Power BI: `$678,781.30` / `$91,522.50` ➜ **100% MATCH**
* **South Region:** SQL: `$391,721.83` / `$46,749.49` | Python: `$391,721.83` / `$46,749.49` | Power BI: `$391,721.83` / `$46,749.49` ➜ **100% MATCH**
* **West Region:** SQL: `$725,457.76` / `$108,418.31` | Python: `$725,457.76` / `$108,418.31` | Power BI: `$725,457.76` / `$108,418.31` ➜ **100% MATCH**
* **Regional Validation Status:** `PASSED - Zero Discrepancy`

### Annual Time Trajectory (Sales & Profit)
* **2015:** SQL: `$484,247.47` / `$49,543.86` | Python: `$484,247.47` / `$49,543.86` | Power BI: `$484,247.47` / `$49,543.86` ➜ **100% MATCH**
* **2016:** SQL: `$470,532.39` / `$61,618.44` | Python: `$470,532.39` / `$61,618.44` | Power BI: `$470,532.39` / `$61,618.44` ➜ **100% MATCH**
* **2017:** SQL: `$609,205.74` / `$81,794.90` | Python: `$609,205.74` / `$81,794.90` | Power BI: `$609,205.74` / `$81,794.90` ➜ **100% MATCH**
* **2018:** SQL: `$733,215.05` / `$93,439.34` | Python: `$733,215.05` / `$93,439.34` | Power BI: `$733,215.05` / `$93,439.34` ➜ **100% MATCH**
* **Annual Time Trajectory Validation Status:** `PASSED - Zero Discrepancy`

---

## 3. Methodological Significance for Analytics Portfolios

In enterprise data analytics, cross-tool reconciliation audits represent the ultimate litmus test for data reliability:
1. **Defends Against Inadvertent Filtering:** Proves that relationship propagation in the Power BI Star Schema does not drop records or create synthetic duplicate cartesian products.
2. **Eliminates Floating-Point Rounding Drift:** Guarantees that currency rounding at the line-item level perfectly aggregates to enterprise P&L totals.
3. **Validates Granularity Consistency:** Proves that distinct counts (`Order ID`, `Customer ID`) maintain integrity whether evaluated via SQL subqueries, Pandas `.nunique()`, or DAX `DISTINCTCOUNT()`.
