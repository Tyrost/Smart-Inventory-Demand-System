import pandas as pd
import numpy as np
from faker import Faker
import random as rd

fake = Faker()

# Mock Knife-Selling Business

# Mock Parameters

number_sales:int = 40000
products = 60
number_stores = 100
date_range =  pd.date_range(start="2018-01-01", end="2024-12-31") # Seven years

product_ids = [f"P{str(i).zfill(3)}" for i in range(products)]
store_ids = [f"S{str(i).zfill(3)}" for i in range(number_stores)]

sales = []

for sale in range(number_sales):

    random_prdouct = rd.choice(product_ids)
    random_store = rd.choice(store_ids)
    date = rd.choice(date_range)
    quantity_sold = rd.randint(1, 5)
    product_price = rd.choice(range(52, 700))
    total_price = product_price * quantity_sold

    sales.append({
        "date": str(date.date()),
        "sale_id": fake.uuid4(),
        "store": random_store,
        "product": random_prdouct,
        "quantity_sold": quantity_sold,
        "product price": product_price,
        "total_price": total_price
    })

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

sales_df = pd.DataFrame(sales)
inventory_df = pd.DataFrame(inventory)

sales_df.to_csv("sales_data.csv", index=False)
inventory_df.to_csv("inventory_data.csv", index=False)