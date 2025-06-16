
from database.Connection import Connection
from database.models import *
from utils.helper import is_valid_schema_input

from typing import List, Union

import logging as log

logger = log.getLogger(__name__)

class Commander(Connection):
    def __init__(self, table:str) -> None:
        
        self.table_name = table

        self.cmd = None
        self.__set_cmd()
        
        self.session = self.get_session()
        
        
    def __set_cmd(self):
        
        match(self.table_name):
            case "products":
                self.cmd = Product
                return
            case "forecast":
                self.cmd = Forecast
                return
            case "inventory":
                self.cmd = Inventory
                return
            case "sales":
                self.cmd = Sale
                return
            case "stock":
                self.cmd = Stock
                return
            
        raise LookupError(f"Invalid table name: {self.table_name} received")
    
    # ____________________ Usage Endpoints ____________________ #

    
    def search_values(self, column:str, name:str, attribute:str = None) -> Union[List[Union[Inventory, Sale, Stock, Forecast, Product]], Union[str, int]]:
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
    
    def create_item(self, elements:dict)->str:
        '''
        Expects a dictionary with the necessary fields for the command-chosen class
        to populate the table with this new record.
        ```
        {
            "_Id": 123,
            "very_specific_field": "val1"
        }
        ```
        '''
        try:
            if not is_valid_schema_input(elements):
                return f"Data failed to commit due to invalid schema structure"
            
            new_item = self.cmd(**elements)
            self.session.add(new_item)
            self.session.commit()
            return "Data successfully committed"
        except Exception as error:
            return f"Data failed to commit: {error}"

    def update_value(self, id_type:dict, attribute:str, new_value):
        try:
            item = self.session.query(self.cmd).filter_by(**id_type).first()
            if item:
                setattr(item, attribute, new_value)
                self.session.commit()
            return item 
        except Exception as error:
            log.error(f"There was an error: {error}")