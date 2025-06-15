
from database.Connection import Connection
from database.models import *

class Commander:
    def __init__(self, table:str) -> None:
        
        self.table_name = table

        self.cmd = None
        self.__set_cmd()
        
        self.session = Connection().get_session()
        
        
    def __set_cmd(self):
        
        match(self.table_name):
            case "products":
                self.cmd = Product()
                return
            case "forecast":
                self.cmd = Forecast()
                return
            case "inventory":
                self.cmd = Inventory()
                return
            case "sales":
                self.cmd = Sale()
                return
            case "stock":
                self.cmd = Stock()
                return
            
        raise LookupError(f"Invalid table name: {self.table_name} received")
    
    # ____________________ User Endpoints ____________________ #