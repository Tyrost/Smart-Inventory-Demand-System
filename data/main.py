from database.Commander import Commander
from data.stock.simulate import map_allocations
from data.sales.simulate import map_sales
from data.sales.inv_management import thread_restock
from utils.helper import clean_pycache

def execute():
    db_engine = Commander("stock")

    # map_allocations(5, db_engine) # Intializes x product categories and allocates stock data
    # map_sales(db_engine) # simulates sales, and return number of products sold
    thread_restock()
    
execute()
clean_pycache()

    
