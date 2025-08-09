import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

from typing import Union

class Model:
    def __init__(self, data:pd.DataFrame) -> None:
        self.df = data
    
    def execute(self)->Union[pd.DataFrame, float, float]:

        features = self.df[["sales_avg_price_7_days", "sales_avg_price_30_days", "last_inventory_level"]] # only include relevant columns
        labels = self.df["forecast_qty"]
        product_ids = self.df["product_id"]
        
        # random state 42 w
        x_train, x_test, y_train, y_test, id_train, id_test = train_test_split( # we will separate our data into test and training data
            features, labels, product_ids, test_size=0.2, random_state=1
        )
        # the `random_state` parameter sets a seed that ensures that reproducibility remains in our model for constancy
        # and debugging
        
        
        model =  RandomForestRegressor(n_estimators=100, random_state=1)
        model.fit(x_train, y_train)
        
        preds = model.predict(x_test)
        
        mae = mean_absolute_error(y_test, preds)
        rmse = mean_squared_error(y_test, preds)
        
        results = x_test.copy()
        results["product_id"] = id_test.values

        # store the prediction values
        results["predicted_qty"] = preds

        # Add the actual values from y_test
        results["actual_qty"] = y_test.values

        return results, mae, rmse

    def visualize(self):
        results, mae, rmse = self.execute()

        # Create a single figure and axis
        fig, ax = plt.subplots(figsize=(8, 5))  # ← set the size here instead of separately

        # Format MAE and RMSE as a multiline string
        textstr = '\n'.join((
            r'MAE = %.2f' % (mae, ),
            r'RMSE = %.2f' % (rmse, )
        ))

        # Style for the text box
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        # Add the metrics box inside the plot
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
                verticalalignment='top', bbox=props)

        # Scatter plot of predicted vs actual quantities
        ax.scatter(results["actual_qty"], results["predicted_qty"], alpha=0.6)

        # Add perfect prediction line
        min_val = min(results["actual_qty"].min(), results["predicted_qty"].min())
        max_val = max(results["actual_qty"].max(), results["predicted_qty"].max())
        ax.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--', label='Perfect Prediction Line')

        # Axis labels and styling
        ax.set_xlabel("Actual Quantity")
        ax.set_ylabel("Predicted Quantity")
        ax.set_title("Predicted vs Actual Forecasted Quantity")
        ax.legend()
        ax.grid(True)

        # Display the plot
        plt.show()