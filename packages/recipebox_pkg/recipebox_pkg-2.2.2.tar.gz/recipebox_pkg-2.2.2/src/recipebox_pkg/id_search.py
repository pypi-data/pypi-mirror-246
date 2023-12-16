import pandas as pd
import requests
import os
import json

class Recipe_id:
    
    def __init__(self, id, api_key):
        self.id = id
        self.api_key = api_key
        
        
    def dict_reader(self, input_dict):
        """
        Process a dictionary into a Pandas Series.

        Parameters:
        - input_dict (dict): The input dictionary to process.

        Returns:
        - pd.Series: Processed Pandas Series.
        """
        row_data = {}
        for i in input_dict.keys():
            info = input_dict[i]
            for j in info.keys():
                row_data[f"{i}_{j}"] = info[j]
        return pd.Series(row_data)    
     
    def list_reader(self, input_dict):
        """
        Process a dictionary into a Pandas Series.

        Parameters:
        - input_dict (dict): The input dictionary to process.

        Returns:
        - pd.Series: Processed Pandas Series.
        """
        row_data = {}
        for i in input_dict.keys():
            info = input_dict[i]
            row_data[f"{i}"] = info
        return pd.Series(row_data)

        
    def search_ingredient_id(self):
        """
        Search for ingredient information using the Spoonacular API.

        Returns:
        - pd.DataFrame or None: A DataFrame containing ingredient information or None if an error occurs.
        """
        url = f'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{self.id}/ingredientWidget.json'
        params = {'id': self.id
        } 
        headers = {
            'x-rapidapi-host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com',
            'x-rapidapi-key': self.api_key } 
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            ingredient= response.json()
            ingredients_df = pd.DataFrame(ingredient)
            ingredients_df = pd.concat([ingredients_df, ingredients_df ['ingredients'].apply(self.list_reader)], axis=1)
            ingredients_df = pd.concat([ingredients_df, ingredients_df['amount'].apply(self.dict_reader)], axis=1)
            ingredients_df= ingredients_df.drop(columns=['image', 'amount', 'ingredients'])
            return  ingredients_df
        except Exception as e:
            print(f"An error occurred for ID {self.id}: {e}")
            return None
        
        
        
    def search_taste_id(self, recipe_id_list):
        """
        Fetch taste information for a list of recipe IDs using the Spoonacular API.

        Parameters:
        - recipe_id_list (list): A list of recipe IDs.

        Returns:
        - pd.DataFrame: A DataFrame containing taste information for each recipe.
        """
        taste_compare = pd.DataFrame()
        headers = {
                'x-rapidapi-host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com',
                'x-rapidapi-key': self.api_key  } 
        for i in recipe_id_list:
            url = f'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{i}/tasteWidget.json'

            params = {'id': i,      
                      'normalize': 'False'
                         }    

            try:
                response = requests.get(url, params=params, headers=headers)
                response.raise_for_status()
                taste_response = response.json()
                df_taste = pd.DataFrame(taste_response, index=[i])
                taste_compare = pd.concat([taste_compare, df_taste], ignore_index=False)
            except Exception as e:
                    print(f"An error occurred for ID {i}: {e}")
        return taste_compare
    
    
    def search_nutrient_id(self, selection = 'info'):  
        """
        Fetch nutrition information for a recipe using the Spoonacular API.

        Parameters:
        - selection (str, optional): Type of nutrition information to retrieve. 
            - 'info': General information about nutrients, caloric breakdown, and weight per serving.
            - 'table': Detailed table of nutrient information.

        Returns:
        - pd.DataFrame: A DataFrame containing the requested nutrition information.
        """
        
        url = f'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{self.id}/nutritionWidget.json'
        params = {'id':  self.id    
                     }    
        headers = {
            'x-rapidapi-host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com',
            'x-rapidapi-key': self.api_key  } 
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            nutrition = response.json()
            keys_to_extract = ['nutrients', 'caloricBreakdown', 'weightPerServing']
            sub_nutr =  {key: nutrition[key] for key in keys_to_extract}

            if selection == 'table':
                nutr =  pd.DataFrame(sub_nutr['nutrients'])

            elif selection == 'info':
                nutr_total = pd.DataFrame(sub_nutr['caloricBreakdown'], index=['info']).T
                nutr_serving = pd.DataFrame(sub_nutr['weightPerServing'], index=['info']).T
                nutr = pd.concat([nutr_total, nutr_serving], ignore_index=False)

            else:
                raise ValueError("Invalid selection. Use 'table' or 'info'.")

        except Exception as e:
                print(f"An error occurred for ID {self.id }: {e}")
                return None
        return nutr

    
    
    def search_equipment_id(self):
        """
        Fetch equipment information for a recipe using the Spoonacular API.

        Returns:
        - pd.DataFrame or None: A DataFrame containing equipment information or None if an error occurs.
        """
        url = f'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{self.id}/equipmentWidget.json'
        params = {'id':self.id}
                       
        headers = {
            'x-rapidapi-host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com',
            'x-rapidapi-key': self.api_key } 
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            equipment = response.json()
            equip_df = pd.DataFrame(equipment)
            equip_df = pd.concat([equip_df, equip_df ['equipment'].apply(self.list_reader)], axis=1)
            equip_df= equip_df.drop(columns=['equipment','image'])

        except Exception as e:
                print(f"An error occurred for ID {self.id}: {e}")
                return None
        return equip_df

    
    def search_instruction_id(self):
        """
        Fetch analyzed instructions for a recipe using the Spoonacular API.

        Returns:
        - list or str: A list of instruction steps or an error message if no instructions are found or an error occurs.
        """
        url = f'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{self.id}/analyzedInstructions'
        params = {'id':self.id
                     }    
        headers = {
            'x-rapidapi-host': 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com',
            'x-rapidapi-key': self.api_key } 
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            if not response.json():
                return f"No instructions found for recipe with ID {self.id}"
            
            instruction_steps = response.json()[0].get('steps', [])
            return instruction_steps
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"
        
        
    def convert_instruction(self, list_in):
        """
        Convert and print a list of instruction steps.

        Parameters:
        - list_in (list): List of instruction steps.

        Returns:
        - None
        """
        step = list()
        length = len(list_in)
        for i in range(length):
            step_info = list_in[i]['step']
            step.append(step_info)
        print(f"Here are the steps to prepare recipe {self.id}:")
        for i, step in enumerate(step, start=1):
            print(f"{i}. {step}")
            print('')   
