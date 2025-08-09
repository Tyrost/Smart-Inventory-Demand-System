from datetime import date

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
        case "inventory_log":
            target = {
                "log_id": str,
                "product_id": str,
                "date": date,
                "quantity_change": int,
                "stock_level": int,
                "warehouse": str,
                "change_type": str,
                "reference_id": (str, type(None))
            }
        case "sales":
            target = {
                "sale_id": str,
                "product_id": str,
                "date": date,
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
        case _: # default case
            raise ValueError(f"Unknown table name: {table}")
        
    return target

def is_valid_schema_input(attempt:dict, table:str):
    target = table_structure(table)
    
    if len(attempt) != len(target):
        return False
    if sorted(target.keys()) != sorted(attempt.keys()):
        return False
    for key in target:
        expected_type  = target[key]
        if not isinstance(attempt[key], expected_type):
            return False
        
    return True # every check passes