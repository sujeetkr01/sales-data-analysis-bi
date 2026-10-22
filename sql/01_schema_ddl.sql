-- =============================================================================
-- SQL SCHEMA DEFINITION (DDL) FOR SUPERSTORE BUSINESS INTELLIGENCE
-- File: sql/01_schema_ddl.sql
-- Database: superstore.db (ANSI SQL Compliant: SQLite / PostgreSQL / MySQL)
-- =============================================================================

-- Drop existing tables to ensure clean rebuild
DROP TABLE IF EXISTS fact_orders;
DROP TABLE IF EXISTS dim_returns;
DROP TABLE IF EXISTS dim_managers;

-- -----------------------------------------------------------------------------
-- 1. DIMENSION TABLE: REGIONAL MANAGERS (dim_managers)
-- -----------------------------------------------------------------------------
CREATE TABLE dim_managers (
    region VARCHAR(50) PRIMARY KEY,
    regional_manager VARCHAR(100) NOT NULL
);

-- -----------------------------------------------------------------------------
-- 2. DIMENSION TABLE: ORDER RETURNS (dim_returns)
-- -----------------------------------------------------------------------------
CREATE TABLE dim_returns (
    order_id VARCHAR(50) PRIMARY KEY,
    returned VARCHAR(10) NOT NULL DEFAULT 'Yes'
);

-- -----------------------------------------------------------------------------
-- 3. FACT TABLE: SALES TRANSACTIONS (fact_orders)
-- -----------------------------------------------------------------------------
CREATE TABLE fact_orders (
    row_id INTEGER PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    order_date DATE NOT NULL,
    ship_date DATE NOT NULL,
    shipping_days INTEGER NOT NULL,
    ship_mode VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    segment VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    region VARCHAR(50) NOT NULL,
    regional_manager VARCHAR(100) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    sales DECIMAL(12, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    discount DECIMAL(5, 2) NOT NULL,
    profit DECIMAL(12, 2) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    unit_cost DECIMAL(10, 2) NOT NULL,
    profit_margin DECIMAL(7, 4) NOT NULL,
    is_returned VARCHAR(5) NOT NULL DEFAULT 'No',
    FOREIGN KEY (region) REFERENCES dim_managers (region)
);

-- -----------------------------------------------------------------------------
-- INDEXES FOR QUERY OPTIMIZATION
-- -----------------------------------------------------------------------------
CREATE INDEX idx_orders_order_date ON fact_orders (order_date);
CREATE INDEX idx_orders_customer_id ON fact_orders (customer_id);
CREATE INDEX idx_orders_product_id ON fact_orders (product_id);
CREATE INDEX idx_orders_category ON fact_orders (category, sub_category);
CREATE INDEX idx_orders_region ON fact_orders (region);
CREATE INDEX idx_orders_order_id ON fact_orders (order_id);
