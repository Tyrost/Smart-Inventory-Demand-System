import asyncio
from database.Commander import Commander
import pandas as pd

def thread_restock(subset = 100):# take sample of the last 100 as default (?)
    '''
    Inputs:
        `subset` (int) for training and probabilistic allocation
        default value of 100 rows of data; but as the Law of Large numbers says, the more the better!
    Outputs:
        None
        Populates the database manually instead.
    
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
    
    # we will simulate at least 30% sells and at most 5% sales of our total stock retrieved from random index gathering
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
    
    I would like to mention that ChatGPT was a great help on this plan.
    '''
    commander = Commander("inventory_log") # we will begin be observing a batch of inventory log sales
    
    data = commander.read_cols(filter={"change_type": "sale"}, limit=subset) # take sample of the last 50 (?)
    
    # for the sake of efficiency, I will place this data onto a dataframe
    # though via query would be faster, I want to practice ORMs and I don't want 
    # to make my commander class messier; instead I want it to be readable and completely understandable.
    # (also for the sake of data analysis :)

    logs = pd.DataFrame(data)
    relevant_cols = ["product_id", "quantity_change", "stock_level"]
    trends = logs[relevant_cols]
    
    trends = trends.groupby(trends["product_id"]).aggregate({"quantity_change": "sum", "stock_level": "first"}) # merge by product
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
    
    

    