from secret_load import get_secret
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging as log

logger = log.getLogger(__name__)

class Connection:
    '''
    The purpose of this simulation will be to be ran locally. Hence we wont worry much about database hosting, therefore secrete/dynamic names
    for host, database (name) and user wont be necessary. I will keep my password secret within my .env file.
    '''
    
    def __init__(self) -> None:
        
        self.host = get_secret("DB_HOST")
        self.database = get_secret("DB_NAME")
        
        self._user = get_secret("DB_USER")
        self.__password = get_secret("DB_PASSWORD")
        
        self.session = None
        self.engine = None
        
        self.__init_session()
    
    # ____________________ Main Setters ____________________ #
    
    def __init_session(self):
        try:
            DATABASE_URL = f"mysql+pymysql://{self._user}:{self.__password}@{self.host}/{self.database}"
            
            self.engine = create_engine(DATABASE_URL)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.session = SessionLocal()
            
        except Exception as error:
            raise Exception(f"There was an error when attempting connection with host {self.host}\n Error: {error}")