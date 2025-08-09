from iterate import execute_iteration_thread

from datetime import date, timedelta
from time import sleep
from random import randint
import logging as log

import sim_config as config
from database.Commander import Commander

logger = log.getLogger(__name__)

def thread_simulation():
    '''
    NOT FOR PRODUCTION USE!! Computation-heavy!
    '''
    
    simulation_days = 30 if not config.SIMULATION_DAYS else config.SIMULATION_DAYS
    database = Commander("sales")
    log.info(f"Main database connection thread initialized -> Host: {database.host}, Database: {database.database}")
    # Set this to be our initial time for the simulation.
    current_date = date(2020, 1, 1) if not config.SIMULATION_STARTING_DATE else config.SIMULATION_STARTING_DATE
    log.info(f"Simulation starting date set to: {current_date}. Simulation set to end: {current_date + timedelta(days=simulation_days)} ({simulation_days} days).")
    
    product_prob = 90 if not config.NEW_PRODUCT_ITERATION_PROB else config.NEW_PRODUCT_ITERATION_PROB
    assert(product_prob <= 90 and product_prob > 0)
    
    for day in range(simulation_days):
        prob = randint(1, 100)

        if day == 0: # initially we must get the first product category
            execute_iteration_thread(current_date, database, False, 1)
        else:
            # we will get a new product category only 10% of the times
            execute_iteration_thread(current_date, database, False, 1) if prob > product_prob else execute_iteration_thread(current_date, database)
        
        log.info(f"Iteration was successful for date {current_date}.")
        
        current_date = current_date + timedelta(days=1)
        sleep(1.5)
    return

if __name__ == "__main__":
    thread_simulation()