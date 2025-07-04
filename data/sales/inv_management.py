from database.Commander import Commander
import pandas as pd

from random import randint
from typing import List

from utils.helper import create_invlog_id
from datetime import date

def thread_restock(data:List[dict])->pd.DataFrame:
    '''
    We will observe the rate of change in which items are being sold.
    If there are a lot of items being sold in shorter X periods of time, 
    then we will prioritize allocating more stock onto that product.
    
    From here we want to implement an algorithm that takes into account demand, as well as the urgency of having
    close to no stock left for an aggregate product.
    Select a total number of allocations for this iteration based on total "popularity" of our products, by taking the same approach as
    our sales simulations when choosing how many products will be sold for that iteration:
    ```
    rows = [database_engine.read_row_index(index) for index in indices]
    
    # sum the total amount of stocks in the data selected
    stock_count = sum(row["stock_level"] for row in rows)
    
    # we will simulate at least 30% sales and at most 5% sales of our total stock retrieved from random index gathering
    lower_bound = floor(stock_count * 0.05)
    upper_bound = ceil(stock_count * 0.30)
    
    # the total items sold
    total_sold = randint(lower_bound, upper_bound)
    ```
    
    We will take the absolute value of `quantity_change` to determine a score, which we will use to allocate stock:
    base_i = abs(quantity_change_i) + ϵ
    score_i = base_i * (1/stock_level_i + δ)
    
    where δ and ϵ are used ot avoid total ignorance of smaller number rates.
    
    These rates will give us computation scores, which we can convert to probability vectors
    by normalizing them in order to assume a probabilistic approach to simulate real-world allocations.
    
    I would like to mention that ChatGPT was a great help on this plan. (Didn't work)
    ^^^ Obsolete again ^^^
    '''

    # for the sake of efficiency, I will place this data onto a dataframe
    # though via query would be faster, I want to practice ORMs and I don't want 
    # to make my commander class messier; instead I want it to be readable and completely understandable.
    # (also for the sake of data analysis :)

    logs = pd.DataFrame(data)
    relevant_cols = ["product_id", "quantity_change", "stock_level"]
    trends = logs[relevant_cols]
    
    # since the product distribution with respective quantity changes are irrelevant and hard to analyze due to more iterations,
    # we will instead merge the data over the product_id.
    trends = trends.groupby(trends["product_id"]).aggregate({"quantity_change": "sum", "stock_level": "first"}) # merge by product
    quantity_sold = abs(trends["quantity_change"].sum())

    # we will choose to restock 80% to 120% of what was sold for that iteration
    quantity_to_restock = randint(round(quantity_sold * 0.8), round(quantity_sold * 1.2)) 

    '''
    ^^^^^ Sample ^^^^^
    product_id      quantity_change  stock_level
                                    
    US25062300011               -5          531
    US25062300015               -8           65
    US25062300017               -5            2
    US25062300021              -27          197
    US25062300026               -8           14
    US25062300027               -8            0
    US25062300028               -4            5
    US25062300031              -13          392
    US25062300032                0            0
    US25062300034               -3          272
    US25062300037                0            0
    US25062300045               -9           75
    US25062300048              -16           17
    US25062300052                0            0
    US25062300055               -8           13
    US25062300059               -3           30
    '''
    change = trends["quantity_change"].apply(lambda x: abs(x))
    
    trends["original_stock"] = trends["stock_level"] + change
    trends["rates"] = change / trends["original_stock"] # calculates rates of change.
    # the faster they are sold, the more likely it is to have higher demand, hence needing to allocate more stock to these products.

    # for products that sold 0 products as a result of having 0 stock initially, there is not really a great way to know the products popularity
    # it could very well be that the product was greatly successful or that it may be unpopular. That's outside of our current scope,
    # so we will "promise" to allocate an arbitrary number of stock into it.
    num_nans = trends["rates"].isna().sum()
    total_products = len(trends)
    nan_proportion = num_nans / total_products
    
    nan_total_allocation = round(quantity_to_restock * nan_proportion)
    per_nan_allocation = round(nan_total_allocation / num_nans) if num_nans else 0
 
    quantity_to_restock -= per_nan_allocation * num_nans
    
    '''
    The algorithm is the following:
    
    let x be the total number of products gathered
    let n be the total number of Null values. 
    let a be total number of restock that was chosen
    let b be the proportion of the ration n to x as a percentage
    Then for each null value we will allocate y:
    y = n / a * b
    Dont forget to round y, as we need to ensure whole numbers represented as a product.
    
    After this I asked ChatGPT what it thought of the algorithm. It disagreed with the implementation, so I went ahead and offered 
    clear examples of why this algorithm is ideal:
    
    ChatGPT:
    This formula explodes or becomes tiny depending on the ratio. Also, you're dividing num_nans by a scaled value of itself, 
    which gets nonsensical fast. 
    
    Let’s say you want to allocate 10% of total restock to NaN products evenly:
    ```
    nan_allocation_fraction = 0.10 
    nan_total_allocation = round(quantity_to_restock * nan_allocation_fraction)
    if num_nans > 0:
        per_nan_allocation = max(1, nan_total_allocation // num_nans)  # avoid 0 allocation
    else:
        per_nan_allocation = 0
    quantity_to_restock -= per_nan_allocation * num_nans
    ```
    What I said:
    I believe that's the whole point. Say there is only one NaN value out of 28 products. 
    This would represent 1/28 which is about 3.7%. Then we take the total product allocation and multiply it by this number. 
    I believe that this is fair, even if the number is small.
    
    Now suppose we have the opposite: 24/28 products are NaN. 
    They got no sales since they didn't have any products in the market. 
    What if they were all extremely popular and successful and got sold so fast in previous iterations 
    (yet to be decided: days, weeks, months...). Then I would be fine allocation the chunk of 
    stock into these products by dividing fairly among them. With this same scenario; Imagine we hard 
    capped the percentage allocation to 10% as you suggested. Then 4 out of the 28 products would be making up 90% of the total stock! 
    Which I believe to be unfair!
    
    If I'm wrong, or have any suggestions let me know :)
    '''
    
    # now we also take into account that we want to focus on products that have higher number of sales (or that have higher current stock)
    # which indicates that people are often buying this product more often.
    # From here I want to take a probabilistic approach. The higher and higher the product count for a product, 
    # the more likely it is to provide more stock allocation to it.
    
    trends["allocation_prob"] = trends["original_stock"] / trends["original_stock"].sum() # provide as a percentage
    trends["cold_allocation"] = trends["allocation_prob"] * quantity_to_restock
    trends["rate_allocation"] = ((trends["rates"] / trends["rates"].sum()) * quantity_to_restock) # calculate a probability vector based on the rates we have
     
    # will take the average of the two approaches as a way of merging them.
    trends["adjusted_allocation"] = (trends["cold_allocation"] + trends["rate_allocation"]) / 2

    trends["adjusted_allocation"] = trends["adjusted_allocation"].fillna(per_nan_allocation) # come back to populate Null values
    trends["adjusted_allocation"] = trends["adjusted_allocation"].apply(lambda x: round(x)) # round the product count 
    trends = trends.reset_index()

    processed = trends[["product_id", "stock_level", "adjusted_allocation"]]
    processed.rename(columns={"adjusted_allocation": "quantity_change"}, inplace=True)
    
    processed = processed.reset_index(drop=True)
  
    return processed
    
    
def map_restock(database:Commander, subset=100)->None: # take sample of the last 100 as default from the database (?)
    '''
    The `subset` parameter represents the number of "logged" data we will gather to find possible trends
    of where it is most convenient to allocate products to.
    As the "Law of Large Number States" the more data we posses for any statistical experiment is given, the more
    accurate the result will be. In this case the accuracy of our trend detection.
    '''
    database.checkout_table("inventory_log") # take the sample
    data = database.read_cols(filter={"change_type": "sale"}, limit=subset) # we will begin be observing a batch of inventory log sales
    
    dataframe = thread_restock(data)
    
    # start building the data from the dataframe to trespass to a List[dict] as our data to be sent to our ORM
    
    dataframe["stock_level"] = dataframe["stock_level"] + dataframe["quantity_change"]
    dataframe["log_date"] = date.today()
    dataframe["warehouse"] = "United Warehouse Main, Washington, US"
    dataframe["change_type"] = "restock"
    dataframe["log_id"] = [create_invlog_id() for i in range(len(dataframe))]
    dataframe["reference_id"] = None

    prepared_data = dataframe.to_dict(orient="records")

    for data in prepared_data:
        status = database.create_item(data)
        if status != 200:
            raise Exception(f"An error occurred when uploading `inventory_log` data. Code: {status}")
    return