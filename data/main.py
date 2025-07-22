from database.Commander import Commander
from data.stock.simulate import map_allocations
from data.sales.simulate import map_sales
from data.sales.inv_management import map_restock

import logging as log
from datetime import date

logger = log.getLogger(__name__)

def execute(current_date:date, skip_new=True, new_categories=0):
    db_engine = Commander("stock")

    if (not skip_new) and new_categories:
        map_allocations(current_date, new_categories, db_engine) # Intializes x product categories and allocates stock data
    else:
        log.info(f"1/3 API product gathering process has been skipped. Continuing with simulation...")
    map_sales(current_date, db_engine) # simulates sales, and return number of products sold
    map_restock(current_date, db_engine) # restocking thread for inventory management
    
    return