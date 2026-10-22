# Power BI DAX Measures, Date Dimension, Slicers & Interactivity Guide

**File Location:** `powerbi/01_dax_measures.dax`  
**Data Model:** Kimball Star Schema (`Fact_Orders` + 6 Dimensions)  
**Measures Table:** `_Measures` (Dedicated measure storage table)  

---

## 1. Date Dimension Setup & Sort-By-Column Configuration

A robust Date Table is essential to prevent time-intelligence calculation bugs (such as incorrect leap-year alignments or sorting errors).

### Date Table DAX Formula
```dax
Dim_Date = 
ADDCOLUMNS (
    CALENDAR ( DATE ( 2015, 1, 1 ), DATE ( 2018, 12, 31 ) ),
    "Date_Key", INT ( FORMAT ( [Date], "YYYYMMDD" ) ),
    "Year", YEAR ( [Date] ),
    "Quarter", "Q" & FORMAT ( [Date], "Q" ),
    "Year_Quarter", YEAR ( [Date] ) & "-Q" & FORMAT ( [Date], "Q" ),
    "Month_Num", MONTH ( [Date] ),
    "Month_Name", FORMAT ( [Date], "MMMM" ),
    "Month_Short", FORMAT ( [Date], "mmm" ),
    "Year_Month", FORMAT ( [Date], "YYYY-MM" ),
    "Month_Year_Short", FORMAT ( [Date], "mmm YYYY" ),
    "Week_Num", WEEKNUM ( [Date], 2 ),
    "Day_of_Month", DAY ( [Date] ),
    "Day_of_Week", FORMAT ( [Date], "dddd" ),
    "Day_of_Week_Short", FORMAT ( [Date], "ddd" ),
    "Day_of_Week_Num", WEEKDAY ( [Date], 2 ),
    "Is_Weekend", IF ( WEEKDAY ( [Date], 2 ) >= 6, "Yes", "No" )
)
```

### Essential Power BI Modeling Settings:
1. **Mark as Date Table:** Right-click `Dim_Date` ➜ **Mark as date table** ➜ Select `[Date]`.
2. **Sort by Column Assignments:**
   * Select `[Month_Short]` ➜ Go to **Column Tools** ➜ **Sort by Column** ➜ Select `[Month_Num]`.
   * Select `[Month_Name]` ➜ **Sort by Column** ➜ Select `[Month_Num]`.
   * Select `[Month_Year_Short]` ➜ **Sort by Column** ➜ Select `[Year_Month]`.
   * Select `[Day_of_Week_Short]` ➜ **Sort by Column** ➜ Select `[Day_of_Week_Num]`.

---

## 2. Core DAX Measure Catalog

### Base Financial & Operational Measures
| Measure Name | DAX Expression | Format | Purpose |
|---|---|---|---|
| `[Total Sales]` | `SUM(Fact_Orders[Sales])` | `$#,##0.00` | Primary top-line revenue metric. |
| `[Total Profit]` | `SUM(Fact_Orders[Profit])` | `$#,##0.00` | Net operating bottom-line earnings. |
| `[Total Cost]` | `[Total Sales] - [Total Profit]` | `$#,##0.00` | Total cost of inventory and discounts. |
| `[Profit Margin %]` | `DIVIDE([Total Profit], [Total Sales], 0)` | `0.00%` | Operational profitability hurdle. |
| `[Total Orders]` | `DISTINCTCOUNT(Fact_Orders[Order ID])` | `#,##0` | Distinct purchasing baskets. |
| `[Total Items Sold]` | `COUNTROWS(Fact_Orders)` | `#,##0` | Total fulfilled line items. |
| `[Total Quantity]` | `SUM(Fact_Orders[Quantity])` | `#,##0` | Physical units dispatched. |
| `[Average Order Value]` | `DIVIDE([Total Sales], [Total Orders], 0)` | `$#,##0.00` | Basket monetization size. |
| `[Average Discount %]` | `AVERAGE(Fact_Orders[Discount])` | `0.0%` | Depth of promotional concessions. |

---

### Time Intelligence & Growth Measures
| Measure Name | DAX Expression | Business Rationale |
|---|---|---|
| `[Sales PY]` | `CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Dim_Date[Date]))` | Baseline revenue from equivalent historical window. |
| `[Sales YoY $]` | `IF(NOT(ISBLANK([Sales PY])), [Total Sales] - [Sales PY], BLANK())` | Dollar growth variance vs prior year. |
| `[Sales YoY %]` | `DIVIDE([Sales YoY $], [Sales PY], BLANK())` | Annual top-line percentage growth trajectory. |
| `[Profit PY]` | `CALCULATE([Total Profit], SAMEPERIODLASTYEAR(Dim_Date[Date]))` | Prior year net profit baseline. |
| `[Profit YoY %]` | `DIVIDE([Total Profit] - [Profit PY], [Profit PY], BLANK())` | Annual profit growth rate. |
| `[Sales MoM %]` | `VAR PM = CALCULATE([Total Sales], DATEADD(Dim_Date[Date], -1, MONTH)) RETURN DIVIDE([Total Sales] - PM, PM, BLANK())` | Monthly operational velocity. |
| `[Cumulative Sales Running Total]` | `CALCULATE([Total Sales], FILTER(ALLSELECTED(Dim_Date), Dim_Date[Date] <= MAX(Dim_Date[Date])))` | YTD day-by-day revenue accumulation. |

---

### Inactive Relationships & Operational Risk Measures
| Measure Name | DAX Expression | Technical Demonstration |
|---|---|---|
| `[Sales by Ship Date]` | `CALCULATE([Total Sales], USERELATIONSHIP(Fact_Orders[Ship Date], Dim_Date[Date]))` | Uses inactive relationship to analyze fulfillment timing rather than order placement timing. |
| `[Average Shipping Days]` | `AVERAGE(Fact_Orders[Shipping_Days])` | Fulfillment SLA performance tracking. |
| `[Loss-Making Orders Count]` | `CALCULATE(COUNTROWS(Fact_Orders), Fact_Orders[Profit] < 0)` | Identifies transactions destroying equity. |
| `[Loss-Making Line %]` | `DIVIDE([Loss-Making Orders Count], [Total Items Sold], 0)` | Percentage of catalog items operating at a loss (18.72%). |
| `[Return Rate %]` | `DIVIDE(CALCULATE(DISTINCTCOUNT(Fact_Orders[Order ID]), Fact_Orders[Is_Returned] = "Yes"), [Total Orders], 0)` | Ratio of returned orders to fulfilled orders (5.91%). |

---

## 3. Slicer Strategy & Synchronization Across Pages

To create a cohesive user experience across all 4 pages:

1. **Global Slicers:**
   * **Date Slicer:** `Dim_Date[Date]` rendered as a **Between Date Slider** or **Year Tile Button Slicer**.
   * **Region Slicer:** `Dim_Geography[Region]` rendered as a **Horizontal Button Pill Slicer** (`Central`, `East`, `South`, `West`).
   * **Category Slicer:** `Dim_Products[Category]` rendered as a **Dropdown Menu**.
2. **Sync Slicers Configuration:**
   * In Power BI Desktop: Go to **View ➜ Sync Slicers**.
   * Check both **Sync** (refresh icon) and **Visible** (eye icon) for all 4 pages (`Executive`, `Product`, `Customer`, `Logistics`).
   * Selecting `West` on Page 1 will immediately filter Pages 2, 3, and 4 without requiring the user to re-filter.

---

## 4. Drill-Through Setup (Sub-Category to SKU Deep Dive)

1. Create a dedicated hidden detail page named **`Product Detail Drill-Through`**.
2. Add a KPI card displaying `[Total Sales]`, `[Total Profit]`, `[Profit Margin %]`, and a table visual listing:
   * `Product Name`, `Sales`, `Quantity`, `Discount`, `Profit`, `Margin %`.
3. In the **Visualizations** pane for this page, expand **Drill-through filters**:
   * Drag `Dim_Products[Sub-Category]` into the **Add drill-through fields here** box.
4. **User Workflow:** On Page 2, a user right-clicks the loss-making bar for `Tables` ➜ Selects **Drill-through ➜ Product Detail Drill-Through** ➜ Immediately views all 319 individual table transactions to inspect SKU-level pricing and discounting errors.

---

## 5. Report Page Tooltips Setup (Monthly Run-Rate Hover)

1. Create a mini canvas page named **`Tooltip - Monthly Health`**:
   * Page Information: Toggle **Allow use as tooltip** to **On**.
   * Page Size: Custom (`320 x 240` px).
2. Insert a mini bar chart displaying `Top 3 Selling Sub-Categories` and a gauge visual of `[Profit Margin %]`.
3. On Page 1, select the **Monthly Sales & Profit Trend** chart:
   * Go to **Format Visual ➜ General ➜ Tooltips**.
   * Type: **Report page**.
   * Page: Select **`Tooltip - Monthly Health`**.
4. **User Workflow:** Hovering over any data point (e.g. November 2018) reveals an instant mini-breakdown of the exact sub-categories driving that month's surge.
