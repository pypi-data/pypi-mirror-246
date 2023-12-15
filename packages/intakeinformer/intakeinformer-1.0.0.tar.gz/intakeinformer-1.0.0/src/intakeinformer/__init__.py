# read version from installed package
from importlib.metadata import version
__version__ = version("intakeinformer")

# Import key functions to top-level namespace
from .main_functions import dri_benchmark, get_calories_for_food_query