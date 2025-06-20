import pandas as pd
import logging as log
from random import randint

from math import ceil, floor

class Allocate:
    
    def __init__(self, data):
        super().__init__()
        
        self.raw_data = data
        self.dataframe = None
        
        self.__get_table_ratings()
        
    # ______________________________________ Filter ______________________________________ #
        
    def __get_table_ratings(self)->pd.DataFrame:

        try:
            aggregate = pd.DataFrame(self.raw_data)
            
            relevant_cols = ["title", "rating", "reviews"]
            ratings = aggregate[relevant_cols]
            
            self.dataframe = ratings
            
        except Exception as error:
            log.error(error)
            
    # ______________________________________ DF Ops ______________________________________ #
    
    def allocate_cold(self, total_allocation:int)->None:
        
        normal_vector:list = self.dataframe["rating"] * self.dataframe["reviews"]
        self.dataframe["normalized_unit"] = normal_vector
        normal_sum = sum(normal_vector)
        
        self.dataframe["standard_factor"] = self.dataframe["normalized_unit"] / normal_sum
        self.dataframe["cold_allocation"] = round(self.dataframe["standard_factor"] * total_allocation, 2)
        
        return
    
    def allocate_adjusted(self, total_allocation:int)->pd.DataFrame:
        
        self.allocate_cold(total_allocation)
        
        lower_bound:list = self.dataframe["cold_allocation"] * 0.20 # 20th percentile
        upper_bound:list = self.dataframe["cold_allocation"] * 0.80 # 80th percentile
        
        adjusted = []
        for i in range(len(self.dataframe)):
            l = floor(lower_bound[i])
            r = ceil(upper_bound[i])

            adjusted_allocation:int = randint(l, r)
            adjusted.append(adjusted_allocation)
            
        self.dataframe["adjusted_allocation"] = adjusted
        return self.dataframe