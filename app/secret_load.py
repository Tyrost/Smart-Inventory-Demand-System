from dotenv import load_dotenv
import os

# We will focus on local secret retrieval only

DEV_ENV = "/Users/danielcorzo/Documents/Github/Smart-Inventory-Demand-System/.env"

def get_secret(name:str)->str:
    global DEV_ENV
    load_dotenv(DEV_ENV)
    
    secret = os.environ.get(name)
    
    return secret