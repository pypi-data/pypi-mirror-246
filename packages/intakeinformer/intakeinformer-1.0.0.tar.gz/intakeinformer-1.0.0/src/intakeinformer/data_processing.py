import pandas as pd
import re


def calculate_calories_from_selection(selected_items):
    """
    Calculates the calorie content per 100g for user-selected food items and returns a dictionary with individual and total calories.
    It first tries to use the 'Energy' nutrient value (Energy_id = 1008) and falls back to calculating calories from protein, fat, and carbohydrates if 'Energy' is not located.

    Parameters
    ----------
    selected_items : list
        A list of DataFrame rows, each representing a user-selected food item. Each row should contain the food nutrients data.

    Returns
    -------
    dict
        A dictionary where each key is the food item's name, and the corresponding value is its calorie content per 100g. 
        The dictionary also includes a 'total' key representing the sum of calories from all selected items.

    Examples
    --------
    # Assuming selected_banana, selected_apple, and selected_orange are DataFrame rows obtained from user selections
    >>> selected_items = [selected_banana, selected_apple, selected_orange]
    >>> calories_content = calculate_calories_from_selection(selected_items)
    >>> print(calories_content)
    {'Banana': 89.0, 'Apple': 52.0, 'Orange': 47.0, 'total': 188.0}
    """

    calories_dict = {}
    total_calories = 0

    # Nutrient IDs
    ENERGY_ID = 1008
    CARBS_ID = 1005
    FAT_ID = 1004
    PROTEIN_ID = 1003

    for item in selected_items:
        food_name = item['description']
        food_calories = 0  # Initialize calories for this food item

        # Extract the nutrients data
        nutrients_df = pd.json_normalize(item['foodNutrients'])
        nutrients = nutrients_df.set_index('nutrientId').to_dict('index')

        # Get the serving size in grams
        serving_size = item.get('servingSize', 100)  # Default to 100g if not specified

        # Calculate calories per 100g
        if ENERGY_ID in nutrients and 'value' in nutrients[ENERGY_ID]:
            energy_per_serving = nutrients[ENERGY_ID]['value']
            food_calories = (energy_per_serving / serving_size) * 100
        else:
            # Fallback to calculating from protein, fat, and carbohydrates
            for nutrient_id, multiplier in zip([CARBS_ID, FAT_ID, PROTEIN_ID], [4, 9, 4]):
                if nutrient_id in nutrients and 'value' in nutrients[nutrient_id]:
                    nutrient_value_per_100g = (nutrients[nutrient_id]['value'] / serving_size) * 100
                    food_calories += nutrient_value_per_100g * multiplier

        # Add to the total and the dictionary
        calories_dict[food_name] = round(food_calories, 2)
        total_calories += food_calories

    # Add total calories to the dictionary
    calories_dict["total"] = round(total_calories, 2)

    return calories_dict




def extract_nutrients(food_nutrients):
    """
    Extracts macronutrient and other nutrient information from the foodNutrients data structure, 
    obtained from the USDA FoodData Central API via get_user_food_selection() function.

    This function processes a list of nutrient data for a given food item, identifying and extracting 
    key nutrients like carbohydrates, proteins, fats, and selected vitamins and minerals. 
    It utilizes regular expressions to match nutrient names from the data with predefined patterns,
    ensuring accurate identification despite potential variations in nutrient naming.

    Parameters
    ----------
    food_nutrients : list
        A list of dictionaries, each representing a nutrient data point for a food item. 
        Each dictionary typically includes nutrient names, values, units, and other metadata.

    Returns
    -------
    dict
        A dictionary mapping nutrient names (e.g., 'Carbohydrate(g/d)', 'Proteinb(g/d)') to their 
        corresponding values extracted from the food_nutrients data. If a nutrient is not found, 
        its value in the dictionary is set to None.

    Examples
    --------
    >>> food_nutrients = [
            {'nutrientName': 'Protein', 'value': 2.5},
            {'nutrientName': 'Total lipid (fat)', 'value': 0.5},
            {'nutrientName': 'Carbohydrate, by difference', 'value': 30},
            {'nutrientName': 'Fiber, total dietary', 'value': 2},
            {'nutrientName': 'Calcium, Ca', 'value': 50},
            # ... more nutrients ...
        ]
    >>> extracted_nutrients = extract_nutrients(food_nutrients)
    >>> print(extracted_nutrients)
    {'Carbohydrate(g/d)': 30, 'Total Fiber(g/d)': 2, 'Fat(g/d)': 0.5, 'Proteinb(g/d)': 2.5, 'Calcium (mg/d)': 50, ...}
    """
    
    # Define the regex patterns for the macronutrients
    patterns = {
        'Carbohydrate(g/d)': re.compile(r'carbohydrate, by difference', re.I),
        'Total Fiber(g/d)': re.compile(r'fiber, total dietary', re.I),
        'Fat(g/d)': re.compile(r'total lipid \(fat\)', re.I),
        'Proteinb(g/d)': re.compile(r'protein', re.I),
        'Calcium (mg/d)': re.compile(r'calcium, ca', re.I),
        'Iron (mg/d)': re.compile(r'iron, fe', re.I),
        'Potassium (mg/d)': re.compile(r'potassium, k', re.I),
        'Sodium (mg/d)': re.compile(r'sodium, na', re.I),
        'Vitamin A(μg/d)a': re.compile(r'vitamin a, (?:IU|μg)', re.I),
        'Vitamin C(mg/d)': re.compile(r'vitamin c, total ascorbic acid', re.I),
        'Vitamin D(μg/d)b,c': re.compile(r'vitamin d(?:3)?', re.I),
        'Vitamin B12(μg/d)': re.compile(r'vitamin b-?12', re.I)
    }
    
    # Initialize a dictionary to hold the macronutrients
    macronutrients = {key: None for key in patterns.keys()}
    
    # Search for the macronutrients in the food_nutrients data
    for nutrient in food_nutrients:
        nutrient_name = nutrient.get('nutrientName', '').lower()
        for key, pattern in patterns.items():
            if pattern.search(nutrient_name):
                # Convert value to float and store in the dictionary
                macronutrients[key] = float(nutrient.get('value', 0))
                break  # Stop searching after finding the nutrient
    
    return macronutrients

