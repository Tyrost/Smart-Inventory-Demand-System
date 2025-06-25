from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, DATE, INTEGER, DECIMAL, BOOLEAN

Base = declarative_base()

class Product(Base): # Gather from API
    __tablename__ = "products"
    product_id = Column(VARCHAR(22), primary_key=True, unique=True)
    product_name = Column(VARCHAR(100), nullable=False)
    category = Column(VARCHAR(50), nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    cost = Column(DECIMAL(10, 2), nullable=False)
    
class Forecast(Base): # Measure
    __tablename__ = "forecast"
    forecast_id = Column(VARCHAR(20), primary_key=True, unique=True)
    product_id = Column(VARCHAR(20), nullable=False)
    forecast_date = Column(DATE(), nullable=False)
    forecast_qty = Column(INTEGER())
    confidence_low = Column(INTEGER())
    confidence_high = Column(INTEGER())
    model_used = Column(VARCHAR(50))
    
class InventoryLog(Base): # Fabricate your own
    __tablename__ = "inventory"
    log_id = Column(VARCHAR(20), primary_key=True, unique=True)
    product_id = Column(VARCHAR(20), nullable=False)
    log_date = Column(DATE(), nullable=False)
    quantity_change = Column(INTEGER(), nullable=False)
    stock_level = Column(INTEGER(), nullable=False)
    warehouse = Column(VARCHAR(50), nullable=False)
    change_type = Column(VARCHAR(20), nullable=False)
    
    reference_id = Column(VARCHAR(20)) # will act as our foreign key for sales in case change type is due to `sale`

class Sale(Base): # Fabricate your own
    __tablename__ = "sales"
    sale_id = Column(VARCHAR(20), primary_key=True, unique=True)
    customer_id = Column(VARCHAR(20), nullable=False)
    product_id = Column(VARCHAR(20), nullable=False)
    sale_date = Column(DATE(), nullable=False)
    quantity_sold = Column(INTEGER(), nullable=False)
    sale_price = Column(DECIMAL(10, 2), nullable=False)
    location = Column(VARCHAR(50), nullable=False)
    
class Stock(Base): # Fabricate your own
    __tablename__ = "stock"
    status_id = Column(VARCHAR(20), primary_key=True, unique=True)
    product_id = Column(VARCHAR(20), nullable=False)
    status_date = Column(DATE(), nullable=False)
    stock_level = Column(INTEGER(), nullable=False)
    is_stockout = Column(BOOLEAN(), nullable=False)
    
    def to_dict(self):
        return {
            "status_id": self.status_id,
            "product_id": self.product_id,
            "status_date": str(self.status_date),
            "stock_level": self.stock_level,
            "is_stockout": self.is_stockout
        }