import os
import shutil
import uuid
from datetime import date

from random import choices

# ________________________ Data Base ________________________ #

def table_structure(table:str)->dict:
    '''
    Previous validation for table name existence is already in place
    so I wont do it again.
    '''
    
    match(table):
        case "products":
            target = {
                "product_id": str,
                "product_name": str,
                "category": str,
                "unit_price": float,
                "cost": float,
            }
        case "forecast":
            target = {
                "forecast_id": str,
                "product_id": str,
                "forecast_date": str,
                "forecast_qty": int,
                "confidence_low": int,
                "confidence_high": int,
                "model_used": str
            }
        case "inventory":
            target = {
                "log_id": str,
                "product_id": str,
                "log_date": str,
                "quantity_in": int,
                "stock_level": int,
                "warehouse": str
            }
        case "sales":
            target = {
                "sale_id": str,
                "product_id": str,
                "sale_date": date,
                "quantity_sold": int,
                "sale_price": float,
                "location": str,
                "customer_id": str
            }
        case "stock":
            target = {
                "status_id": str,
                "product_id": str,
                "status_date": date,
                "stock_level": int,
                "is_stockout": bool
            }
        
    return target

def is_valid_schema_input(attempt:dict, table:str):

    target = table_structure(table) # get the schema structure
    
    if len(attempt) != len(target): # check they have the same length
        return False
    
    if sorted(target.keys()) != sorted(attempt.keys()): # check they have the same keys
        return False
    
    for key in target:
        instance  = target[key]
        if not (type(attempt[key]) is instance): # check valid data types
            return False
        
    return True # return true if every check passes

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

def create_status_id():
    '''
    For stock data usage
    '''
    base = str(uuid.uuid4())[:8] # make sure its adding up to 20 (for schema type maximum VARCHAR)
    current_date = str(date.today())
    
    return current_date + "-" + base

def create_sale_id():
    current_date = str(date.today()).replace("-", "")
    id = ''.join(choices('0123456789', k=12))
        
    return current_date + id 