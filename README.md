# Recipe Manager
This project consists of an application for obtaining the nutritional information (micronutrients, macronutrients, and phenols) of the ingredients in a recipe and calculating the total nutritional information. This has been achieved using translation models and fine-tuning of the BERT language model.

## Requeriments ##
* Python 3.10.2

https://www.python.org/downloads/release/python-3102/

* FastAPI
```python
pip install fastapi
```
* Requests
```python
pip install requests
```
* Transformers
```python
pip install transformers
```
* Beautiful Soup
```python
pip install beautifulsoup4
```
## Project Structure ##
* main.py: handles requests and acts as the server

* public: contains the webpage templates and the static (CSS) files that include the styles used for the design of the web pages.
  * static/css
    * style.css: CSS file with webpages styles.
  * templates
    * complete_nutritional_information.html: contains the structure of the interface when calculating the total nutritional information in the recipe.
    * nutritional_information.html: contains the structure of the interface when obtaining the nutritional information of an ingredient.
    * recipe_details.html: contains the structure of the interface when accessing recipe information.
    * recipe_manager.html: contains the structure of the main page interface.
    * recipes_list.html: contains the structure of the interface when accessing the list of existing recipes.

* recipe_processor: contains the Python files used to perform internal functions.
    * nutritional_data_handler.py: handles nutritional information and its retrieval through GET requests to the BEDCA and Phenol Explorer services.
    * Recipe.py: collects information about the recipes and the ingredients that compose them in order to facilitate their internal handling.
    * recipe_extractor.py: extracts and processes recipe ingredients and recipe steps. It makes use of the NER and translation models.
    * scrapper.py: extracts information from recipe web pages using the scraping method.
      
* recipes: contains processed recipes.
  * AllRecipes: contains the recipes obtained from All Recipes website.
    * cooklang_format_recipes: contains the Cooklang format recipes.
    * original_recipes: contains JSON format recipes.
  * RecetasGratis: contains the recipes obtained from Recetas Gratis website.
    * cooklang_format_recipes: contains the Cooklang format recipes.
    * original_recipes: contains JSON format recipes.

    
## How to use ##
To use the Recipe Manager, open a terminal at the path of the "main.py" file, which contains the code necessary to build the API. Once the necessary dependencies have been installed, type the following command:
```bash
uvicorn main:app --reload 
```
Then proceed to open a browser tab and enter the URL: http://127.0.0.1:8000/; this will take you to the root location (main page) of the web API.
