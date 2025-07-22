from data.main import execute
from utils.misc import setup_logging, clean_pycache

from datetime import date, timedelta
from time import sleep
from random import randint, randrange
import logging as log

logger = log.getLogger(__name__)

current_date = date(2020, 1, 10)


def thread_simulation(simulation_days=30):
    '''
    NOT FOR PRODUCTION USE!! Computation-heavy!
    '''
    
    setup_logging()
    
    current_date = date(2020, 1, 1) # Set this to be our initial time for the simulation.
    
    for day in range(simulation_days):
        prob = randint(1, 100)

        if day == 0: # initially we must get the first product category
            execute(current_date, False, 1)
        else:
            # we will get a new product category only 10% of the times
            execute(current_date, False, 1) if prob > 90 else execute(current_date)
        
        log.info(f"Iteration was successful. Day: {current_date}")
        
        current_date = current_date + timedelta(days=1)
        sleep(3)
    return