# recipebox_pkg

A Python package designed for fetching information about recipes.

## Installation

```bash
$ pip install recipebox_pkg
```
## Features

- **Explore Recipe Details:** Access comprehensive information about recipes through user queries.

- **Nutrition Insights:** Retrieve detailed nutritional information tailored to specific dietary constraints.

- **Ingredient Details:** Discover essential details about ingredients required for a recipe.

- **Visualize the Dish:** View images showcasing the appearance of the prepared dish.

## Usage

```python
# Import the necessary function from recipebox_pkg
from recipebox_pkg import (fetch_recipe, id_search, ing_search, nutr_search)

# Replace the empty string with actual API key
api_key = 'your_actual_api_key'
```
```
# Use the fetch_recipe.search_recipes function to search for recipes 
recipes = fetch_recipe.search_recipes(api_key, 'pizza')

# Convert the retrieved recipes into a Pandas DataFrame
recipes_retrieved = fetch_recipe.convert_recipes(api_key, recipes)
```
```
# Define a list of ingredients you want to search for recipes
ingredients_list = ['beef', 'potato']

recipe_ingr = ing_search.ingredient_search_recipe(api_key, ingredients_list, number=5)

ingr_image = ing_search.display_images_ingredients(recipe_ingr)
```
```
# Define nutritional constraints using a dictionary
nutr_constraints = {'minProtein':'20', 'maxFat':'50' }

nutr_recipe = nutr_search.nutrient_search_recipe(api_key, nutr_constraints)

nutr_image = nutr_search.display_images_nutrient(nutr_recipe)
```

```
example_recipe_id = 123456
recipe = id_search.Recipe_id(pick_id, api_key)

# Retrieve information about the ingredients used in the recipe
ingredient_info = recipe.search_ingredient_id()

# Retrieve nutritional information for the recipe
nutr_info = recipe.search_nutrient_id()

# Retrieve information about the equipment required for the recipe
equipment_info = recipe.search_equipment_id()

# Retrieve raw instruction data for the recipe
raw_instruction = recipe.search_instruction_id()

# Convert the raw instruction data into a more usable format
instruction_info = recipe.convert_instruction(raw_instruction)
```
```
# List of recipe IDs for which you want to search for taste information
example_id_list = [123456, 987654]

# Retrieve taste information for the specified recipe IDs
taste = recipe.search_taste_id(id_list)
```
## Dependencies

This package requires the following Python libraries:
- Pandas
- Requests

To install these libraries, run:

```bash
pip install pandas requests
```
## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`recipebox_pkg` was created by Yuchen An. It is licensed under the terms of the MIT license.

## Credits

`recipebox_pkg` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

## Links

[Documentation](https://recipebox-pkg.readthedocs.io/en/latest/)

[Recipe-Food-Nutrition API Documentation](https://spoonacular.com/food-api/docs)

[TestPyPI](https://test.pypi.org/project/recipebox_pkg/)

