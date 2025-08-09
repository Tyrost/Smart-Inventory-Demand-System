CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(22) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS forecast (
    forecast_id VARCHAR(20) PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL,
    forecast_date DATE NOT NULL,
    forecast_qty INT,
    confidence_low INT,
    confidence_high INT,
    model_used VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS inventory_log (
    log_id VARCHAR(20) PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    quantity_change INT NOT NULL,
    stock_level INT NOT NULL,
    warehouse VARCHAR(50) NOT NULL,
    change_type VARCHAR(20) NOT NULL,
    reference_id VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    quantity_sold INT NOT NULL,
    sale_price DECIMAL(10, 2) NOT NULL,
    location VARCHAR(50) NOT NULL,
    refunded BOOLEAN NOT NULL,
    reason VARCHAR(40)
);

CREATE TABLE IF NOT EXISTS stock (
    status_id VARCHAR(20) PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL,
    status_date DATE NOT NULL,
    stock_level INT NOT NULL,
    is_stockout BOOLEAN NOT NULL
);
