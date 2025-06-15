from config.secret_load import get_secret
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging as log

logger = log.getLogger(__name__)

class Connection:
    
    def __init__(self) -> None:
        
        self.host = "localhost"
        self.database = "SIDS"
        
        self._user = "danielcorzo"
        self.__password = get_secret("DB_PW")
        
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
            log.error(f"There was an error when attempting connection with host {self.host}\n Error: {error}")
            return None
    
    def get_session(self):
        try:
            return self.session
        except Exception:
            log.error("An error occurred.")