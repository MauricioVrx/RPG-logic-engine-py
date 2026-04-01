import pkgutil
import importlib

def load_actions():
    package = __name__

    for _, module_name, _ in pkgutil.walk_packages(__path__, package + "."):
        importlib.import_module(module_name)