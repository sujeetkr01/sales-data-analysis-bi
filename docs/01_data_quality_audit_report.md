# Data Quality, Schema & Hygiene Audit Report

**Target File:** `data/raw/Sample_Superstore_Raw.csv`  
**Execution Date:** 2026-10-23  
**Status:** Completed - Baseline Validated  

---

## 1. File Structure & Entity Boundaries
The raw export file contains multiple tabular entities stacked vertically:
* **Total Raw File Rows:** 10,800 rows across 21 columns.
* **Primary Transactions (`Orders`):** Rows `1` to `9,994` (9,994 rows).
* **Metadata Sheet 1 (`People` / Regional Managers):** Rows `9,995` to `9,998` (4 rows).
* **Metadata Sheet 2 (`Returns`):** Rows `10,000` to `10,800` (800 rows, representing 296 unique returned orders).

---

## 2. Orders Completeness & Missing Values
Audit performed on the primary 9,994 transaction rows:

| Metric | Result | Impact & Root Cause |
|---|---|---|
| Total Primary Rows | 9,994 | Matches standard US Superstore benchmark. |
| Fully Populated Columns | 20 of 21 | High baseline data completeness (95.2%). |
| Missing `Postal Code` | 11 rows (0.11%) | All 11 missing records belong to `City = Burlington`, `State = Vermont`. US ZIP code for Burlington is `05401`. |
| Missing Other Attributes | 0 rows (0.00%) | Zero missing values across Sales, Profit, Dates, and IDs. |

---

## 3. Duplicate Analysis
* **Full Duplicate Rows:** `0` (Zero duplicate rows across all 21 columns).
* **Duplicate `Row ID`:** `0` (Every transaction line item has a strictly unique sequential integer ID).
* **Multi-Line Order Distribution:** 
  * Total Distinct Orders: `5,009`
  * Average items per order: `2.00` items
  * Max items in single order: `14` items

---

## 4. Temporal & Chronological Validity
* **Order Date Span:** `2015-01-03` to `2018-12-30` (4 complete calendar years: 2015–2018).
* **Ship Date Span:** `2015-01-07` to `2019-01-05`.
* **Temporal Sequence Violations (`Ship Date < Order Date`):** `0`.
* **Logistics Transit Duration:** Min `0` days, Max `7` days, Mean `3.96` days.

---

## 5. Statistical & Business Logic Sanity Checks
* **Sales Revenue Range:** `$0.44` to `$22,638.48` (Mean: `$229.86`). Zero or negative sales: `0`.
* **Order Quantities:** Min `1`, Max `14` units. Zero or negative quantities: `0`.
* **Promotional Discount Range:** `0%` to `80%` (Mean: `15.6%`).
* **Profit Distribution:** Min `$-6,599.98` to Max `$8,399.98` (Mean: `$28.66`).
* **Loss-Making Transactions:** Exactly `1,871` rows (18.72% of all line items) generate a net financial loss, demonstrating high discount sensitivity.

---

## 6. Relational Entity Profiling

### Regional Managers (`People`)
| Regional Manager | Assigned Territory |
|---|---|
| Anna Andreadi | West |
| Chuck Magee | East |
| Kelly Williams | Central |
| Cassandra Brandow | South |

### Returns Tracking (`Returns`)
* Total Raw Return Entries: `800`
* Distinct Returned Orders: `296` (504 rows are duplicate order lines created during line-item level logging).
* Referential Integrity: `800 / 800` (100% of returned orders exist within the Orders table).
