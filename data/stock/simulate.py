from database.Commander import Commander
from data.processed.Clean import Clean 
from data.stock.Allocate import Allocate

from random import randint
from datetime import date

import logging as log
from utils.misc import create_status_id
from data.pipeline import upload

logger = log.getLogger(__name__)

def allocate(products:list, allocation_engine:Allocate):
    total = randint(300, 2500) # choose from a pool of up to 2500 items per category
    
    allocations = {}
    dataframe = allocation_engine.allocate_adjusted(total)

    for index, product in enumerate(products): # get row by row and extract the allocation stock value-by-value
        product_row = dataframe.iloc[index] 
        
        allocation = int(product_row["adjusted_allocation"])
        allocations[product["product_name"]] = allocation

    return allocations

def parse_allocations(date:date, allocations:dict, IDs:list):
    '''
    preparation for database intake.
    Takes the IDs of the products and matches them accordingly 
    via index.
    '''
    parsed_data = []
    
    length = len(allocations) # should always be 10
    
    status_ids = [create_status_id(date) for i in range(length)]
    product_ids = IDs
    status_date = date
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

def map_allocations(date:date, num_categories:int, database_engine:Commander):
    '''
    This represents the main executing function that populates the `products` and `stock` tables.
    Concurrently initializes the gathering and cleaning of API product gathering for our analysis.
    We gather 10 products from `x` categories `num_categories` number of times.
    For each product, we do automated matching to allocate products determined by the ratings and reviews
    each received as a way to quantify product popularity.
    '''
    log.info("1/3 Processing `product` and `allocation`. Now populating...")
    
    for i in range(num_categories): # 10 product API calls
        
        builder = Clean()
        
        products = builder.get_clean(date) # for upload
        raw_data = builder.get_raw()
        rating = Allocate(raw_data)
        
        if not products:
            print(f"No products listing found for iteration count: {i+1}. Continuing")
            continue
        
        product_ids:list = builder.get_dataframe()["product_id"] # get the id vector of our clean dataframe
        allocations = allocate(products, rating) # initialize allocation division algorithm
        
        parsed_stock_data:list = parse_allocations(date, allocations, product_ids) # prepare stock data for upload
        
        # call to upload data onto database
        # it will already ensure schema validation
        upload(products, "products", database_engine)
        upload(parsed_stock_data, "stock", database_engine)
    log.info("Product creation and allocation complete.")
    return