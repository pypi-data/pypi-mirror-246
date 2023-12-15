import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np


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

def plot_calorie_comparison(calorie_data):
    """
    Generates and displays a bar chart for comparing the calorie content of selected food items.

    Serves as an important visualization helper function for IntakeInformer's functionality One - calculating calorie intakes
    
    Parameters
    ----------
    calorie_data : dict
        A dictionary where keys are food item names and values are their corresponding calorie content per 100g. 
        It should also contain a 'total' key for the sum of calories.

    Returns
    -------
    None
        This function displays a bar chart.

    Examples
    --------
    >>> calorie_data = {'BANANA FREEZE DRIED FRUIT': 2000.0, 'GALA APPLES': 28.57, 'ORGANIC VALENCIA ORANGES': 29.22, 'total': 2057.79}
    >>> plot_calorie_comparison(calorie_data)
    # This will display a bar chart comparing the calorie content of the listed food items.
    """
    if 'total' in calorie_data:
        total_calories = calorie_data.pop('total')
    
    food_items = list(calorie_data.keys())
    calories = [calorie_data[item] for item in food_items]

    plt.figure(figsize=(10, 6))
    plt.bar(food_items, calories, color='skyblue')
    plt.xlabel('Food Items')
    plt.ylabel('Calories per 100g')
    plt.title('Comparison of Calorie Content')
    plt.xticks(rotation=45)
    plt.axhline(y=total_calories, color='r', linestyle='-', label=f'Total Calories: {total_calories:.2f}')
    plt.legend()
    plt.show()




def plot_nutrient_comparison(actual_nutrients, df_combined, life_stage_info):
    """
    Generates and displays a bar chart comparing actual nutrient intake against 
    Dietary Reference Intake (DRI) recommendations for a specific life stage.

    Serves as an essential helper function for  IntakeInformer's functionality Two - benchmarking against DRI nutrition allowances.

    Parameters
    ----------
    actual_nutrients : dict
        A dictionary containing the actual nutrient values of the selected food item. 
        Each key-value pair corresponds to a nutrient and its intake value.
    df_combined : pandas.DataFrame
        A DataFrame consolidating DRI values for various nutrients across different life stages.
    life_stage_info : tuple
        A tuple containing the life stage category (e.g., 'Children') and the specific 
        age range (e.g., '1–3 y') for which DRI values are to be compared.

    Returns
    -------
    None
        Displays a bar chart visualization but does not return any value.

    Examples
    --------
    >>> actual_nutrients = {'Carbohydrate(g/d)': 30, 'Proteinb(g/d)': 15, 'Fat(g/d)': 10}
    >>> life_stage_info = ('Children', '1–3 y')
    >>> plot_nutrient_comparison(actual_nutrients, df_combined, life_stage_info)
    [Bar chart is displayed showing the comparison between actual nutrient intake and DRI]

    """
    life_stage_category, age_range = life_stage_info

    # Find the start index for the life stage category
    start_index = df_combined[df_combined['Life StageGroup'] == life_stage_category].index[0]

    # Locate the row for the specific age range within the category
    life_stage_row = df_combined.loc[start_index:].query("`Life StageGroup` == @age_range").iloc[0]

    # Extract DRI values for each nutrient in actual_nutrients
    dri_nutrients = {}
    for nutrient in actual_nutrients.keys():
        # If the nutrient is found in the DRI data and is not NaN, use its value; otherwise, use 0
        dri_value = life_stage_row.get(nutrient)
        dri_nutrients[nutrient] = 0 if dri_value is None or np.isnan(dri_value) else dri_value

    # Filter out nutrients with None values in actual_nutrients
    actual_nutrients = {k: v for k, v in actual_nutrients.items() if v is not None}

    # Define the labels, positions, and width for the bars
    labels = actual_nutrients.keys()
    actual_values = actual_nutrients.values()
    dri_values = [dri_nutrients.get(key, 0) for key in labels]  # Get DRI values or default to 0
    x = range(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x, actual_values, width, label='Actual')
    rects2 = ax.bar([p + width for p in x], dri_values, width, label='DRI')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Nutrient Amount')
    ax.set_title(f'Comparison of Actual Intake vs. DRI Recommendations for {age_range} in {life_stage_category}')
    ax.set_xticks([p + width / 2 for p in x])
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()

    plt.show()
