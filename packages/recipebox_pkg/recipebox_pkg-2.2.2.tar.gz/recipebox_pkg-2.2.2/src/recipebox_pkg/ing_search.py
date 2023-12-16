import pandas as pd
import requests
import os
import json
from IPython.display import display, Image


def ingredient_search_recipe(api_key, ingredient_list, number = 5):
    """
    Search for recipes based on specified ingredients using the Spoonacular API.
    
    Parameters:
    - api_key (str): The API key for accessing the Spoonacular API.
    - ingredient_list (list): List of ingredients to search for in recipes.
    - number (int): The maximum number of recipes to retrieve (default is 5).

    Returns:
    - pd.DataFrame or None: A DataFrame containing recipe information or None if no recipes are found.    
    """
    url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients'
    params = {
        'ingredients': ingredient_list,
        'number': number,
        'ignorePantry': 'true',
        'ranking': 1
    }     
    headers = {
        'x-rapidapi-host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com',
        'x-rapidapi-key': api_key } 
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        recipe = response.json()
        recipe_df = pd.DataFrame(recipe)
        df = recipe_df[['id', 'title', 'image']]
        return df
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {e}")
        return None

    except pd.errors.EmptyDataError:
        print("No recipes found.")
        return None
    

def display_images_ingredients(df):
    """
    Display images for each recipe in a DataFrame.

    Parameters:
    - df (pd.DataFrame): DataFrame containing recipe information, including 'title', 'id', and 'image' columns.

    This function iterates over the DataFrame, printing the title and recipe ID for each row,
    and then displays the corresponding image.

    Example:
    >>> df = pd.DataFrame({'title': ['Spaghetti Carbonara', 'Chicken Alfredo'],
    ...                    'id': [123, 456],
    ...                    'image': ['https://example.com/spaghetti.jpg', 'https://example.com/chicken.jpg']})
    >>> display_images_ingredients(df)
    """
    for _, row in df.iterrows():
        print(f"Title: {row['title']}")
        print(f"Recipe ID: {row['id']}")
        display(Image(url=row['image'], width=200))
        print()