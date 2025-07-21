from config.secret_load import get_secret
import requests
import random
from typing import List
import logging as log
import json
import os
import logging as log

logger = log.getLogger(__name__)

class Builder:
    '''
    API Provider:
    SerpAPI

    API Documentation:
    https://serpapi.com/search-api

    This API is uses web-scraping tools to then transform into an API. This is greatly fitting for what
    we are trying to achieve.
    '''
    # for practice sake, I will choose from a finite random set of products and get 10 products to then analyze.
    def __init__(self):

        self.products = [
            "Clock",            "Watch",            "Basketball",       "Coffee Maker",     "T-Shirt",
            "Laptop",           "Smartphone",       "Backpack",         "Water Bottle",     "Desk Lamp",
            "Keyboard",         "Mouse",            "Notebook",         "Pen",              "Coffee Mug",
            "Sneakers",         "Headphones",       "Toothbrush",       "Shampoo",          "Soap",
            "Towel",            "Pillow",           "Blanket",          "Book",             "Chair",
            "Table",            "Television",       "Remote Control",   "Battery",          "Light Bulb",
            "Picture Frame",    "Vase",             "Candle",           "Cutting Board",    "Frying Pan",
            "Plate",            "Fork",             "Spoon",            "Knife",            "Blender",
            "Toaster",          "Vacuum Cleaner",   "Broom",            "Dustpan",          "Hanger",
            "Iron",             "Umbrella",         "Wallet",           "Sunglasses",       "Gloves",
            "Scarf",            "Hat",              "Measuring Tape",   "Screwdriver",      "Hammer",
            "Pliers",           "Drill",            "Extension Cord",   "Power Strip",      "Router",
            "Webcam",           "Microphone",       "External Hard Drive","USB Drive",      "Printer",
            "Scanner",          "Paper Shredder",   "Calculator",       "Stapler",          "Scissors",
            "Tape Dispenser",   "Folder",           "Binder",           "Highlighter",      "Eraser",
            "Glue Stick",       "Markers",          "Crayons",          "Paint Brush",      "Canvas",
            "Yoga Mat",         "Dumbbells",        "Jump Rope",        "Resistance Band",  "Football",
            "Soccer Ball",      "Baseball Glove",   "Tennis Racket",    "Bicycle",          "Helmet",
            "Flashlight",       "First Aid Kit",    "Fire Extinguisher","Smoke Detector",   "Door Mat",
            "Curtains",         "Rug",              "Mirror",           "Shelf",            "Storage Bin"
        ]

        self.product = None
        self.raw_data = None # return value
        
        self.__get_random()
    
    # __________________________________________________________________________________________ #
    
    def __call(self, params:str):
        try:
            BASE = "https://serpapi.com/search.json?"
            
            response = requests.get(BASE, params)
            
            if response.status_code != 200:
                raise ConnectionError(f"There was an issue with the response. Status code: {response.status_code}")
            
            content = response.json()
            return content
        except Exception as error:
            log.error(error)
    
    def __get_random(self):
        choice = random.choice(self.products)
        choice = choice.replace(" ", "").strip()
        self.product = choice
        
    def __handle_json(self, data)->None: # remove if/when in production
        '''
        We only want to keep one raw data file in there for demonstration
        and maybe for debugging. The rest is useless, as there may turn into 
        duplicates and GitHub will complain if I start overloading my data pushes.
        '''
        
        base = "data/raw/log/"
        
        files:list = os.listdir(base)
        
        if len(files) != 0:
            for file in files:
                file_path = os.path.join(base, file)
                os.remove(file_path)
        
        with open(f"data/raw/log/{self.product}_product.json", "w") as file:
            json.dump(data, file, indent=4)
            

    # ______________________________________ Usage Methods ______________________________________ #
    
    def execute(self) -> None:
        try:
            
            KEY = get_secret("SERPAPI_KEY")
            params = {
                "engine": "amazon",
                "k": self.product, # k is the search item. Ik, weird name.
                "api_key": KEY
            }

            data_aggregate:dict = self.__call(params)
            # WE CAN FURTHER ENHANCE THIS BY ACCEPTING RANDOM POOLS OF INDEXES (while keep 10 still) RATHER THAN HARD-CODED POSITIONS.
            data:List[dict] = data_aggregate["organic_results"][6:16] # only get 10 products and skip the first 6 products as these are sponsored
            
            self.__handle_json(data)
            
            self.raw_data = data
            
        except Exception as error:
            log.error(error)
            return "Failure"