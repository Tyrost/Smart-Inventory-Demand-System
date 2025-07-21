import os
import shutil
import uuid
from datetime import date
import logging
from random import choices

# ___________________________________________________________________ #

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

# ___________________________________________________________________ #

def clean_pycache():
    '''
    Removes annoying __pycache__ files after every execution
    '''
    for dirpath, dirnames, _ in os.walk("."):
        for dirname in dirnames:
            if dirname == "__pycache__":
                full_path = os.path.join(dirpath, dirname)
                shutil.rmtree(full_path, ignore_errors=True)

def create_status_id(date:date):
    '''
    For stock data usage
    '''
    base = str(uuid.uuid4())[:8] # make sure its adding up to 20 (for schema type maximum VARCHAR)
    current_date = str(date)
    
    return current_date + "-" + base

def create_sale_id(date:date):
    current_date = str(date).replace("-", "")
    id = ''.join(choices('0123456789', k=12))
        
    return current_date + id 

def create_invlog_id():
    id = ''.join(choices('0123456789', k=17))
    return "INV" + id