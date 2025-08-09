import os
import shutil
import uuid
from datetime import date, datetime
import logging
from random import choices
from typing import List
import sim_config as config

# ___________________________________________________________________ #

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

# ___________________________________________________________________ #

def clean_pycache():
    '''
    Removes annoying __pycache__ files after every execution
    '''
    for dirpath, dirnames, _ in os.walk("."):
        for dirname in dirnames:
            if dirname == "__pycache__":
                full_path = os.path.join(dirpath, dirname)
                shutil.rmtree(full_path, ignore_errors=True)

# ________________________________ ID ________________________________ #

def create_status_id(date:date):
    '''
    For stock data usage
    '''
    base = str(uuid.uuid4())[:8] # make sure its adding up to 20 (for schema type maximum VARCHAR)
    current_date = str(date)
    
    return current_date + "-" + base

def create_sale_id(date:date):
    current_date = str(date).replace("-", "")
    id = ''.join(choices('0123456789', k=12))
        
    return current_date + id 

def create_invlog_id():
    id = ''.join(choices('0123456789', k=17))
    return "INV" + id

def create_forecast_id():
    base = str(uuid.uuid4())[:17]
    return "FOR" + base

# ___________________________________________________________________ #


def upload(data:List[dict], table_name, database)->None:
    '''
    Specific data upload.
    '''
    
    database.checkout_table(table_name)
    
    for index in range(len(data)):
        status = database.create_item(data[index])
        if status != 200:
            raise ConnectionError(f"An error to SQL database ocurred when uploading `{table_name}` data. Booted error: {status}")
    return 

# ___________________________________________________________________ #

def dict_to_config(configuration:dict):
    hints = config.__annotations__ # Thank the lord for this dunder method
    
    for key, value in configuration.items():
        data_type = hints[key]
        
        if hasattr(config, key): # case config global varibale exists
            if data_type == date: # case: parse string to date
                date_val = datetime.strptime(value, "%Y-%m-%d").date()
                setattr(config, key, date_val)
            else: # case int, str, float (supported by JSON)
                setattr(config, key, value)
        else:
            return
        
# ___________________________________________________________________ #

WAREHOUSES = [
    "Amazon Fulfillment Center, California, US",
    "Walmart Distribution Center, Arkansas, US",
    "FedEx Supply Chain, Pennsylvania, US",
    "UPS Supply Chain Solutions, Kentucky, US",
    "DHL Supply Chain, Ohio, US",
    "XPO Logistics Warehouse, Illinois, US",
    "Ryder Logistics Hub, Florida, US",
    "GEODIS Warehouse, Texas, US",
    "Lineage Logistics, Michigan, US",
    "C.H. Robinson Warehouse, Minnesota, US",
    "Kenco Logistics, Tennessee, US",
    "NFI Industries Warehouse, New Jersey, US",
    "DB Schenker Logistics, Georgia, US",
    "Penske Logistics Center, Indiana, US",
    "Saddle Creek Logistics, Missouri, US",
    "Americold Storage Facility, Colorado, US",
    "CEVA Logistics Center, Arizona, US",
    "Radial Fulfillment Center, Nevada, US",
    "ShipBob Warehouse, Illinois, US",
    "Flexe Partner Warehouse, Washington, US"
]