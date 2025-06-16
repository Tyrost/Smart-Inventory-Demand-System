

# ________________________ Data Base 

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
                "cost": float
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
                "sales_date": str,
                "quantity_sold": int,
                "sale_price": float,
                "location": str
            }
        case "stock":
            target = {
                "status_id": str,
                "product_id": str,
                "status_date": str,
                "stock_level": int,
                "is_stockout": int
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
