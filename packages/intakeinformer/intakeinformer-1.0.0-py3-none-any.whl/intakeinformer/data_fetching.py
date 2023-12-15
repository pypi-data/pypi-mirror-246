import requests
from requests.exceptions import HTTPError
import json
import os
import pandas as pd

from bs4 import BeautifulSoup


'''
internal helper function to fetch data from API and parse it into dataframe for future operation
'''
def _fetch_food_data(FDC_Key, query):
    """
    Fetches food data from the USDA FoodData Central API for a specified query.

    This function sends a GET request to the USDA FoodData Central API with a given food query and returns the results as a pandas DataFrame. It handles HTTP errors and returns an empty DataFrame if no data is found.

    Parameters
    ----------
    FDC_Key: str
        The USDA API Key that works as personal access token to the API.
    query : str
        The food query string to search for in the USDA FoodData Central API.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the fetched food data. Each row represents a different food item, with columns for various food attributes.

    Raises
    ------
    HTTPError
        If the HTTP request to the USDA API fails.

    Exception
        For general exceptions that may occur during the API request.

    Examples
    --------
    >>> _fetch_food_data(FDC_Key, "apple")
    DataFrame containing data for various apple products, with columns such as 'description', 'brandOwner', and nutritional information.

    Notes
    -----
    The function uses an internal API key defined as FDC_key. Ensure this key is properly set before using the function. The function is intended for internal use within the package and is not exposed to the end users.

    """
    url_search = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params_search = {
        "api_key": FDC_Key,
        
        "pageSize": 10,     # number of results to return, default to 1 for ease of access
        "pageNumber": 2,   # Page number to retrieve, default to 1
        "dataType": [ "Branded"],
        "sortBy": "publishedDate",
        "sortOrder": "asc",
        "query": query
    }
    data = {}  # Initialize data as an empty dictionary

    try:
        response_food_search = requests.get(url_search, params=params_search)
        response_food_search.raise_for_status()
        data = response_food_search.json()  # Update data with the response
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


    if 'foods' in data:
        '''
        pd.json_normalize is used to flatten the nested JSON structure into a DataFrame. 
        '''
        return pd.json_normalize(data, record_path=['foods'])
    else:
        return pd.DataFrame()




def get_user_food_selection(food_df):
    """
    Prompts the user to select a specific food item from a list presented based on the queried food.

    This function displays a list of food items retrieved from the USDA FoodData Central API, 
    allowing the user to select one. The list includes various brands or types of the food item queried. 
    The user's selection is returned for further processing, such as nutrient analysis or calorie calculation.

    Parameters
    ----------
    food_df : pandas.DataFrame
        A DataFrame containing a list of food items, obtained from the 
        USDA FoodData Central API. Each row represents a different variety or brand 
        of the queried food.

    Returns
    -------
    pandas.DataFrame
        A single-row DataFrame representing the user's selected food item.

    Examples
    --------
    >>> food_df = _fetch_food_data("apple")
    >>> selected_apple = get_user_food_selection(food_df)
    >>> print(selected_apple)

    Notes
    -----
    - The function works as an internal helper function for both main functions.
    """
    if food_df.empty:
        print("No foods found.")
        return None

    # Display the top results to the user
    for i, row in food_df.iterrows():
        brand_owner = row.get('brandOwner', 'No brand information')
        print(f"{i + 1}: {row['description']} ({brand_owner}, {row.get('servingSize', 'N/A')}g)")

    # Ask the user to make a selection
    try:
        choice = int(input("Enter the number of your choice: ")) - 1
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

    # Return the selected food item
    if 0 <= choice < len(food_df):
        return food_df.iloc[choice]
    else:
        print("Invalid selection.")
        return None

def get_user_life_stage():
    """
    Interactively prompts users to identify their life stage category and age range 
    for Dietary Reference Intake (DRI) comparison. 

    This function asks users to choose from predefined life stage categories and age ranges 
    that align with DRI standards. These categories include options for Infants, Children, 
    Males, Females, Pregnancy, and Lactation, with specific age ranges under each. 
    The user's selections are returned as a tuple, which can be used to retrieve appropriate 
    DRI benchmarks for nutrient comparison.

    Returns
    -------
    tuple
        A tuple containing two strings: the life stage category (e.g., 'Children') and 
        the specific age range within that category (e.g., '1–3 y').

    Examples
    --------
    >>> life_stage_info = get_user_life_stage()
    >>> print(life_stage_info)
    ('Children', '1–3 y')
    """
    
    life_stage_categories = ['Infants', 'Children', 'Males', 'Females', 'Pregnancy', 'Lactation']
    age_ranges = {
        'Infants': ['0–6 mo', '6–12 mo'],
        'Children': ['1–3 y', '4–8 y'],
        'Males': ['9–13 y', '14–18 y', '19–30 y', '31–50 y', '51–70 y', '> 70 y'],
        'Females': ['9–13 y', '14–18 y', '19–30 y', '31–50 y', '51–70 y', '> 70 y'],
        'Pregnancy': ['14–18 y', '19–30 y', '31–50 y'],
        'Lactation': ['14–18 y', '19–30 y', '31–50 y']
    }

    # Prompt user to select their life stage category
    print("Please select your life stage category:")
    for i, category in enumerate(life_stage_categories):
        print(f"{i + 1}. {category}")
    category_choice = int(input("Enter the number of your choice: "))
    selected_category = life_stage_categories[category_choice - 1]

    # Prompt user to select their age range within the life stage category
    print(f"Please select your age range for the '{selected_category}' category:")
    for i, age_range in enumerate(age_ranges[selected_category]):
        print(f"{i + 1}. {age_range}")
    age_choice = int(input("Enter the number of your choice: "))
    selected_age_range = age_ranges[selected_category][age_choice - 1]

    return selected_category, selected_age_range

