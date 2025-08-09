'''
Call via Lambda function.
'''

from utils.misc import dict_to_config
import config.config as config
from thread import thread_simulation
from data.misc.thread import thread_metrics
from ml.model import Model
from ml.train import Train

def lambda_handler(event, context):
    function = event.get("function", "null")
    configuration:dict = event.get("config", {})
    
    dict_to_config(configuration)
    
    config.validate_config()
    
    if function == "run":
        thread_simulation()
        response = "Database population complete"
    elif function == "metric":
        operation = configuration.get("config").get("metric").get("operation")
        response = thread_metrics(operation)
    elif function == "forecast":
        response = Model(Train()).execute()
    else:
        raise SystemError(f"Invalid function call given: {function}")

    return {
        "status": "success",
        "response": response
    }