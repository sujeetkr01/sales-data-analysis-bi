# Power BI Multi-Page Dashboard Architecture & Design Specification

**Project:** Global Superstore Sales Performance & Profitability Intelligence  
**Role:** Senior Power BI Developer & Data Architect  
**Model Architecture:** Kimball Star Schema (Single-direction 1:Many relationships)  
**Model Data Path:** `powerbi/model_data/`  
**Canvas Resolution:** 16:9 Standard (`1280 x 720` px or `1920 x 1080` px)  

---

## 1. Relational Star Schema Model & Relationship Diagram

```
       ┌─────────────────────────┐
       │      Dim_Managers       │
       ├─────────────────────────┤
       │ Region (PK)             │
       │ Regional_Manager        │
       └────────────┬────────────┘
                    │ 1:N
                    ▼
       ┌─────────────────────────┐         ┌─────────────────────────┐
       │      Dim_Geography      │         │      Dim_Customers      │
       ├─────────────────────────┤         ├─────────────────────────┤
       │ Postal Code (PK)        │         │ Customer ID (PK)        │
       │ City, State, Region     │         │ Customer Name, Segment  │
       └────────────┬────────────┘         └────────────┬────────────┘
                    │ 1:N                               │ 1:N
                    ▼                                   ▼
       ┌─────────────────────────────────────────────────────────────┐
       │                         Fact_Orders                         │
       ├─────────────────────────────────────────────────────────────┤
       │ Row ID (PK)                                                 │
       │ Order ID (FK) ──────────────► Dim_Returns [Order ID] (1:1)  │
       │ Order Date (FK) ────────────► Dim_Date [Date] (Active 1:N)  │
       │ Ship Date (FK)  ────────────► Dim_Date [Date] (Inactive 1:N)│
       │ Customer ID (FK), Product ID (FK), Postal Code (FK)         │
       │ Sales, Quantity, Discount, Profit, Shipping_Days            │
       └─────────────────────────────┬───────────────────────────────┘
                                     │ 1:N
                                     ▼
                        ┌─────────────────────────┐
                        │      Dim_Products       │
                        ├─────────────────────────┤
                        │ Product ID (PK)         │
                        │ Category, Sub-Category  │
                        │ Product Name            │
                        └─────────────────────────┘
```

### Relationship Configuration Rules:
1. `Dim_Date[Date]` ➜ `Fact_Orders[Order Date]`: **1 to Many (1:*), Single Direction (Active)**.
2. `Dim_Date[Date]` ➜ `Fact_Orders[Ship Date]`: **1 to Many (1:*), Single Direction (Inactive)** — activated via DAX `USERELATIONSHIP()`.
3. `Dim_Customers[Customer ID]` ➜ `Fact_Orders[Customer ID]`: **1 to Many (1:*), Single Direction**.
4. `Dim_Products[Product ID]` ➜ `Fact_Orders[Product ID]`: **1 to Many (1:*), Single Direction**.
5. `Dim_Geography[Postal Code]` ➜ `Fact_Orders[Postal Code]`: **1 to Many (1:*), Single Direction**.
6. `Dim_Managers[Region]` ➜ `Dim_Geography[Region]`: **1 to Many (1:*), Single Direction**.
7. `Dim_Returns[Order ID]` ➜ `Fact_Orders[Order ID]`: **1 to Many (1:*), Single Direction**.

---

## 2. Design System & Corporate Color Palette

* **Primary Dark (Headers & Text):** Deep Midnight Navy (`#1A2530`)
* **Primary Accent (Sales & Brand):** Slate Blue (`#2B6CB0`)
* **Success / Positive Profit:** Emerald Forest (`#27AE60`)
* **Warning / Alert:** Amber Gold (`#F39C12`)
* **Danger / Loss-Making / Returns:** Crimson Coral (`#E74C3C`)
* **Neutral Background Canvas:** Off-White Gray (`#F8F9FA`)
* **Container Cards:** Pure White (`#FFFFFF`) with 1px border (`#E2E8F0`) and 4px corner radius.

---

## 3. Four-Page Dashboard Blueprints & Layout Specifications

### PAGE 1: Executive KPI & Strategic Overview
**Target Audience:** Chief Executive Officer (CEO), Chief Commercial Officer (CCO), VP of Sales.  
**Core Objective:** High-level executive pulse check on gross revenue, net margin, order volume, and territory health.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ GLOBAL HEADER: Sales & Profit Intelligence Dashboard | Filters: [Year] [Region] [Cat]  │
├──────────────┬──────────────┬──────────────┬──────────────┬────────────────────────────┤
│ Total Sales  │ Net Profit   │ Net Margin % │ Total Orders │ Average Order Value (AOV)  │
│  $2,297,201  │   $286,397   │    12.47%    │    5,009     │          $458.61           │
│  ▲ +20.4% YoY│  ▲ +14.2% YoY│  ▼ -0.69% YoY│  ▲ +28.3% YoY│         ▼ -6.2% YoY        │
├──────────────┴──────────────┴──────────────┴──────────────┴────────────────────────────┤
│ VISUAL 1 (Left 60%): Monthly Sales & Profit Trend (Combo Area / Line Chart)            │
│   - X-Axis: Dim_Date[Year_Month]                                                       │
│   - Y-Axis 1 (Bar/Area): [Total Sales] ($)                                             │
│   - Y-Axis 2 (Line): [Total Profit] ($)                                                │
│   - Tooltip: Prior Year Sales, YoY Growth %, Profit Margin %                           │
├─────────────────────────────────────────────┬──────────────────────────────────────────┤
│ VISUAL 2 (Right Top 20%): Margin by Region  │ VISUAL 3 (Right Bottom 20%): Sales by    │
│   - Horizontal Bar: Dim_Geography[Region]   │ Category & Segment (100% Stacked Bar)    │
│   - Value: [Profit Margin %]                │   - X-Axis: Dim_Products[Category]       │
│   - Benchmark Line: Corporate Avg (12.47%)  │   - Legend: Dim_Customers[Segment]       │
│   - Data Labels: West 14.9%, Central 7.9%   │   - Value: [Total Sales]                 │
└─────────────────────────────────────────────┴──────────────────────────────────────────┘
```

---

### PAGE 2: Product Performance & Profitability Deep-Dive
**Target Audience:** Product Line Managers, Merchandising Directors, Pricing Analysts.  
**Core Objective:** Identify product margin drivers, uncover loss-making sub-categories, and diagnose SKU pricing flaws.

* **Top Mini-KPI Row:**
  * Top Margin Category: **Technology ($145,455 Profit / 17.4% Margin)**
  * Loss-Making Sub-Categories: **3 Sub-Categories (`Tables`, `Bookcases`, `Supplies`)**
  * Maximum SKU Loss: **-$8,880 (`Cubify CubeX 3D Printer`)**
* **Visual 1 (Top Left): Sub-Category Profitability Divergence (Divergent Bar Chart)**
  * *Y-Axis:* `Dim_Products[Sub-Category]` (17 items, sorted descending by Profit).
  * *X-Axis:* `[Total Profit]`.
  * *Color Rule:* Positive = Emerald (`#27AE60`), Negative = Crimson (`#E74C3C`).
  * *Callout:* Clearly exposes `Tables` (-$17.7K) and `Bookcases` (-$3.5K).
* **Visual 2 (Top Right): 4-Quadrant Margin vs. Sales Scatter Plot**
  * *X-Axis:* `[Total Sales]` (Log or Linear scale).
  * *Y-Axis:* `[Profit Margin %]`.
  * *Size:* `[Total Units Sold]`.
  * *Quadrant Dividers:* X-Ref Line = Median Sales ($30K), Y-Ref Line = 0.00% Margin.
  * *Quadrants:* **Cash Cows** (Top Right), **Loss Traps** (Bottom Right), **Volume Builders** (Top Left), **Review/Discontinue** (Bottom Left).
* **Visual 3 (Bottom): SKU Leaderboard Matrix (Drill-Through Target)**
  * Columns: `Product Name`, `Sub-Category`, `Units Sold`, `Gross Sales`, `Avg Discount %`, `Net Profit`, `Margin %`.
  * Slicer Toggle: **[Top 10 Profitable SKUs]** vs. **[Worst 10 Loss-Making SKUs]**.

---

### PAGE 3: Customer Segmentation & Regional Territory Scorecard
**Target Audience:** VP of Sales, Regional Directors (Anna Andreadi, Chuck Magee, Kelly Williams, Cassandra Brandow).  
**Core Objective:** Territory revenue allocation, customer account health, and sales representative accountability.

* **Visual 1 (Left 50%): US Geographic State Profitability Map**
  * *Map Type:* Shape Map or Filled Bubble Map of Continental US States.
  * *Bubble Size:* `[Total Sales]`.
  * *Color Saturation:* `[Profit Margin %]` (Divergent palette: Red for negative states like Texas & Ohio, Blue/Green for California & New York).
* **Visual 2 (Top Right): Regional Leadership Scorecard Table**
  * Columns: `Region`, `Regional Manager`, `Orders`, `Sales`, `Profit`, `Margin %`, `Avg Discount %`.
  * Conditional Formatting: Highlight Central Region's 24.0% discount rate in light red.
* **Visual 3 (Bottom Right): Customer Lifetime Value (CLV) & Top Accounts**
  * Clustered Bar: `Customer Name` (Top 10 by Sales).
  * Dual-Measure: `[Total Sales]` vs. `[Total Profit]`.
  * *Callout:* Highlights account anomaly **Sean Miller** ($25K revenue, -$1,981 loss) vs **Tamara Chand** ($19K revenue, +$8,981 profit).

---

### PAGE 4: Time Trends, Seasonality & Fulfillment Logistics
**Target Audience:** Supply Chain Operations, Warehouse Directors, Customer Experience Leads.  
**Core Objective:** Transit SLA adherence, carrier performance, holiday seasonality, and return rate drivers.

* **Visual 1 (Top Left): Annual Month-over-Month Seasonality Heatmap**
  * *Rows:* `Dim_Date[Month_Short]` (Jan–Dec).
  * *Columns:* `Dim_Date[Year]` (2015, 2016, 2017, 2018).
  * *Cell Values:* `[Total Sales]`.
  * *Finding:* Visualizes steady Q4 November/December revenue peaks across all four operating years.
* **Visual 2 (Top Right): Logistics Fulfillment SLA Analysis**
  * Clustered Bar: `Fact_Orders[Ship Mode]` (`Same Day`, `First Class`, `Second Class`, `Standard Class`).
  * Measures: `[Avg Shipping Days]` (Bar) vs. `[Shipping SLA Target Days]` (Reference Line).
* **Visual 3 (Bottom Left): Return Rate % by Product Category & Logistics Mode**
  * 100% Stacked Bar or Matrix: Identifies highest return rate cluster: **Technology via Same Day Shipping (12.66% return rate)**.
* **Visual 4 (Bottom Right): Cumulative Running Total Sales (YTD vs Prior Year YTD)**
  * Area / Line chart tracking cumulative day-by-day revenue progression.

---

## 4. UI/UX Interaction Model & Filter Hierarchy

1. **Global Canvas Slicers (Synchronized across all 4 pages):**
   * `Date Range Slider` (Dim_Date[Date])
   * `Region Dropdown` (Dim_Geography[Region])
   * `Product Category Tiles` (Dim_Products[Category])
2. **Cross-Filtering:** Selecting any Region or Category automatically cross-highlights related visuals on that page.
3. **Drill-Through Workflow:**
   * Right-click on any Sub-Category (e.g., `Tables`) ➜ **Drill-through ➜ Product SKU Deep-Dive**.
   * Right-click on any Customer (e.g., `Sean Miller`) ➜ **Drill-through ➜ Customer Order History**.
4. **Dynamic Tooltips:** Hovering over any monthly data point displays a mini-visual tooltip containing the top 3 selling sub-categories for that month.
