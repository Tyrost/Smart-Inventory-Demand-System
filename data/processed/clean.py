from datetime import date
import random
from data.raw.Builder import Builder
import pandas as pd

class Clean(Builder):
    
    def __init__(self) -> None:
        
        super().__init__()
        
        self.clean_df = None
        self.execute()

    @staticmethod
    def create_id():
        '''
        The plan for ID creation was the following:
        ID: [CountryCode (2)][Date (YY/MM/DD)][AutoIncrement (5)]
        '''
        raw_date = str(date.today())
        parsed_date = raw_date[2:].replace("-", "")
        
        with open("id.txt", "r+") as file:
            
            content = file.read().strip()
            serial_num = int(content)
            
            file.seek(0)
            file.truncate()
            file.write(str(serial_num + 1).zfill(5))
        
        ID = "US"+parsed_date+content # hardcoded country for now
        
        return ID

    def __get_name(self, raw_name:str):
        '''
        example input:
        Cordless Vacuum Cleaner,580W 48KPA 65Mins Vacuum Cleaners for Home,Self-Standing Stick Vacuum with Anti-Tangle Brush & OLED Touch Screen,Rechargeable Vacuum Cordless for Pet Hair,Carpet,Hardwood Floor
        example output:
        Cordless Vacuum Cleaner
        '''
        # cleansing
        name_list = raw_name.replace("\n", " ").replace("-", " ").replace(",", " ") # replace to a common delimeter
        selective = name_list.split(" ")[0:3] # 3rd index not included
        return " ".join(selective)

    def __get_cost(self, price:float):
        '''
        Public mediums usually don't expose the unit cost of production for their products. This is the case
        with our API; so we will have to craft our own computation to approximate and replicate the cost of production 
        give the retail price. 
        To give a best approximate simulating the value, I will use random number specifiers to 
        compute a percentage gain for the product (example price * 0.4 = 60% gain when product is sold)
        '''
        upper_lim = 0.70
        lower_lim = 0.30
        value = random.uniform(lower_lim, upper_lim)
        
        return round(price * value, 2)

    def get_raw_data(self):
        return self.raw_data
    
    def get_raw(self):
        return self.raw_data
    
    def get_dataframe(self):
        return self.clean_df
    
    def get_clean(self):
        result = []
        data = self.raw_data
        
        for product in data:
            ID = self.create_id()
            NAME = self.__get_name(product["title"])
            CATEGORY = self.product
            PRICE = float(product["price"].replace("$", "").replace(",", "")) # selling price. Clean the number first to match out db
            COST = self.__get_cost(PRICE)
            
            new = {
                "product_id": ID,
                "product_name": NAME,
                "category": CATEGORY,
                "unit_price": PRICE,
                "cost": COST,
            }
            
            result.append(new)
        
        self.clean_df = pd.DataFrame(result)
            
        return result