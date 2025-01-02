import pandas as pd
from faker import Faker
import random as rd

fake = Faker()

# Mock Knife-Selling Business

def init_mock_data(): # Creating function to be invoked

    # Mock Parameters
    number_sales:int = 40000
    products = 60
    number_stores = 100
    date_range =  pd.date_range(start="2018-01-01", end="2024-12-31") # Seven years

    # Get ordered IDs for products and stores
    product_ids = [f"P{str(i).zfill(3)}" for i in range(products)]
    store_ids = [f"S{str(i).zfill(3)}" for i in range(number_stores)]

    sales = []

    for sale in range(number_sales): # We describe random values to all historical purchases

        # Initialize random choice values and integers where appropriate
        random_prdouct = rd.choice(product_ids) 
        random_store = rd.choice(store_ids)
        date = rd.choice(date_range)
        quantity_sold = rd.randint(1, 5)
        product_price = rd.choice(range(52, 700))
        total_price = product_price * quantity_sold
        
        # Input data onto a dictionary, appended to an overall list
        sales.append({
            "date": str(date.date()),
            "sale_id": fake.uuid4(),
            "store": random_store,
            "product": random_prdouct,
            "quantity_sold": quantity_sold,
            "product price": product_price,
            "total_price": total_price
        })

    sales_df = pd.DataFrame(sales)


    inventory = []
    for product_id in product_ids:
        for store_id in store_ids:
            for date in date_range[::30]:
                stock_level = rd.randint(50, 500)
                inventory.append({
                    "inventory_id": fake.uuid4(),
                    "product_id": product_id,
                    "store_id": store_id,
                    "date": date,
                    "stock_level": stock_level
                })

    
    inventory_df = pd.DataFrame(inventory)

    sales_df.to_csv("sales_data.csv", index=False)
    inventory_df.to_csv("inventory_data.csv", index=False)

    return