from database.Commander import Commander
from data.processed.Clean import Clean 
from data.stock.Allocate import Allocate

from random import randint
from datetime import date

from utils.helper import create_status_id
from data.pipeline import upload

def allocate(products:list, allocation_engine:Allocate):
    total = randint(300, 2500) # choose from a pool of up to 2500 items per category
    
    allocations = {}
    dataframe = allocation_engine.allocate_adjusted(total)

    for index, product in enumerate(products): # get row by row and extract the allocation stock value-by-value
        product_row = dataframe.iloc[index] 
        
        allocation = int(product_row["adjusted_allocation"])
        allocations[product["product_name"]] = allocation

    return allocations

def parse_allocations(allocations:dict, IDs:list):
    '''
    preparation for database intake.
    Takes the IDs of the products and matches them accordingly 
    via index.
    '''
    parsed_data = []
    
    length = len(allocations) # should always be 10
    
    status_ids = [create_status_id() for i in range(length)]
    product_ids = IDs
    status_date = date.today()
    stock_level = list(allocations.values())
    is_stockout = [True if value == 0 else False for value in stock_level]
    
    for index in range(length):
        stock = {
            "status_id": status_ids[index],
            "product_id": product_ids[index],
            "status_date": status_date,
            "stock_level": stock_level[index],
            "is_stockout": is_stockout[index]
        }
        parsed_data.append(stock)
    
    return parsed_data

def map_allocations(num_categories:int, database_engine:Commander)->dict:
    '''
    Don't mind the brain dump :) 
    There are exactly 10 different products for every unique category. Hence we will choose a fitting range
    that will be divided upon these 10 different products for each category. Let said range be 100 - 500
    Then for each aggregate category stock we will choose a random number to assign to each of the 10 products
    
    The lower and upper bounds will be a computation of the popularity and rating for that product. This data we don't
    have in the cleansed dataset, but we can find these metrics in the raw datasets gotten from our API 
    
    Let the bottom bound be -> (standardized review-to-rating unit / 100) * (range * 0.10)
    Let the upper bound be -> (standardized review-to-rating unit / 100) * (range * 0.80)
    then:
    x = randint(lower, upper)
    range = range - x
    
    and do this again for 10 iterations. If there are any left over then discard these extra stock products
    
    We will simulate how much stock we have for each product
    For every product type, we will get a random stock number.
    
    ^^^ Obsolete ^^^
    '''
    
    for i in range(num_categories): # 10 product API calls
        
        builder = Clean()
        
        products = builder.get_clean() # for upload
        raw_data = builder.get_raw()
        rating = Allocate(raw_data)
        
        if not products:
            print(f"No products listing found for iteration count: {i+1}. Continuing")
            continue
        
        product_ids:list = builder.get_dataframe()["product_id"] # get the id vector of our clean dataframe
        allocations = allocate(products, rating) # initialize allocation division algorithm
        
        parsed_stock_data:list = parse_allocations(allocations, product_ids) # prepare stock data for upload
        
        # call to upload data onto database
        # it will already ensure schema validation
        upload(products, "products", database_engine)
        upload(parsed_stock_data, "stock", database_engine)
    
    return