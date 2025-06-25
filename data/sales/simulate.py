from database.Commander import Commander
from utils.helper import create_sale_id

from random import randint, choices
from typing import List
from math import ceil, floor
from datetime import date

def simulate_sell(database_engine:Commander, data:List[dict], stock_to_sell:int):
    i = 0
    count = 0
    while(stock_to_sell != 0):
        database_engine.checkout_table("products") # for foreign key mapping and price extraction
        if i == len(data): # make sure it goes back to first position to avoid overflow
            i = 0
        
        product_row:dict = data[i]

        if product_row["is_stockout"]: # check if data has no stuck. If so, then continue with next products
            i += 1
            continue
        
        quantities = [1, 2, 3, 4, 5]
        prob = [0.82, 0.10, 0.05, 0.02, 0.01] # set probabilities 
        
        # set data
        sale_id = create_sale_id()
        product_id = product_row["product_id"]
        sale_date = date.today()
        quantity_sold = choices(quantities, weights=prob, k=1)[0]
        price = database_engine.read_cols("cost", filter={"product_id": product_id})[0]
        sale_price = round(price * quantity_sold, 2)
        
        # CREATE NEW TABLE WITH RANDOM USER INFORMATION AND EXTRACT WITH FOREIGN KEY
        location = "Washington, US"
        customer_id = "123"
        
        sale = {
            "sale_id": sale_id,
            "product_id": product_id,
            "sale_date": sale_date,
            "quantity_sold": quantity_sold,
            "sale_price": float(sale_price),
            "location": location,
            "customer_id": customer_id
            }
        # create sale with data gathering upload
        database_engine.checkout_table("sales")
        status = database_engine.create_item(sale)
        
        if status != 200:
            raise Exception(f"An error occurred when uploading `sale` data. Code: {status}")
        
        # Now we need to update the values
        product_stock = product_row["stock_level"]
        if quantity_sold > product_stock:
            quantity_sold = product_stock
        
        product_stock -= quantity_sold
        stock_to_sell -= quantity_sold
        
        # update stock value data in `stock` table
        database_engine.checkout_table("stock")
        database_engine.update_value({"product_id": product_id}, "stock_level", product_stock)
        
        # update counter and increase index value
        count += 1
        i += 1
        
    return count # return the count of sells

def map_sales(database_engine:Commander):
    '''
    Read every product and simulate sales
    '''
    # count total number of records in the stock table
    database_engine.checkout_table("stock")
    product_count = database_engine.count_records()

    # we will select an amount of products that we will allocate for sales
    lower_bound = floor(product_count * 0.10)
    upper_bound = ceil(product_count * 0.90)
    total_selections = randint(lower_bound, upper_bound) # determines how many products were selected to be chosen to allocate sells onto
    # choose random product indices to sale product to
    
    # get random indices fro stock data
    indices = [randint(0, product_count-1)  for i in range(total_selections)]
    rows = [database_engine.read_row_index(index) for index in indices]
    
    # sum the total amount of stocks in the data selected
    stock_count = sum(row["stock_level"] for row in rows)
    
    # we will simulate at least 30% sells and at most 5% sales of our total stock retrieved from random index gathering
    lower_bound = floor(stock_count * 0.05)
    upper_bound = ceil(stock_count * 0.30)
    
    # the total items sold
    total_sold = randint(lower_bound, upper_bound)
    
    # the function will handle data storage and simulation over iterations
    # it will also distribute the total stock onto the products chosen
    count = simulate_sell(database_engine, data=rows, stock_to_sell=total_sold)
    return count