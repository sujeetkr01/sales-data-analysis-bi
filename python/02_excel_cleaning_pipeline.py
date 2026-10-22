"""
=============================================================================
STEP 3: EXCEL CLEANING & TRANSFORMATION PIPELINE
Script: python/02_excel_cleaning_pipeline.py
Description: Cleans, structures, standardizes, and enriches Superstore data,
             producing a production-grade multi-tab Excel workbook (.xlsx)
             and normalized CSV staging files.
=============================================================================
"""

import os
import pandas as pd
import numpy as np

def clean_superstore_dataset(raw_path: str, output_excel_path: str, processed_dir: str):
    print("=" * 70)
    print("STEP 3: EXCEL TRANSFORMATION & CLEANING PIPELINE")
    print(f"Reading raw data from: {raw_path}")
    print("=" * 70)

    # 1. Read raw CSV
    df_raw = pd.read_csv(raw_path, encoding='latin1')
    
    # -------------------------------------------------------------------------
    # TRANSFORMATION 1: ENTITY SEPARATION (Multi-Sheet Splitting)
    # -------------------------------------------------------------------------
    print("\n[Transformation 1] Separating stacked entities into relational datasets...")
    # Orders fact table: rows 0 to 9993
    df_orders = df_raw.iloc[0:9994].copy()
    
    # People dimension: rows 9995 to 9998
    df_people = df_raw.iloc[9995:9999, [1, 0]].copy()
    df_people.columns = ['Region', 'Regional_Manager']
    df_people['Region'] = df_people['Region'].str.strip()
    df_people['Regional_Manager'] = df_people['Regional_Manager'].str.strip()
    
    # Returns dimension: rows 10000 to end
    df_returns_raw = df_raw.iloc[10000:, [1, 0]].copy()
    df_returns_raw.columns = ['Order ID', 'Returned']
    df_returns_raw['Order ID'] = df_returns_raw['Order ID'].str.strip()
    df_returns_raw['Returned'] = df_returns_raw['Returned'].str.strip()
    # Deduplicate returns dimension so Order ID is unique primary key
    df_returns = df_returns_raw.drop_duplicates(subset=['Order ID']).reset_index(drop=True)
    
    print(f" -> Orders extracted: {len(df_orders)} records")
    print(f" -> Regional Managers extracted: {len(df_people)} records")
    print(f" -> Returns extracted: {len(df_returns)} unique returned orders (from {len(df_returns_raw)} log rows)")

    # -------------------------------------------------------------------------
    # TRANSFORMATION 2: DATA TYPE CONVERSIONS & COLUMN TRIMMING
    # -------------------------------------------------------------------------
    print("\n[Transformation 2] Standardizing data types, whitespace, and case...")
    df_orders['Row ID'] = pd.to_numeric(df_orders['Row ID']).astype(int)
    
    text_cols = ['Order ID', 'Ship Mode', 'Customer ID', 'Customer Name', 
                 'Segment', 'Country', 'City', 'State', 'Region', 
                 'Product ID', 'Category', 'Sub-Category', 'Product Name']
    for col in text_cols:
        df_orders[col] = df_orders[col].astype(str).str.strip()

    # -------------------------------------------------------------------------
    # TRANSFORMATION 3: POSTAL CODE IMPUTATION & LEADING ZERO PRESERVATION
    # -------------------------------------------------------------------------
    print("\n[Transformation 3] Imputing missing Postal Codes and formatting as 5-digit ZIP...")
    # Burlington, Vermont has 11 missing ZIP codes. Real ZIP is 05401.
    burlington_mask = (df_orders['City'] == 'Burlington') & (df_orders['State'] == 'Vermont') & (df_orders['Postal Code'].isnull())
    print(f" -> Imputing '05401' for {burlington_mask.sum()} Burlington, VT rows")
    df_orders.loc[burlington_mask, 'Postal Code'] = 5401.0
    
    # Format all postal codes as 5-character string with leading zeroes
    df_orders['Postal Code'] = df_orders['Postal Code'].astype(int).astype(str).str.zfill(5)

    # -------------------------------------------------------------------------
    # TRANSFORMATION 4: DATE PARSING & STANDARDIZATION
    # -------------------------------------------------------------------------
    print("\n[Transformation 4] Standardizing Order Date and Ship Date to ISO format...")
    df_orders['Order Date'] = pd.to_datetime(df_orders['Order Date'], format='%m/%d/%Y')
    df_orders['Ship Date'] = pd.to_datetime(df_orders['Ship Date'], format='%m/%d/%Y')
    
    # -------------------------------------------------------------------------
    # TRANSFORMATION 5: NUMERIC CLEANING & ROUNDING
    # -------------------------------------------------------------------------
    print("\n[Transformation 5] Cleaning and rounding financial metrics...")
    df_orders['Sales'] = df_orders['Sales'].astype(float).round(2)
    df_orders['Quantity'] = df_orders['Quantity'].astype(int)
    df_orders['Discount'] = df_orders['Discount'].astype(float).round(2)
    df_orders['Profit'] = df_orders['Profit'].astype(float).round(2)

    # -------------------------------------------------------------------------
    # TRANSFORMATION 6: DERIVED BUSINESS ATTRIBUTES & UNIT ECONOMICS
    # -------------------------------------------------------------------------
    print("\n[Transformation 6] Engineering derived analytical columns...")
    # Shipping Lead Time
    df_orders['Shipping_Days'] = (df_orders['Ship Date'] - df_orders['Order Date']).dt.days
    
    # Unit Economics
    df_orders['Unit_Price'] = (df_orders['Sales'] / df_orders['Quantity']).round(2)
    df_orders['Unit_Cost'] = ((df_orders['Sales'] - df_orders['Profit']) / df_orders['Quantity']).round(2)
    
    # Profit Margin % (Profit / Sales)
    df_orders['Profit_Margin'] = (df_orders['Profit'] / df_orders['Sales']).round(4)
    
    # Order Return Status Lookup (Excel XLOOKUP / MATCH equivalent)
    returned_set = set(df_returns['Order ID'])
    df_orders['Is_Returned'] = df_orders['Order ID'].apply(lambda x: 'Yes' if x in returned_set else 'No')
    
    # Regional Manager Lookup
    manager_map = dict(zip(df_people['Region'], df_people['Regional_Manager']))
    df_orders['Regional_Manager'] = df_orders['Region'].map(manager_map)

    # Date formatting for clean spreadsheet and CSV output
    df_orders['Order Date'] = df_orders['Order Date'].dt.strftime('%Y-%m-%d')
    df_orders['Ship Date'] = df_orders['Ship Date'].dt.strftime('%Y-%m-%d')

    # Reorder columns logically
    final_cols = [
        'Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Shipping_Days',
        'Ship Mode', 'Customer ID', 'Customer Name', 'Segment',
        'Country', 'City', 'State', 'Postal Code', 'Region', 'Regional_Manager',
        'Product ID', 'Category', 'Sub-Category', 'Product Name',
        'Sales', 'Quantity', 'Discount', 'Profit', 'Unit_Price', 'Unit_Cost',
        'Profit_Margin', 'Is_Returned'
    ]
    df_orders = df_orders[final_cols]

    # -------------------------------------------------------------------------
    # SAVE PROCESSED EXCEL WORKBOOK & CLEAN CSVs
    # -------------------------------------------------------------------------
    print("\n[Export] Generating multi-sheet Excel workbook and CSV exports...")
    os.makedirs(os.path.dirname(output_excel_path), exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
        df_orders.to_excel(writer, sheet_name='Orders', index=False)
        df_returns.to_excel(writer, sheet_name='Returns', index=False)
        df_people.to_excel(writer, sheet_name='People', index=False)
    
    orders_csv_path = os.path.join(processed_dir, 'orders_cleaned.csv')
    returns_csv_path = os.path.join(processed_dir, 'returns_cleaned.csv')
    people_csv_path = os.path.join(processed_dir, 'people_cleaned.csv')

    df_orders.to_csv(orders_csv_path, index=False)
    df_returns.to_csv(returns_csv_path, index=False)
    df_people.to_csv(people_csv_path, index=False)

    print(f" -> Multi-sheet Excel workbook generated: {output_excel_path}")
    print(f" -> Orders CSV exported: {orders_csv_path}")
    print(f" -> Returns CSV exported: {returns_csv_path}")
    print(f" -> People CSV exported: {people_csv_path}")

    # Summary statistics
    total_sales = df_orders['Sales'].sum()
    total_profit = df_orders['Profit'].sum()
    overall_margin = (total_profit / total_sales) * 100
    returned_orders_cnt = (df_orders['Is_Returned'] == 'Yes').sum()

    print("\n" + "=" * 70)
    print("CLEANING & TRANSFORMATION SUMMARY")
    print(f"Total Transactions: {len(df_orders):,} rows")
    print(f"Total Gross Sales:  ${total_sales:,.2f}")
    print(f"Total Net Profit:   ${total_profit:,.2f}")
    print(f"Blended Margin:     {overall_margin:.2f}%")
    print(f"Line items returned: {returned_orders_cnt:,} ({returned_orders_cnt/len(df_orders)*100:.2f}%)")
    print("=" * 70)

if __name__ == '__main__':
    raw = os.path.join('data', 'raw', 'Sample_Superstore_Raw.csv')
    excel_out = os.path.join('data', 'processed', 'Superstore_Cleaned.xlsx')
    proc_dir = os.path.join('data', 'processed')
    clean_superstore_dataset(raw, excel_out, proc_dir)
