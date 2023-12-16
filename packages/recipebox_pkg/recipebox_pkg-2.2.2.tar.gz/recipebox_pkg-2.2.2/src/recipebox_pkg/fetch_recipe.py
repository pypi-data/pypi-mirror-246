import pandas as pd
import requests
import os
import json


def search_recipes(api_key, query, r_diet = None, r_excludeIngredients = None, r_intolerances = None, r_number = 10):  
    """
    Search for recipes based on a specified query and additional parameters using the Spoonacular API.

    Parameters:
    - api_key (str): The API key for accessing the Spoonacular API.
    - query (str): The search query for recipes.
    - r_diet (str): The diet type to filter recipes (e.g., 'vegetarian', 'vegan').
    - r_excludeIngredients (str): Ingredients to exclude from the recipes.
    - r_intolerances (str): Intolerances to consider when searching for recipes.
    - r_number (int): The maximum number of recipes to retrieve (default is 10).

    Returns:
    - dict or None: A dictionary containing recipe information or None if an error occurs.
    """
    url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search'
    params = {'query': query,
              'diet': r_diet,
              'excludeIngredients': r_excludeIngredients,
              'intolerances': r_intolerances,
              'number': r_number      
             }
    headers = {
        'x-rapidapi-host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com',
        'x-rapidapi-key': api_key } 
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        recipe_response = response.json()
        return recipe_response

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def convert_recipes(response):
    """
    Convert recipe information from Spoonacular API response to a styled DataFrame.

    Parameters:
    - response (dict): The response from the Spoonacular API containing recipe information.

    Returns:
    - pd.io.formats.style.Styler: A styled DataFrame with selected columns and formatted 'sourceUrl' column.
    """
    result = response['results']
    df = pd.DataFrame(result)
    df = df.set_index(['id'], inplace=False)  
    new_order = ['title', 'servings', 'readyInMinutes', 'sourceUrl']
    new_df = df[new_order]
    styled_df = new_df.style
    styled_df = styled_df.format({'sourceUrl': lambda x: f'<a href="{x}" target="_blank">{x}</a>'})
    return styled_df