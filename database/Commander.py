
from database.Connection import Connection
from database.models import *
from utils.schema import is_valid_schema_input, table_structure
from utils.threading import safe_first

import time
from sqlalchemy import select, distinct, func

from typing import List, Union

import logging as log

logger = log.getLogger(__name__)

class Commander(Connection):
    def __init__(self, table:str) -> None:
        super().__init__()
        self.table_options = ["forecast", "inventory_log", "stock", "sales", "products"]
        self.table_name = table

        self.cmd = None
        self.__set_cmd()
        
    def __set_cmd(self):
        
        match(self.table_name):
            case "products":
                self.cmd = Product
                return
            case "forecast":
                self.cmd = Forecast
                return
            case "inventory_log":
                self.cmd = InventoryLog
                return
            case "sales":
                self.cmd = Sale
                return
            case "stock":
                self.cmd = Stock
                return
            case _:
                raise LookupError(f"Invalid table name: {self.table_name} received")
    
    def __is_valid_attribute(self, value:str)->bool:
        struct = table_structure(self.table_name)
        return value in struct
    
    # ____________________ Usage Endpoints ____________________ #

    def checkout_table(self, new_table):
        if self.table_name == new_table:
            return
        self.table_name = new_table
        self.__set_cmd()
    
    def search_values(self, column:str, name:str, attribute:str = None) -> Union[List[Union[InventoryLog, Sale, Stock, Forecast, Product]], Union[str, int]]:
        try:          
            model = getattr(self.cmd, column) # self.cmd."some_attribute"
            records = self.session.query(self.cmd).filter(model == name).all()
            
            if attribute:
                column = []
                for record in records:
                    entry = getattr(record, attribute)
                    column.append(entry)
                return column

            return records
        except AttributeError:
            log.error("Attribute passed isn't supported.")
        except Exception as error:
            log.error(error)
    
    # ____________________ Create ____________________ #
    
    def create_item(self, elements:dict)->int:
        '''
        Expects a dictionary with the necessary fields for the command-chosen class
        to populate the table with this new record.
        ```
        {
            "_Id": 123,
            "very_specific_field": "val1"
        }
        ```
        Returns a status code element upload.
        '''
        try:
            if not is_valid_schema_input(elements, self.table_name):
                return 406 # if invalid schema passed for this table object...
            
            new_item = self.cmd(**elements)
            self.session.add(new_item)
            self.session.commit()
            return 200
        
        except Exception as error:
            log.error(error)
            return 400

    # ____________________ Read ____________________ #
    
    def count_records(self):
        try:
            query = select(func.count()).select_from(self.cmd)
            executed = self.session.execute(query)
            return executed.scalar()
        
        except Exception as error:
            log.error(error)
        
    def read_row_index(self, index:int)->dict:
        try:
            query = select(self.cmd).limit(1).offset(index)
            result = self.session.execute(query)
            row = result.scalar_one()
            return row.to_dict()
        
        except Exception as error:
            log.error(error)
    
    def read_cols(self, value=None, filter:dict=None, limit=None)->list:
        try:
            query = self.session.query(self.cmd)
            if filter:
                query = query.filter_by(**filter)
                
            records = query.all() if not limit else query.limit(limit).all()
            if value is None:
                return [record.__dict__.copy() for record in records]  # careful, includes _sa_instance_state
            else:
                if not self.__is_valid_attribute(value):  # validate
                    log.warn("attribute was not valid")
                    return []
            return [getattr(record, value) for record in records]
        except Exception as error:
            log.error(error)

    # ____________________ Update ____________________ #
    
    def update_value(self, id_type:dict, attribute:str, new_value):
        try:
            if not (self.__is_valid_attribute(attribute)): # validate passed attribute
                return None
            
            item = safe_first(self.session, self.cmd, id_type)
            if item is None:
                log.info("Skipping update due to timeout")
                return
            # if item:
            #     setattr(item, attribute, new_value)
            #     self.session.commit()
            return item 
        except Exception as error:
            log.error(f"There was an error: {error}")
    
    # ____________________ Misc ____________________ # 
    
    def delete_data(self):
        self.session.query(self.cmd).delete()
        self.session.commit()
        return
     
    def get_unique(self, unique_val):
        try:
            attribute = getattr(self.cmd, unique_val)
            array = self.session.execute(select(distinct(attribute))).scalars().all()
            return array
        
        except Exception as error:
            log.error(f"An error ocurred when fetching unique values: {error}")