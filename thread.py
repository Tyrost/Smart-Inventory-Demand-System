from data.main import execute
from utils.misc import setup_logging, clean_pycache

from datetime import date, timedelta
from time import sleep
from random import randint
import logging as log

logger = log.getLogger(__name__)

current_date = date(2020, 1, 1)

# def thread_simulation(simulation_days=30):
#     '''
#     NOT FOR PRODUCTION USE!! Computation-heavy!
#     '''
#     global current_date
#     prob = randint(0, 1)
#     setup_logging()
#     if prob >= 0.95:
#         execute(current_date, False, 1) 
#     else:
#         execute(current_date)
#     current_date = current_date + timedelta(days=1)

def thread_simulation(simulation_days=30):
    '''
    NOT FOR PRODUCTION USE!! Computation-heavy!
    '''
    
    setup_logging()
    
    current_date = date(2020, 1, 1) # Set this to be our initial time for the simulation.
    
    for day in range(simulation_days):
        print("Resuming. Day Count:", day)
        prob = randint(0, 1)
        
        if day == 0:
            execute(current_date, False, 1)
        else:
            execute(current_date, False, 1) if prob <= 0.90 else execute(current_date)
            
        current_date = current_date + timedelta(days=1)
        log.info("Sleeping three seconds.")
        sleep(3)
    return
        
thread_simulation(60)