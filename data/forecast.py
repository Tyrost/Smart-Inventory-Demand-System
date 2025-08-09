from database.Commander import Commander
from ml.train import Train
from ml.model import Model

from utils.misc import create_forecast_id

import logging as log
import pandas as pd
from datetime import date, datetime

logger = log.getLogger(__name__)

def gather_forecast(cutoff:date, horizon_days:int):
    try:
        database = Commander("forecast")
        
        training_model = Train(cutoff, horizon_days)
        clean_data:pd.DataFrame = training_model.prepare_features()
        
        model = Model(clean_data)
        forecasts, mae, rmse = model.execute()
        
        forecasts = forecasts.to_dict("records")
        
        for forecast in forecasts:
            forecast_id = create_forecast_id()
            product_id = forecast.get("product_id")
            forecast_date = datetime.now().date()
            forecast_qty = round(forecast.get("predicted_qty"))
            confidence_low = max(0, int(forecast_qty - rmse))
            confidence_high = int(forecast_qty + rmse)
            model_used = "RandomForest_v1"
            
            record = {
                "forecast_id": forecast_id,
                "product_id": product_id,
                "forecast_date": forecast_date,
                "forecast_qty": forecast_qty,
                "confidence_low": confidence_low,
                "confidence_high": confidence_high,
                "model_used": model_used,
                "rmse": rmse,
                "mae": mae
            }
            
            status = database.create_item(record)
            
            if status != 200:
                raise ConnectionAbortedError("Failed to upload forecast data.")
        log.info("Forecast data upload complete.")
    except Exception as error:
        log.error(error)

