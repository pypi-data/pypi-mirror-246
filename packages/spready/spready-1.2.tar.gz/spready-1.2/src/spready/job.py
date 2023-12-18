import importlib
from typing import Any, Dict
from .parser import SpreadyDecoratorParser
import os

 
parser = SpreadyDecoratorParser(os.environ["SPREADY_MODULES"])
spreadyModules = parser.spreadyRouts

from .dto import SPRequest



def runjob(routePath: str, params: Dict[str, Any], requestType: str):
    print(f"Running myfunc with {routePath} and {params}")
    if routePath in spreadyModules:
        routePath = spreadyModules[routePath]
    else:
        raise ValueError("Route not found")
    function_string = routePath
    mod_name, func_name = function_string.rsplit('.',1)
    mod = importlib.import_module(mod_name)
    func = getattr(mod, func_name)
    req = SPRequest(json=params, requestType=requestType)
    return func(req)
