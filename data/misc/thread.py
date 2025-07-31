from data.misc.Metrics import Metrics
from database.Commander import Commander

def thread_metrics(operation):
    if not operation:
        raise AssertionError("Must specify a metric operation to continue.")
    
    database = Commander("sales")
    metrics = Metrics(database)
    
    match(operation):
        case "product_counts":
            return metrics.get_product_counts()
        case "stockout_counts":
            return metrics.stockout_counts()
        case "sale_to_restock_ratio":
            return metrics.sale_to_restock_ratio()
        case "describe_sales":
            return metrics.describe_sales()
        case "gather_refund_data":
            return metrics.gather_refund_data()
        case _:
            raise AssertionError(f"Not a valid operation: {operation}. Please select the -h/--help flag further assistance.")
    
    