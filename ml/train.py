from datetime import date
from database.Commander import Commander
from datetime import timedelta

import pandas as pd

class Train:
    '''
    The class mainly prepares the aggregate data to predict `horizon_days` ahead of the current time.
    Within this class, we choose the predictor variables (features) that we will use to train and test our
    model against to be able to predict the trend of how much stock is gonna be needed for a specific product.
    '''
    
    def __init__(self, cutoff:date, horizon_days) -> None:
        
        self.database = Commander("sales")
        
        self.cutoff = cutoff
        self.horizon = horizon_days
        
    def __handle_look_window(self):
        '''
        This is a simple filtering function that will fetch our data from DB based on a few conditions.
        First, we want to gather data that include a date equal to our prognostication. For example, we want to prognosticate `x` feature before/after
        `y` amount of days (`self.horizon` as our attribute). Then we will filter DB data that is within the `y` date boundary.  
        Second, since we are specifying that our data will come in from the `sales` and `inventory_log` tables then we will have to specify that within the logs, 
        we are only interested on `sale` data, since restock is irrelevant to our goal.
        
        We will return `y` days prior to our `horizon` as our `feature window`, and `y` days after it as our `label window`.
        '''
        # set our windows
        lookback = self.cutoff - timedelta(days=self.horizon)
        lookforth = self.cutoff + timedelta(days=self.horizon)

        date_object = self.database.table.date # gather the object's date attribute (since both table's date attribute match)
        
        if "inventory_log" == self.database.table_name: # case: we are working with inventory_log data
            feature_filter = [date_object < self.cutoff, date_object >= lookback, self.database.table.change_type == "sale"]
            label_filter = [date_object >= self.cutoff, date_object < lookforth, self.database.table.change_type == "sale"]
        elif "sales" == self.database.table_name:
            feature_filter = [date_object < self.cutoff, date_object >= lookback]
            label_filter = [date_object >= self.cutoff, date_object < lookforth]
        
        # fetch data as appropriate
        feature_window = self.database.read(table_filter=feature_filter)
        label_window = self.database.read(table_filter=label_filter)
        
        assert(len(feature_window) != 0 and len(label_window) != 0)
        
        return feature_window, label_window

    @staticmethod
    def __get_latest_inventory(group:pd.DataFrame)->pd.Series:
        '''
        Helper that allows us to get the latest date value for each product.
        '''
        latest_row = group.loc[group["date"].idxmax()]
        return pd.Series({
            "last_inventory_level": latest_row["stock_level"]
        })
        
    def __compute_feature_window(self, df:pd.DataFrame, lookback_days:int, prefix:str)->pd.DataFrame:
        df = df.copy()
        filtered = df[(df["date"] < self.cutoff) & (df["date"] >= self.cutoff - pd.Timedelta(days=lookback_days))]

        # https://www.geeksforgeeks.org/pandas/python-pandas-dataframe-groupby/ <-- I love you :')
        
        # Depending on what table we want to talk about, we will want different data.
        # In the case of the inventory_logs data, we will want to gather only the latest stock level for
        # each product.
        # For the sales, we will gather the total sales, as well as the mean price in case we need it.
        if prefix == "sales":
            grouped = filtered.groupby("product_id").agg(
                total=("quantity_sold", "sum"),  
                avg_price=("sale_price", "mean")
            )
            grouped = grouped.rename(columns={
                "avg_price": f"{prefix}_avg_price_{lookback_days}_days"
            })
            
        if prefix == "logs":
            grouped = filtered.groupby("product_id").apply(Train.__get_latest_inventory).reset_index()
        
        return grouped.reset_index() 
    
    def prepare_features(self)->pd.DataFrame:
        '''
        Prepares features using helper functions.
        '''
        
        # Get feature/label windows for both sales and logs
        self.database.checkout_table("sales")
        sale_feature_window, sale_label_window = self.__handle_look_window()
        
        self.database.checkout_table("inventory_log")
        log_feature_window, log_label_window = self.__handle_look_window() # we dont actually need the label window for logs
        
        # turn the two features into dataframes
        sale_feature_df = pd.DataFrame(sale_feature_window)
        log_feature_df = pd.DataFrame(log_feature_window)
        
        # turn the sales label window into dataframe 
        sales_label_df = pd.DataFrame(sale_label_window)

        labels = sales_label_df.groupby("product_id").agg(
            forecast_qty=("quantity_sold", "sum")
        )

        # gather the necessary information required from each respective table
        sales_7:pd.DataFrame = self.__compute_feature_window(sale_feature_df, 7, "sales")
        sales_30:pd.DataFrame = self.__compute_feature_window(sale_feature_df, 30, "sales")
        
        log_latest_qty:pd.DataFrame = self.__compute_feature_window(log_feature_df, 30, "logs")
        
        sale_features = sales_7.merge(sales_30, on="product_id", how="outer")
        
        features = sale_features.merge(log_latest_qty, on="product_id", how="inner")
        features = features.merge(labels, on="product_id", how="left")
        
        features["cutoff_date"] = self.cutoff
        features = features.drop(columns=["total_x", "total_y", "index"]) # clean up repeated columns

        return features