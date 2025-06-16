from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, DATE, INTEGER, DECIMAL, BOOLEAN

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    product_id = Column(VARCHAR(22), primary_key=True, unique=True)
    product_name = Column(VARCHAR(100))
    category = Column(VARCHAR(50))
    unit_price = Column(DECIMAL(10, 2))
    cost = Column(DECIMAL(10, 2))
    
class Forecast(Base):
    __tablename__ = "forecast"
    forecast_id = Column(VARCHAR(20), primary_key=True)
    product_id = Column(VARCHAR(20))
    forecast_date = Column(DATE())
    forecast_qty = Column(INTEGER())
    confidence_low = Column(INTEGER())
    confidence_high = Column(INTEGER())
    model_used = Column(VARCHAR(50))
    
class Inventory(Base):
    __tablename__ = "inventory"
    log_id = Column(VARCHAR(20), primary_key=True)
    product_id = Column(VARCHAR(20))
    log_date = Column(DATE())
    quantity_in = Column(INTEGER())
    stock_level = Column(INTEGER())
    warehouse = Column(VARCHAR(50))

class Sale(Base):
    __tablename__ = "sales"
    sale_id = Column(VARCHAR(20), primary_key=True)
    product_id = Column(VARCHAR(20))
    sales_date = Column(DATE())
    quantity_sold = Column(INTEGER())
    sale_price = Column(DECIMAL(10, 2))
    location = Column(VARCHAR(50))
    
class Stock(Base):
    __tablename__ = "stock"
    status_id = Column(VARCHAR(20), primary_key=True)
    product_id = Column(VARCHAR(20))
    status_date = Column(DATE())
    stock_level = Column(INTEGER())
    is_stockout = Column(BOOLEAN())