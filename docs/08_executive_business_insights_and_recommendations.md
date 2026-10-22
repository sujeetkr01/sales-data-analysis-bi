# Executive Business Intelligence Findings & Strategic Recommendations

**Project:** Global Superstore Performance & Profitability Analysis  
**Data Scope:** 9,994 transactions across 4 fiscal years (2015–2018)  
**Total Revenue:** $2,297,200.65 | **Total Profit:** $286,396.54 | **Margin:** 12.47%  

---

## Executive Summary

Through our integrated SQL warehousing, Python statistical modeling, and Power BI diagnostic dashboards, we uncovered five major operational vulnerabilities and commercial growth levers. Left unaddressed, discount leakage, regional pricing disparities, and loss-making product lines cost the business an estimated **~$157,000+ in lost earnings**.

---

## Finding 1: The 20% Promotional Discount Cliff (Severe Margin Destruction)

### 1. Verified Empirical Evidence
By bucketing all 9,994 transactions into promotional discount tiers, we proved that discount depth does not follow a linear margin decay; it exhibits an abrupt **cliff at 20% discount**:

| Promotional Tier | Order Lines | Gross Sales | Net Profit / Loss | Realized Margin | Loss Order Count | Loss Order % |
|:---|---:|---:|---:|---:|---:|---:|
| **1. Full Price (0%)** | 4,798 | $1,087,908.47 | **+$320,987.01** | **+29.50%** | 0 | **0.00%** |
| **2. Moderate Promo (1–20%)** | 3,803 | $846,522.11 | **+$100,785.81** | **+11.91%** | 523 | **13.75%** |
| **3. Aggressive Promo (21–40%)** | 460 | $234,137.95 | **-$35,817.54** | **-15.30%** | 415 | **90.22%** |
| **4. Clearance (>40%)** | 933 | $128,632.12 | **-$99,558.74** | **-77.40%** | 933 | **100.00%** |

### 2. Business Implications
* Promotional discounting between 1% and 20% acts as a viable sales driver, yielding **+$100.8K** in net profit.
* However, once discounts exceed 20%, **90.2% of orders lose money**.
* Discounts above 40% are 100% destructive: every single transaction destroys capital, burning **-$99,558.74**.
* Total equity burned across tiers 3 and 4: **`-$135,376.28`**.

### 3. Actionable Strategic Recommendations
* **ERP Hard Discount Governance:** Configure the CRM/ERP order checkout system to enforce a hard cap of 20% discount for field sales representatives.
* **VP Approval Workflows:** Any contractual discount between 21% and 30% must require automated sign-off from the Regional Director.
* **Abolish Blanket >40% Clearance Markdowns:** Discontinue 50–80% clearance sales on high-cost manufactured hardware; liquidate remaining distressed stock through bundled B2B wholesale liquidators instead of retail channels.
* **Estimated Annual Profit Recovery:** **+$45,000 – $65,000 / year**.

---

## Finding 2: Systemic Product Drag in Furniture (`Tables` & `Bookcases`)

### 1. Verified Empirical Evidence
While the overall business achieves a 12.47% margin, exactly three sub-categories operate at a net financial loss across the multi-year history:

| Sub-Category | Parent Category | Order Count | Gross Sales | Net Profit / Loss | Profit Margin % | Primary Driver |
|:---|:---|---:|---:|---:|---:|:---|
| **Tables** | Furniture | 319 | $206,965.53 | **-$17,725.57** | **-8.56%** | High bulky freight costs & average 26.1% discount. |
| **Bookcases** | Furniture | 228 | $114,879.98 | **-$3,472.59** | **-3.02%** | Flatpack transit damage and discount erosion. |
| **Supplies** | Office Supplies | 190 | $46,673.52 | **-$1,189.08** | **-2.55%** | Underpriced commercial cutting/binding tools. |
| **Total Drag** | — | **737** | **$368,519.03** | **-$22,387.24** | **-6.07%** | **$22.4K capital drain** |

*In contrast, `Copiers` generated **+$55,617.88 profit (37.20% margin)** on just 68 sales, and `Paper` generated **+$34,053.11 profit (43.39% margin)**.*

### 2. Business Implications
Furniture represents **$321,845 in sales** that actively drains company equity. The business is subsidizing heavy, bulky tables and bookcases with high margins earned from office paper and copiers.

### 3. Actionable Strategic Recommendations
* **Unbundle Freight & Assembly:** Eliminate free delivery on bulky Furniture items. Introduce mandatory flat-rate shipping surcharges for `Tables` and `Bookcases`.
* **SKU Rationalization:** Discontinue the bottom 5 loss-making table models (such as `Chromcraft Bull-Nose Wood Oval Conference Tables`, which lost -$2,876.11 alone).
* **Switch to Drop-Ship / Made-to-Order:** Transition tables and conference furnishings from pre-stocked warehouse inventory to just-in-time direct supplier fulfillment.
* **Estimated Annual Profit Recovery:** **+$18,000 – $22,000 / year**.

---

## 3. Finding 3: Central Region Profit Compression & Discount Over-Reliance

### 1. Verified Empirical Evidence
Comparing regional performance against territory leadership reveals a major profitability deficit in the Central Region:

| Region | Regional Manager | Total Sales | Total Profit | Realized Margin | Avg Discount % | Profit Rank |
|:---|:---|---:|---:|---:|---:|:---:|
| **West** | Anna Andreadi | $725,457.76 | **$108,418.31** | **14.94%** | **10.9%** | **1** |
| **East** | Chuck Magee | $678,781.30 | **$91,522.50** | **13.48%** | **14.5%** | **2** |
| **South** | Cassandra Brandow | $391,721.83 | **$46,749.49** | **11.93%** | **14.7%** | **3** |
| **Central** | Kelly Williams | $501,239.76 | **$39,706.24** | **7.92%** | **24.0%** | **4** |

*Drilling into state performance reveals that **Texas** (Central Region) generated **-$25,729.39 in net losses** and **Illinois** generated **-$12,607.89 in losses** due to average discounts exceeding 37%.*

### 2. Business Implications
The Central Region generated over **half a million dollars in revenue ($501K)**, yet converted barely **7.92%** into operating profit—nearly half the conversion efficiency of Anna Andreadi's West Region (14.94%). Central sales representatives are winning revenue by giving away margin.

### 3. Actionable Strategic Recommendations
* **Restructure Sales Commission Structures:** Shift sales incentives from gross revenue quotas to **Gross Margin Contribution ($)**. Sales representatives discounting above 15% should see commission payouts reduced proportionately.
* **Targeted Pricing Interventions in Texas & Illinois:** Review state-level pricing contracts. Eliminate the automated promotional allowances currently active in Texas.
* **Margin Parity Target:** If Central increases its realized margin from 7.92% to the company average of 12.47%, it generates an immediate **+$22,806 in incremental net profit** on existing volume.

---

## 4. Finding 4: The Top-Customer Revenue Mirage (Sean Miller Case Study)

### 1. Verified Empirical Evidence
Evaluating customer accounts purely by top-line spend creates dangerous operational misalignments:

| Customer Name | Segment | Total Orders | Total Items | Gross Revenue | Net Profit Contribution | Net Margin % | Customer Health |
|:---|:---|---:|---:|---:|---:|---:|:---:|
| **Sean Miller** | Home Office | 5 | 15 | **$25,043.07** | **-$1,980.75** | **-7.91%** | **Capital Drain** |
| **Tamara Chand** | Corporate | 5 | 12 | **$19,052.22** | **+$8,981.32** | **+47.14%** | **Tier 1 Cash Cow** |
| **Raymond Buch** | Consumer | 6 | 18 | **$15,117.35** | **+$6,976.09** | **+46.15%** | **Tier 1 Cash Cow** |
| **Tom Ashbrook** | Home Office | 4 | 10 | **$14,595.62** | **+$4,703.80** | **+32.23%** | **Healthy Account** |
| **Adrian Barton** | Consumer | 10 | 20 | **$14,473.56** | **+$5,444.81** | **+37.62%** | **Healthy Account** |

### 2. Business Implications
* Sean Miller is celebrated in raw sales reports as the **#1 Customer by Revenue ($25.0K)**.
* In reality, servicing Sean Miller destroyed **-$1,980.75 in cash** because his transactions received steep 50%+ discounts on expensive hardware.
* Conversely, Tamara Chand generated **$8,981 in pure profit (47.1% margin)** on lower gross spend.

### 3. Actionable Strategic Recommendations
* **Implement Customer Health & Margin Scoring:** Replace simple "Top Spender" leaderboards with a **Profit-Contribution Quadrant** in Power BI.
* **Account-Level Minimum Margin Hurdles:** Flag Sean Miller's account in CRM. Future purchase quotes must maintain a minimum 15% realized gross margin.
* **White-Glove VIP Treatment for True Cash Cows:** Allocate dedicated account management and executive perks to high-margin accounts like Tamara Chand and Raymond Buch.

---

## 5. Finding 5: Return Rate Spikes in Expedited Technology Logistics

### 1. Verified Empirical Evidence
While the baseline corporate return rate is modest at **5.91%** (296 of 5,009 orders), cross-analyzing product categories against fulfillment modes reveals a distinct vulnerability:

| Category | Fulfillment Mode | Total Orders | Returned Orders | Return Rate % | Revenue Impact ($) |
|:---|:---|---:|---:|---:|---:|
| **Technology** | **Same Day** | 79 | 10 | **12.66%** | $8,077.42 |
| **Technology** | **First Class** | 250 | 26 | **10.40%** | $23,761.85 |
| **Furniture** | First Class | 274 | 23 | **8.39%** | $9,159.17 |
| **Office Supplies** | Standard Class | 2,248 | 132 | **5.87%** | $27,614.08 |

### 2. Business Implications
Technology orders dispatched via Same Day and First Class shipping experience **double the baseline return rate (10.4% – 12.7%)**. Expedited transit of complex electronics leads to buyer remorse, order misconfiguration, or transit handling damage. Furthermore, processing returns on high-ticket tech items incurs expensive return logistics and restocking depreciation.

### 3. Actionable Strategic Recommendations
* **Automated Pre-Dispatch Order Verification:** Implement an automated SMS/email configuration check for Same Day tech orders above $500 before the parcel leaves the depot.
* **Carrier Packaging Audit:** Conduct packaging audits for expedited carriers to prevent hardware transit shock.
* **Restocking Fee Policy:** Introduce a standard 10% restocking fee on returned expedited hardware to curb impulsive purchases and offset processing expenses.
* **Estimated Annual Profit Recovery:** **+$12,000 / year**.

---

## Synthesis of Financial Impact

| Strategic Initiative | Root Cause Addressed | Annual Profit Recovery Target |
|---|---|---|
| **1. Enforce 20% Discount Ceiling** | Severe losses on orders with >20% discount | **+$45,000 – $65,000** |
| **2. Restructure Central Region Sales Incentives** | Central discount over-reliance (24.0% avg discount) | **+$20,000 – $25,000** |
| **3. Unbundle Bulky Furniture Freight & Cut Loss SKUs** | Tables & Bookcases negative cumulative margin (-$21.2K) | **+$18,000 – $22,000** |
| **4. Account Margin Hurdles on High-Volume Buyers** | Top spenders operating as loss leaders (Sean Miller) | **+$8,000 – $12,000** |
| **5. Expedited Tech Hardware Return Mitigation** | 12.66% return spike on Same Day tech orders | **+$10,000 – $12,000** |
| **Total Annual Enterprise Value Added** | — | **+$101,000 – $136,000** |
