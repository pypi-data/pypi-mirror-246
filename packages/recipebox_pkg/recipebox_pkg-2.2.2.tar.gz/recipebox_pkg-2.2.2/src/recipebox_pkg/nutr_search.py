import pandas as pd
import requests
import os
import json
from IPython.display import display, Image


def nutrient_search_recipe(api_key, nutrients):
    """
    Search for recipes based on specified nutrient parameters using the Spoonacular API.

    Parameters:
    - api_key (str): The API key for accessing the Spoonacular API.
    - nutrients (dict): Dictionary containing nutrient parameters for the recipe search.

    Returns:
    - pd.DataFrame or None: A DataFrame containing recipe information or None if no recipes are found.
    """
    if nutrients is None:
        raise ValueError("Nutrients cannot be None.")
    url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByNutrients'
    params = nutrients

    headers = {
        'x-rapidapi-host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com',
        'x-rapidapi-key': api_key
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        recipe = response.json()
        recipe_df = pd.DataFrame(recipe)
        return recipe_df
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {e}")
        return None

    except pd.errors.EmptyDataError:
        print("No recipes found.")
        return None
    
    

def display_images_nutrient(recipe_df):
    """
    Display nutrient information and images for each recipe in a DataFrame.

    Parameters:
    - recipe_df (pd.DataFrame): DataFrame containing recipe information, including 'title', 'id', 'calories', 'protein', 'fat', 'carbs', and 'image' columns.

    This function iterates over the DataFrame, printing the title, recipe ID, and nutrient information for each row,
    and then displays the corresponding image.

    Example:
    >>> df = pd.DataFrame({'title': ['Spaghetti Carbonara', 'Chicken Alfredo'],
    ...                    'id': [123, 456],
    ...                    'calories': [500, 700],
    ...                    'protein': [20, 30],
    ...                    'fat': [15, 25],
    ...                    'carbs': [50, 40],
    ...                    'image': ['https://example.com/spaghetti.jpg', 'https://example.com/chicken.jpg']})
    >>> display_images_nutrient(df)
    """
    for _, row in recipe_df.iterrows():
        print(f"Title: {row['title']}")
        print(f"Recipe ID: {row['id']}")
        print(f"Calories: {row['calories']:<4}; Protein: {row['protein']:<4}; Fat: {row['fat']:<4}; Carbohydrate: {row['carbs']:<4}")
        display(Image(url=row['image'], width=200))