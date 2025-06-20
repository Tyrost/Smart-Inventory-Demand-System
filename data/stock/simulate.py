
from database.Commander import Commander
from random import randint

from data.processed.Clean import Clean 
from data.Allocate import Allocate

from pprint import pprint

def allocate(category, commander:Commander, rating_engine:Allocate):
    
    total = randint(300, 2500) #choose from a pool of up to 2500 items per category
    products = commander.read_cols("product_name", filter={"category": category}) # get the product names for this category
    
    print(f"\nTotal products chosen: {total} for category: {category}\n")
    
    if len(products) != 10: # ensure there are 10 products
        raise Exception(f"Expected 10 products in category '{category}', got {len(products)}")
    
    allocations = []
    
    dataframe = rating_engine.allocate_adjusted(total)

    for index, product in enumerate(products):
        product_row = dataframe.iloc[index]
        
        allocation = int(product_row["adjusted_allocation"])
        allocations.append((product, allocation))

    return allocations
       
        
def map_allocations()->dict:
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
    result = {}
    
    clean = Clean()
    products = clean.get_clean()
    raw_data = clean.raw_data
    rating = Allocate(raw_data)

    commander = Commander("products")
    for product in products:
        commander.create_item(product)
    
    categories = commander.get_unique("category")

    for category in categories:
        allocations = allocate(category, commander, rating)
        result[category] = allocations

    return result

if __name__ == "__main__":
    pprint(map_allocations(), sort_dicts=False)