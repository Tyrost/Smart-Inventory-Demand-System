from data.processed.clean import get_clean
from database.Commander import Commander

def populate_products():
    try:
        corrupted = False
        
        commander = Commander("products")
        product_batch = get_clean()
        
        # take the list of 10 products in the same category for every one, take the status of it
        logs = [True if commander.create_item(product) == 200 else False for product in product_batch] 
        if not any(logs): # if there is at least one non-200 status code
            corrupted = True # set flag for warning
        
        if corrupted:
            return "At least one item was unsuccessfully submitted"
            
        return f"Successfully uploaded {len(logs)} records -> {commander.table_name}"
    
    except Exception as error:
        raise Exception(f"Failure: {error}")