from config.secret_load import get_secret
import requests
import random
import json
from typing import Union, List
import logging as log

class Builder:
    '''
    API Provider:
    SerpAPI

    API Documentation:
    https://serpapi.com/search-api

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
            "Webcam",           "Microphone",       "External Hard Drive","USB Drive",          "Printer",
            "Scanner",          "Paper Shredder",   "Calculator",       "Stapler",          "Scissors",
            "Tape Dispenser",   "Folder",           "Binder",           "Highlighter",      "Eraser",
            "Glue Stick",       "Markers",          "Crayons",          "Paint Brush",      "Canvas",
            "Yoga Mat",         "Dumbbells",        "Jump Rope",        "Resistance Band",  "Football",
            "Soccer Ball",      "Baseball Glove",   "Tennis Racket",    "Bicycle",          "Helmet",
            "Flashlight",       "First Aid Kit",    "Fire Extinguisher","Smoke Detector",   "Door Mat",
            "Curtains",         "Rug",              "Mirror",           "Shelf",            "Storage Bin"
        ]
    
    def __call(params:str):
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
        return choice

    def execute(self) -> str:
        try:
            product = self.__get_random()
            KEY = get_secret("SERPAPI_KEY")
            params = {
                "engine": "amazon",
                "k": product, # k is the search item.
                "api_key": KEY
            }

            data_aggregate:dict = self.__call(params)
            data:List[dict] = data_aggregate["organic_results"][6:16] # only get 10 products and skip the first 6 products as these are sponsored


            with open(f"data/raw/{product}_product.json", "w") as file:
                json.dump(data, file, indent=4)
            
            return "Success"
            
        except Exception as error:
            log,error(error)
            return "Failure"