'''
This configuration panel will provide full control of the parameters and behavior of the simulation.
Default values are in-place in case values are not set.

We have validated the arguments within code, but we will create a function specifically to validate arguments.
'''
from datetime import date

PRODUCT_LISTING:list = None # [product1, product2, product3, ...] 
WAREHOUSE_LISTING:list = None # [Washington US Some warehouse1, Washington US Some warehouse2, Washington US Some warehouse3, ...]

# these proportions dictate variability (randomly chosen proportion between the two) 
# on choosing how much of the total sold products are to be restocked for that iteration.
PRODUCT_RESTOCK_LOWER_PROPORTION:float = None
PRODUCT_RESTOCK_UPPER_PROPORTION:float = None
# if these are set to null values, then you have the option to keep a uniform proportion across all iterations.
PRODUCT_RESTOCK_UNIFORM_PROPORTION:float = None

# The number of data we will use to gather metrics
SALE_TREND_SUBSET:int = None

SIMULATION_STARTING_DATE:date = None # CLI MUST ENSURE TO PARSE INTO `date` OBJECT
SIMULATION_DAYS:int = None # how many days will we simulate over

NEW_PRODUCT_ITERATION_PROB:int = None # the probability that a new product category will be added to our simulation.
# each product category introduces 10 new products

REFUND_RATE:list = None # example [9, 1] -> indicates 10% refund
QUANTITY_SELL_RATES:list = None # must add to 1. # must add to 1. Example [0.4, 0.3, 0.2, 0.1, 0.0] -> indicates probabilities of [1,2,3,4,5] quantities sold accordingly.

# dictate lower and upper bound for random value gathering per iteration on
# what % of the current total stock we will simulate to sell
# Ex: We hold 100 items of products, then lower = 5%, upper = 30%
# then we will make sure to sell a percentage randomly chosen between 5 and 30
SALE_SIMULATION_PROPORTION_LOWER_BOUND:float = None
SALE_SIMULATION_PROPORTION_UPPER_BOUND:float = None

# select a range (or constant value) of how many items will be created for each category iteration.
ITERATION_PRODUCT_COUNT_ALLOCATION_LOWER_BOUND:int = None
ITERATION_PRODUCT_COUNT_ALLOCATION_UPPER_BOUND:int = None
ITERATION_PRODUCT_COUNT_ALLOCATION_UNIFORM_BOUND:int = None

#  indicates that we will read all records from that date until present times.
METRIC_DATE_CUTOFF:date = None

def validate_config()->None:
    '''
    Validates all parameters.
    '''
    test = True
    if PRODUCT_LISTING:
        test = test and isinstance(PRODUCT_LISTING, list)
    if WAREHOUSE_LISTING:
        test = test and isinstance(WAREHOUSE_LISTING, list)
        
    if (PRODUCT_RESTOCK_LOWER_PROPORTION and PRODUCT_RESTOCK_UPPER_PROPORTION) or PRODUCT_RESTOCK_UNIFORM_PROPORTION:
        test = test and not (
            PRODUCT_RESTOCK_LOWER_PROPORTION < PRODUCT_RESTOCK_UPPER_PROPORTION and
            not (PRODUCT_RESTOCK_LOWER_PROPORTION and PRODUCT_RESTOCK_UPPER_PROPORTION and PRODUCT_RESTOCK_UNIFORM_PROPORTION) and 
            (not (PRODUCT_RESTOCK_LOWER_PROPORTION + PRODUCT_RESTOCK_UPPER_PROPORTION == 1) or
            PRODUCT_RESTOCK_UNIFORM_PROPORTION <= 1) and
            (isinstance(PRODUCT_RESTOCK_LOWER_PROPORTION, float) and isinstance(PRODUCT_RESTOCK_UPPER_PROPORTION, float)) or isinstance(PRODUCT_RESTOCK_UNIFORM_PROPORTION, float)
        )
    
    if SALE_TREND_SUBSET:
        test = test and isinstance(SALE_TREND_SUBSET, int) and SALE_TREND_SUBSET > 100
        
    if SIMULATION_STARTING_DATE:
        test = test and isinstance(SIMULATION_STARTING_DATE, date)
    
    if SIMULATION_DAYS:
        test = test and isinstance(SIMULATION_DAYS, int) and SIMULATION_DAYS < 900
    
    if NEW_PRODUCT_ITERATION_PROB:
        test = test and isinstance(NEW_PRODUCT_ITERATION_PROB, int) and NEW_PRODUCT_ITERATION_PROB <= 90
        
    if REFUND_RATE:
        test = test and isinstance(REFUND_RATE, list) and len(REFUND_RATE) == 2 and REFUND_RATE[0] + REFUND_RATE[1] == 10
        
    if QUANTITY_SELL_RATES:
        test = test and isinstance(QUANTITY_SELL_RATES, list) and len(QUANTITY_SELL_RATES) == 5 and sum(QUANTITY_SELL_RATES) == 1
        
    if SALE_SIMULATION_PROPORTION_LOWER_BOUND and ITERATION_PRODUCT_COUNT_ALLOCATION_UPPER_BOUND:
        test = test and (SALE_SIMULATION_PROPORTION_LOWER_BOUND < ITERATION_PRODUCT_COUNT_ALLOCATION_UPPER_BOUND and 
        SALE_SIMULATION_PROPORTION_LOWER_BOUND + ITERATION_PRODUCT_COUNT_ALLOCATION_UPPER_BOUND < 1)
        
        test = test and not (ITERATION_PRODUCT_COUNT_ALLOCATION_LOWER_BOUND < ITERATION_PRODUCT_COUNT_ALLOCATION_UPPER_BOUND and
        not (ITERATION_PRODUCT_COUNT_ALLOCATION_LOWER_BOUND and ITERATION_PRODUCT_COUNT_ALLOCATION_UPPER_BOUND and ITERATION_PRODUCT_COUNT_ALLOCATION_UNIFORM_BOUND) and
        (not (ITERATION_PRODUCT_COUNT_ALLOCATION_LOWER_BOUND + ITERATION_PRODUCT_COUNT_ALLOCATION_UPPER_BOUND == 1) or
        ITERATION_PRODUCT_COUNT_ALLOCATION_UNIFORM_BOUND <= 1)
    )
        
    if METRIC_DATE_CUTOFF:
        test = test and isinstance(METRIC_DATE_CUTOFF, date)
        
    assert(test)