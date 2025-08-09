'''
Main module for usage endpoints.
General metrics and data description.
'''

from database.Commander import Commander
import pandas as pd
from datetime import date 

import config.config as config

class Metrics:
    '''
    Ignoring the `date_cutoff` parameter will read all existent data instead.
    '''
    def __init__(self, database:Commander) -> None:
        self.database = database
        self.date_cutoff = None if not config.METRIC_DATE_CUTOFF else config.METRIC_DATE_CUTOFF
        self.data = None
        
        self.__gather_data()
        
    def __gather_data(self):
        if self.date_cutoff:
            data = self.database.read(table_filter=[self.database.table.date <= self.date_cutoff])
        else:
            data = self.database.read()
        assert(len(data) > 0) # assertion for correct usage
        self.data =  pd.DataFrame(data)
    
    def checkout_date(self, date_cutoff):
        
        self.date_cutoff = date_cutoff
        self.__gather_data()

    # __________________ Fundamental Count __________________ #
    
    
    def get_product_counts(self):
        '''
        Ignores date cutoff and focuses on aggregate data of product counts
        '''
        self.database.checkout_table("products")
        unique_products = self.database.get_unique("product_id")
    
        return len(unique_products)
    
    def stockout_counts(self)->list:
        self.database.checkout_table("stock")
        data:list = self.database.read(value="product_id", filter={"is_stockout": True})
        
        return data
    
    def sale_to_restock_ratio(self):
        '''
        Returns a ratio of the counts of product sales to product restocks.
        '''

        self.database.checkout_table("inventory_log")
        
        log = pd.DataFrame(self.database.read())
        log = log[["change_type", "quantity_change", "product_id"]]
        
        sales = log[log["change_type"] == "sale"]
        restock = log[log["change_type"] == "restock"]
        
        sales_sum = abs(sales["quantity_change"].sum())
        restock_sum = restock["quantity_change"].sum()
        
        return round(sales_sum / restock_sum, 3)
        
    # ________________________ Sales ________________________ #
    
    def __ensure_data_exists(self):
        count = self.database.count_records()
        if count <= 0:
            return False
        return True
    
    def __get_sale_growth(self, sales:pd.DataFrame)->float:
        '''
        Returns a proportion of growth compared to past months
        '''
        sales["date"] = pd.to_datetime(sales["date"]) # ensure datetime
        sales["year_month"] = sales["date"].dt.to_period("M").astype(str) # we want to observe monthly change/growth

        monthly_sales = sales.groupby("year_month").agg(
            quantity_sold=("quantity_sold", "sum"),
            month_revenue=("sale_price", "sum")
        )
        
        if not len(monthly_sales) > 1: # we need at least two rows of grouped month data to make a growth metric
            return None
        
        aggregate_growth = []
        prev = None
        for index, row in monthly_sales.iterrows():
            if prev is not None:
                if prev != 0:
                    growth = ((row["month_revenue"] - prev) / prev) * 100 # calculate proportion for this iteration
                else:
                    growth = 0
                aggregate_growth.append(growth)
            prev = row["month_revenue"]

        if len(aggregate_growth) == 1:
            return 100.00 # if these is only one result
        
        return float(round(sum(aggregate_growth) / len(aggregate_growth), 2))
        
    def describe_sales(self)->dict:
        self.database.checkout_table("sales")
        if not self.__ensure_data_exists():
            return None
        
        sales = self.data.copy()
        
        purchase_count = len(self.data)
        
        revenue = sales["sale_price"].sum()
        average_price = float(round(revenue/purchase_count, 2))
        revenue_growth = self.__get_sale_growth(sales)
        
        return {
            "purchase_count": purchase_count,
            "revenue": revenue,
            "average_price": average_price,
            "average_revenue_monthly_growth": revenue_growth
        }
    
    # ________________________ Refunds ________________________ #
    
    def gather_refund_data(self):

        refunded = self.data[self.data["refunded" == 1]]
        refunded_count = len(refunded)
        refunded_proportions = (refunded_count / len(self.data)) * 100
        
        reasons:dict = self.data["reason"].value_counts().to_dict()

        return {
            "refunded_count": refunded_count,
            "refunded_proportions": refunded_proportions,
            "reason_mapping": reasons
        }