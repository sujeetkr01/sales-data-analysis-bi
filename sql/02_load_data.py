"""
=============================================================================
SQL DATABASE INITIALIZATION AND DATA INGESTION
Script: sql/02_load_data.py
Database: sql/superstore.db
=============================================================================
"""

import os
import sqlite3
import pandas as pd

def init_and_load_db(db_path: str, ddl_path: str, data_dir: str):
    print("=" * 70)
    print("INITIALIZING SQL DATABASE & LOADING DATA")
    print(f"Target Database: {db_path}")
    print("=" * 70)
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Execute DDL Schema
    print("\n[Step 1] Executing DDL Schema from sql/01_schema_ddl.sql...")
    with open(ddl_path, 'r', encoding='utf-8') as f:
        ddl_script = f.read()
    cursor.executescript(ddl_script)
    print(" -> Tables (dim_managers, dim_returns, fact_orders) and indexes created.")
    
    # 2. Ingest Dim People / Managers
    print("\n[Step 2] Ingesting dim_managers...")
    people_csv = os.path.join(data_dir, 'people_cleaned.csv')
    df_people = pd.read_csv(people_csv)
    # Rename columns to match DDL
    df_people.columns = ['region', 'regional_manager']
    df_people.to_sql('dim_managers', conn, if_exists='append', index=False)
    print(f" -> Inserted {len(df_people)} rows into dim_managers.")
    
    # 3. Ingest Dim Returns
    print("\n[Step 3] Ingesting dim_returns...")
    returns_csv = os.path.join(data_dir, 'returns_cleaned.csv')
    df_returns = pd.read_csv(returns_csv)
    df_returns.columns = ['order_id', 'returned']
    df_returns.to_sql('dim_returns', conn, if_exists='append', index=False)
    print(f" -> Inserted {len(df_returns)} rows into dim_returns.")
    
    # 4. Ingest Fact Orders
    print("\n[Step 4] Ingesting fact_orders...")
    orders_csv = os.path.join(data_dir, 'orders_cleaned.csv')
    df_orders = pd.read_csv(orders_csv, dtype={'Postal Code': str})
    # Map CSV column names to SQL snake_case column names
    col_map = {
        'Row ID': 'row_id',
        'Order ID': 'order_id',
        'Order Date': 'order_date',
        'Ship Date': 'ship_date',
        'Shipping_Days': 'shipping_days',
        'Ship Mode': 'ship_mode',
        'Customer ID': 'customer_id',
        'Customer Name': 'customer_name',
        'Segment': 'segment',
        'Country': 'country',
        'City': 'city',
        'State': 'state',
        'Postal Code': 'postal_code',
        'Region': 'region',
        'Regional_Manager': 'regional_manager',
        'Product ID': 'product_id',
        'Category': 'category',
        'Sub-Category': 'sub_category',
        'Product Name': 'product_name',
        'Sales': 'sales',
        'Quantity': 'quantity',
        'Discount': 'discount',
        'Profit': 'profit',
        'Unit_Price': 'unit_price',
        'Unit_Cost': 'unit_cost',
        'Profit_Margin': 'profit_margin',
        'Is_Returned': 'is_returned'
    }
    df_orders = df_orders.rename(columns=col_map)
    df_orders.to_sql('fact_orders', conn, if_exists='append', index=False)
    print(f" -> Inserted {len(df_orders)} rows into fact_orders.")
    
    conn.commit()
    
    # 5. Sanity check counts
    print("\n" + "=" * 70)
    print("DATABASE INGESTION VERIFICATION")
    print("=" * 70)
    for table in ['dim_managers', 'dim_returns', 'fact_orders']:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"Table '{table}': {count:,} rows")
        
    totals = cursor.execute("""
        SELECT 
            ROUND(SUM(sales), 2) AS total_sales,
            ROUND(SUM(profit), 2) AS total_profit,
            COUNT(DISTINCT order_id) AS distinct_orders,
            COUNT(DISTINCT customer_id) AS distinct_customers
        FROM fact_orders
    """).fetchone()
    print(f"Total Sales:    ${totals[0]:,.2f}")
    print(f"Total Profit:   ${totals[1]:,.2f}")
    print(f"Distinct Orders: {totals[2]:,}")
    print(f"Customers:       {totals[3]:,}")
    print("=" * 70)
    
    conn.close()

if __name__ == '__main__':
    db = os.path.join('sql', 'superstore.db')
    ddl = os.path.join('sql', '01_schema_ddl.sql')
    data = os.path.join('data', 'processed')
    init_and_load_db(db, ddl, data)
