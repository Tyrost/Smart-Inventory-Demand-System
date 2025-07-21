from typing import List

def upload(data:List[dict], table_name, database)->None:
    
    database.checkout_table(table_name)
    
    for index in range(len(data)):
        status = database.create_item(data[index])
        if status != 200:
            raise ConnectionError(f"An error to SQL database ocurred when uploading `{table_name}` data. Booted error: {status}")
    return 