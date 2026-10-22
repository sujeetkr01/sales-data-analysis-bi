# Excel Cleaning & Data Transformation Documentation

**Project:** Global Superstore Sales Performance & Profitability Intelligence  
**Dataset:** US Superstore Sales  
**Generated Files:**  
* Cleaned Multi-Tab Workbook: `data/processed/Superstore_Cleaned.xlsx`  
* Staging Normalized Fact Table: `data/processed/orders_cleaned.csv`  
* Staging Dim Returns: `data/processed/returns_cleaned.csv`  
* Staging Dim People: `data/processed/people_cleaned.csv`  

---

## 1. Overview of Transformation Objectives
The goal of the Excel data cleaning phase is to transform an uncurated, vertically stacked export into a clean, relational star schema model ready for SQL warehousing and Power BI visualization.

---

## 2. Transformation Log & Formula Reference

### Transformation 1: Entity Separation (Multi-Sheet Normalization)
* **Problem:** Rows 1–9,994 were order line items, rows 9,995–9,998 were regional managers, and rows 10,000–10,800 were return logs.
* **Excel / Power Query Execution:**
  * In Excel Power Query (Get & Transform): Split source into 3 separate queries:
    1. `Orders`: Filter `[Row ID]` to keep numeric rows 1 to 9994.
    2. `People`: Filter rows where `[Row ID] = "Person"` down to row 9998, promote headers (`Person`, `Region`), rename columns to `Regional_Manager` and `Region`.
    3. `Returns`: Filter rows where `[Row ID] = "Returned"` down to end, promote headers (`Returned`, `Order ID`), and remove duplicates on `Order ID`.

### Transformation 2: Missing Postal Code Imputation
* **Problem:** 11 order records for **Burlington, Vermont** had blank postal codes (`NaN`).
* **Root Cause:** Burlington, VT has US ZIP code `05401`. Leading zero truncation in spreadsheet software often converts or drops `05401`.
* **Excel Formula (Column N):**
  ```excel
  =IF(AND(K2="Burlington", L2="Vermont", ISBLANK(M2)), "05401", TEXT(M2, "00000"))
  ```
* **Power Query M:**
  ```powerquery
  Table.ReplaceValue(#"PreviousStep", null, "05401", Replacer.ReplaceValue, {"Postal Code"})
  ```

### Transformation 3: Text Normalization & Trimming
* **Problem:** Inadvertent leading or trailing whitespaces from CSV parsing.
* **Excel Formula:**
  ```excel
  =TRIM(PROPER(G2))  // For Customer Name
  =TRIM(UPPER(F2))  // For Customer ID (e.g., CG-12520)
  ```

### Transformation 4: Date Parsing & Standardization
* **Problem:** Dates were formatted in US string format `MM/DD/YYYY`.
* **Resolution:** Parsed to standard ISO 8601 `YYYY-MM-DD` and formatted in Excel cells as `yyyy-mm-dd`.
* **Excel Formula:**
  ```excel
  =DATE(YEAR(C2), MONTH(C2), DAY(C2))
  ```

### Transformation 5: Unit Economics & Derived Metrics
To unlock business insights in SQL and Power BI, five analytical metrics were engineered:

1. **Shipping Lead Time (`Shipping_Days`):**
   ```excel
   =D2 - C2  // [Ship Date] - [Order Date] formatted as General Integer
   ```
2. **Unit Selling Price (`Unit_Price`):**
   ```excel
   =ROUND(R2 / S2, 2)  // [Sales] / [Quantity]
   ```
3. **Unit Manufacturing / Acquisition Cost (`Unit_Cost`):**
   ```excel
   =ROUND((R2 - U2) / S2, 2)  // ([Sales] - [Profit]) / [Quantity]
   ```
4. **Line-Item Profit Margin % (`Profit_Margin`):**
   ```excel
   =ROUND(U2 / R2, 4)  // [Profit] / [Sales] formatted as Percentage (0.00%)
   ```
5. **Return Status (`Is_Returned`):**
   ```excel
   =IF(ISNUMBER(XLOOKUP(B2, Returns!A:A, Returns!A:A)), "Yes", "No")
   ```
6. **Regional Leadership (`Regional_Manager`):**
   ```excel
   =XLOOKUP(N2, People!A:A, People!B:B, "Unassigned")
   ```

---

## 3. Data Transformation Audit Matrix

| Metric | Raw Dataset | Processed Dataset | Variance / Delta |
|---|---|---|---|
| **Total Rows (Fact Table)** | 10,800 | **9,994** | -806 (Separated into Dim tables) |
| **Returns Dimension Rows** | 800 (stacked) | **296** (unique) | Deduplicated order keys |
| **People Dimension Rows** | 4 (stacked) | **4** (normalized) | Clean regional manager lookup |
| **Missing Postal Codes** | 11 | **0** | Imputed Burlington, VT (`05401`) |
| **Postal Code Format** | Float (e.g. `90036.0`) | **5-digit Text (`00000`)** | Preserved leading zeroes |
| **Total Sales Volume** | `$2,297,200.65` | **`$2,297,200.65`** | $0.00 delta (Exact match) |
| **Total Net Profit** | `$286,396.54` | **`$286,396.54`** | $0.00 delta (Exact match) |
| **Blended Profit Margin** | 12.467% | **12.47%** | Precision preserved |
| **Loss-Making Transactions** | 1,871 | **1,871** | Validated (18.72% of orders) |
| **Total Line Items Returned** | N/A (unlinked) | **800** | 8.00% return rate across line items |
