import pandas as pd
import csv
import os
from data.raw import init_mock_data
import logging as log

#Default export function
def main():
    '''
    Index 0 = inventory DF object
    Index 1 = sales DF objects
    '''
    inventoryCSV_relpath = 'data/raw/inventory_data.csv'
    salesCSV_relpath = 'data/raw/sales_data.csv'

    if not os.path.exists(inventoryCSV_relpath) or not os.path.exists(salesCSV_relpath):
        log.debug(f"Required path files:\n{inventoryCSV_relpath}\n{salesCSV_relpath}\nnot found... Executing data initialization script.")
        init_mock_data()
    
    inventoryDF = get_inventory(inventoryCSV_relpath)
    salesDF = get_sales(salesCSV_relpath)

    return inventoryDF, salesDF # return tuple of both utilized DataFrame objects


def get_inventory(filePath):
    try:
        with open(filePath, 'r') as file:
            inventoryFile = csv.DictReader(file, fieldnames=["inventory_id", "product_id", "store_id", "date", "stock_level"])
            inventoryList = list(inventoryFile)
            inventory_df = pd.DataFrame(inventoryList)

            return inventory_df
        
    except Exception as error:
        log.error(f'There was an error reading inventory data file. Error:\n{error}')
        return

def get_sales(filePath):
    try:

        with open(filePath, 'r') as file:
            salesFile = csv.DictReader(file, fieldnames=["sale_id", "product_id", "store_id", "date", "quantity"])
            salesList = list(salesFile)
            sales_df = pd.DataFrame(salesList)

            return sales_df
    
    except Exception as error:
        log.error(f'There was an error reading sales data file. Error:\n{error}')
        return