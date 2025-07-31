from thread import thread_simulation
from data.misc.thread import thread_metrics
from ml.model import Model
from data.misc.Metrics import Metrics
from utils.cli_helper import instructions, update_config
from utils.misc import setup_logging

import argparse
import config.config as config
import logging as log

setup_logging()
logger = log.getLogger(__name__)

def generate_parser():
    '''
    Set flags for arguments for the sake of controlling how the simulation threads.
    '''
    parser = argparse.ArgumentParser(description="Smart Inventory Simulation CLI")

    parser.add_argument('--product-listing', type=str, help='Comma-separated list of product names')
    parser.add_argument('--warehouse-listing', type=str, help='Comma-separated list of warehouse names')

    parser.add_argument('--restock-lower', type=float, help='Lower bound proportion for restocking (float between 0 and 1)')
    parser.add_argument('--restock-upper', type=float, help='Upper bound proportion for restocking (float between 0 and 1)')
    parser.add_argument('--restock-uniform', type=float, help='Fixed uniform restock proportion (float between 0 and 1)')

    parser.add_argument('--subset-size', type=int, help='Number of entries to use for sales trend subset (must be > 100)')

    parser.add_argument('--start-date', type=str, help='Simulation start date (format: YYYY-MM-DD)')
    parser.add_argument('--days', type=int, help='Number of days to simulate')

    parser.add_argument('--new-product-prob', type=int, help='Probability (0–90) that new product categories are added')

    parser.add_argument('--refund-rate', type=str, help='Comma-separated 2-element list of refund rate weights (must sum to 10)')
    parser.add_argument('--quantity-sell-rates', type=str, help='Comma-separated 5-element list of quantity sale probabilities (must sum to 1.0)')

    parser.add_argument('--sale-lower', type=float, help='Lower bound percentage of current stock to simulate sales')
    parser.add_argument('--sale-upper', type=float, help='Upper bound percentage of current stock to simulate sales')

    parser.add_argument('--alloc-lower', type=int, help='Lower bound of product allocation count per new category')
    parser.add_argument('--alloc-upper', type=int, help='Upper bound of product allocation count per new category')
    parser.add_argument('--alloc-uniform', type=int, help='Uniform product allocation count per new category')
    
    # parameters (independent from config)
    
    parser.add_argument('--metric-operation', metavar='operation', help='To gather a metric from data, you must first specify what action to observe.')

    # example function calling
    parser.add_argument('-r', '--run', metavar='run', action='store_true', help='Run the inventory simulation')
    parser.add_argument('--get-metrics', metavar='metrics',action='store_true', help='Compute metrics after simulation')

    return parser.parse_args()

def main():
    args = generate_parser()
    update_config(args)

    if args.help:
        instructions()
        return

    try:
        config.validate_config()
    except AssertionError as error:
        log.warn(f"Configuration validation failed: {error}")
        return

    if args.run:
        thread_simulation()

    if args.get_metrics:
        thread_metrics(args.metric_operation)

    
'''
python main.py --run-sim --product-listing p1,p2,p3 --start-date 2025-08-01 --days 30

Compute metrics only (assuming simulation already ran):

python main.py --compute-metrics

Run both:

python main.py --run-sim --compute-metrics --start-date 2025-08-01 --days 30
'''