from .data_fetching import _fetch_food_data, get_user_food_selection, get_user_life_stage
from .data_processing import calculate_calories_from_selection, extract_nutrients
from .visualization import plot_calorie_comparison, plot_nutrient_comparison

import os
import pandas as pd

def load_dri_combined():
    """
    Loads the combined DRI DataFrame from a pickle file.
    
    Ensure df_combined is loaded from the pickle file installed alongside all other dependencies and available for use when needed.
    
    Returns
    -------
    pandas.DataFrame
        The DataFrame containing combined DRI data.
    """
    # Construct the relative path to the pickle file
    package_directory = os.path.dirname(__file__)  # Directory of the current file
    relative_path = os.path.join(package_directory, 'data', 'dri_combined.pkl')

    # Load the DataFrame from the pickle file
    df_combined = pd.read_pickle(relative_path)
    return df_combined

df_combined = load_dri_combined()

def get_calories_for_food_query(FDC_Key, *food_queries):
    """
    Calculates and displays the calorie content per 100g for each queried food item. 

    This function takes multiple food queries and fetches their nutrient data from the USDA FoodData Central API. 
    Users are then prompted to select specific varieties or brands of each food item. 
    The function calculates and returns the calorie content of these selected items, 
    normalized to a standard serving size of 100g. The calorie calculation considers 
    the three main macronutrients (carbohydrates, fats, and proteins) of the food.

    Parameters
    ----------
    FDC_Key: str
        The USDA API Key that works as personal access token to the API.
    *food_queries : str
        Variable number of string arguments, each representing a food item query.
        For example, 'banana', 'apple', 'orange'.

    Returns
    -------
    dict
        A dictionary with the calorie content for each selected food item per 100g, 
        along with the total calorie count of all selected items. 
        Format: {'Food Item': calories, ..., 'total': total_calories}

    Examples
    --------
    >>> get_calories_for_food_query(FDC_Key, "banana", "apple", "orange")
    {'BANANA FREEZE DRIED FRUIT': 2000.0, 'GALA APPLES': 28.57, 'ORGANIC VALENCIA ORANGES': 29.22, 'total': 2057.79}

    Notes
    -----
    The function internally calls:
    `_fetch_food_data` for data retrieval
    `get_user_food_selection` for user selection. 
    'calculate_calories_from_selection' for the actual calorie calculation
    Calorie calculation is based on the USDA nutritional data and is normalized to a 100g serving size for each item.
    
    """
    selected_items = []
    for query in food_queries:
        # Fetch food data
        food_df = _fetch_food_data(FDC_Key, query)

        # Get user's selection for each query
        print(f"Select an item for '{query}':")
        selected_food = get_user_food_selection(food_df)
        if selected_food is not None:
            selected_items.append(selected_food)
        else:
            print(f"No valid selection made for '{query}'. Skipping...")

    # Calculate calories for the selected items and plot the results
    if selected_items:
        calorie_info = calculate_calories_from_selection(selected_items)
        
        # Make a copy of calorie_info before plotting
        calorie_info_for_plotting = calorie_info.copy()
        plot_calorie_comparison(calorie_info_for_plotting)  
        
        return calorie_info
    else:
        return "No calorie information available. No valid selections were made."



def dri_benchmark(FDC_Key, *food_queries):
    """
    Compares the nutrient content of the queried foods against Dietary Reference Intake (DRI) benchmarks.

    This function evaluates the following nutrients:
    - Macronutrients: Carbohydrates, Total Dietary Fiber, Fat, Protein
    - Vitamins: Vitamin A, Vitamin C, Vitamin D, Vitamin B12
    - Elements (Minerals): Calcium, Iron, Potassium, Sodium

    It takes multiple food queries, fetches their nutrient data from the USDA FoodData Central API, 
    allows the user to select specific food items, and compares their combined nutrient content to DRI benchmarks.
    A visualization is generated showing the comparison against recommended values for a selected life stage group.
    
    Parameters
    ----------
    FDC_Key: str
        The USDA API Key that works as personal access token to the API.
    *food_queries : str
        Variable number of arguments, each a string representing a food item to query. 
        For example, 'apple', 'banana', 'spinach'.

    Returns
    -------
    None
        Displays a bar chart visualization comparing actual nutrient intake against DRI benchmarks. 
        The chart includes macronutrients, vitamins, and elements.

    Examples
    --------
    >>> dri_benchmark(FDC_Key, 'apple', 'banana', 'spinach')
    
    This will prompt the user to select specific types of apple, banana, and spinach from a list of options, 
    then display a chart comparing the combined nutrient content of these selections against DRI benchmarks.

    Notes
    -----
    The function internally calls several helper functions: 
    - `_fetch_food_data` to retrieve food data from the USDA API.
    - `get_user_food_selection` for user to select specific food items.
    - `extract_nutrients` to extract nutrient data from the selected food items.
    - `get_user_life_stage` to get the user's life stage group for DRI comparison.
    - `plot_nutrient_comparison` to generate the comparative visualization.

    The visualization is based on the combined nutrient content of all selected food items and 
    compares it to DRI values for the user's specific life stage group.
    """

    combined_nutrients = {}

    for query in food_queries:
        food_data = _fetch_food_data(FDC_Key, query)
        selected_food = get_user_food_selection(food_data)

        # Check if selected_food is not empty before proceeding
        if not selected_food.empty:
            nutrients = extract_nutrients(selected_food['foodNutrients'])
            combined_nutrients.update(nutrients)


    plot_nutrient_comparison(combined_nutrients, df_combined, get_user_life_stage())


