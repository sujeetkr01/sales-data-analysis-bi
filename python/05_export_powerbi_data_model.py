"""
=============================================================================
STEP 6: POWER BI STAR SCHEMA DATA MODEL EXPORTER
Script: python/05_export_powerbi_data_model.py
Description: Generates clean, normalized dimensional tables (Kimball Star Schema)
             optimized for VertiPaq storage and Power BI relationships.
=============================================================================
"""

import os
import pandas as pd

def build_powerbi_star_schema(orders_path: str, date_path: str, output_dir: str):
    print("=" * 70)
    print("STEP 6: EXPORTING POWER BI STAR SCHEMA DATA MODEL")
    print(f"Reading from: {orders_path}")
    print(f"Target Directory: {output_dir}")
    print("=" * 70)

    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(orders_path, dtype={'Postal Code': str})

    # 1. Dim Customers (1:N with Fact Orders)
    dim_customers = df[['Customer ID', 'Customer Name', 'Segment']].drop_duplicates(subset=['Customer ID']).reset_index(drop=True)
    dim_customers_path = os.path.join(output_dir, 'Dim_Customers.csv')
    dim_customers.to_csv(dim_customers_path, index=False)
    print(f" -> Exported Dim_Customers: {len(dim_customers)} rows")

    # 2. Dim Products (1:N with Fact Orders)
    dim_products = df[['Product ID', 'Category', 'Sub-Category', 'Product Name']].drop_duplicates(subset=['Product ID'], keep='last').reset_index(drop=True)
    dim_products_path = os.path.join(output_dir, 'Dim_Products.csv')
    dim_products.to_csv(dim_products_path, index=False)
    print(f" -> Exported Dim_Products: {len(dim_products)} rows")

    # 3. Dim Geography (1:N with Fact Orders)
    dim_geo = df[['Postal Code', 'City', 'State', 'Region', 'Country']].drop_duplicates(subset=['Postal Code'], keep='last').reset_index(drop=True)
    dim_geo_path = os.path.join(output_dir, 'Dim_Geography.csv')
    dim_geo.to_csv(dim_geo_path, index=False)
    print(f" -> Exported Dim_Geography: {len(dim_geo)} rows")

    # 4. Dim Regional Managers (1:N with Dim Geography / Fact Orders)
    people_path = os.path.join('data', 'processed', 'people_cleaned.csv')
    df_people = pd.read_csv(people_path)
    dim_managers_path = os.path.join(output_dir, 'Dim_Managers.csv')
    df_people.to_csv(dim_managers_path, index=False)
    print(f" -> Exported Dim_Managers: {len(df_people)} rows")

    # 5. Dim Returns (1:1 / 1:N with Fact Orders)
    returns_path = os.path.join('data', 'processed', 'returns_cleaned.csv')
    df_returns = pd.read_csv(returns_path)
    dim_returns_path = os.path.join(output_dir, 'Dim_Returns.csv')
    df_returns.to_csv(dim_returns_path, index=False)
    print(f" -> Exported Dim_Returns: {len(df_returns)} rows")

    # 6. Dim Date (1:N with Fact Orders on Order Date and Ship Date)
    df_date = pd.read_csv(date_path)
    dim_date_path = os.path.join(output_dir, 'Dim_Date.csv')
    df_date.to_csv(dim_date_path, index=False)
    print(f" -> Exported Dim_Date: {len(df_date)} rows")

    # 7. Fact Orders (Central Transactional Table)
    fact_cols = [
        'Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Customer ID',
        'Product ID', 'Postal Code', 'Ship Mode', 'Sales', 'Quantity',
        'Discount', 'Profit', 'Shipping_Days', 'Unit_Price', 'Unit_Cost',
        'Profit_Margin', 'Is_Returned'
    ]
    fact_orders = df[fact_cols].copy()
    fact_orders_path = os.path.join(output_dir, 'Fact_Orders.csv')
    fact_orders.to_csv(fact_orders_path, index=False)
    print(f" -> Exported Fact_Orders: {len(fact_orders)} rows")

    print("\n" + "=" * 70)
    print("POWER BI STAR SCHEMA MODEL READY IN:", output_dir)
    print("=" * 70)

if __name__ == '__main__':
    orders = os.path.join('data', 'processed', 'orders_cleaned.csv')
    dates = os.path.join('data', 'processed', 'dim_date.csv')
    out = os.path.join('powerbi', 'model_data')
    build_powerbi_star_schema(orders, dates, out)
