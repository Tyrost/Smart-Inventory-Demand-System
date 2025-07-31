
import config.config as config
import datetime
import logging as log

logger = log.getLogger(__name__)

def instructions()->None:
    print("Not implemented")

def update_config(args):
    if args.product_listing:
        config.PRODUCT_LISTING = args.product_listing.split(',')
    if args.warehouse_listing:
        config.WAREHOUSE_LISTING = args.warehouse_listing.split(',')

    if args.restock_lower is not None:
        config.PRODUCT_RESTOCK_LOWER_PROPORTION = args.restock_lower
    if args.restock_upper is not None:
        config.PRODUCT_RESTOCK_UPPER_PROPORTION = args.restock_upper
    if args.restock_uniform is not None:
        config.PRODUCT_RESTOCK_UNIFORM_PROPORTION = args.restock_uniform

    if args.subset_size is not None:
        config.SALE_TREND_SUBSET = args.subset_size
    if args.start_date:
        try:
            config.SIMULATION_STARTING_DATE = datetime.strptime(args.start_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Start date must be in YYYY-MM-DD format.")
    if args.days is not None:
        config.SIMULATION_DAYS = args.days

    if args.new_product_prob is not None:
        config.NEW_PRODUCT_ITERATION_PROB = args.new_product_prob
    if args.refund_rate:
        config.REFUND_RATE = list(map(int, args.refund_rate.split(',')))
    if args.quantity_sell_rates:
        config.QUANTITY_SELL_RATES = list(map(float, args.quantity_sell_rates.split(',')))

    if args.sale_lower is not None:
        config.SALE_SIMULATION_PROPORTION_LOWER_BOUND = args.sale_lower
    if args.sale_upper is not None:
        config.SALE_SIMULATION_PROPORTION_UPPER_BOUND = args.sale_upper

    if args.alloc_lower is not None:
        config.ITERATION_PRODUCT_COUNT_ALLOCATION_LOWER_BOUND = args.alloc_lower
    if args.alloc_upper is not None:
        config.ITERATION_PRODUCT_COUNT_ALLOCATION_UPPER_BOUND = args.alloc_upper
    if args.alloc_uniform is not None:
        config.ITERATION_PRODUCT_COUNT_ALLOCATION_UNIFORM_BOUND = args.alloc_uniform
    
    log.info("All variables for simulation have been configured.")