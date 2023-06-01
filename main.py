from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import json
from recipe_processor import nutritional_data_handler as ndh

app = FastAPI()

app.mount("/static", StaticFiles(directory="./public/static"), name="static")

templates = Jinja2Templates(directory="./public/templates")

#uvicorn main:app --reload
#http://127.0.0.1:8000/

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
	return templates.TemplateResponse("recipe_manager.html", {"request": request})

@app.get("/rg-recipes", response_class=HTMLResponse)
async def read_files(request: Request):
	path = "./recipes/RecetasGratis/original_recipes"
	recipe_file_names = os.listdir(path)
	recipe_names = []
	for recipe_file_name in recipe_file_names:
		recipe_name = recipe_file_name.replace(".json", "")
		recipe_names.append(recipe_name)
	return templates.TemplateResponse("recipes_list.html", {"request": request, "recipe_names": recipe_names, "recipe_file_names": recipe_file_names, "recipe_type": "RG"})

@app.get("/rg-recipes/{recipe_name}", response_class=HTMLResponse)
async def read_file(recipe_name: str, request: Request):
	path = f"./recipes/RecetasGratis/original_recipes/{recipe_name}"
	with open(path, "r") as f:
		recipe_text = json.load(f)

	recipe_cooklang_file_name = recipe_name.replace("json", "cook")
	recipe_title = recipe_name.replace("_", " ").replace(".json", "")
	recipe_direction = "/rg-recipes/" + recipe_name

	return templates.TemplateResponse("recipe_details.html", {"request": request, "recipe_title": recipe_title, "recipe_text": recipe_text, "recipe_type": "RG", "recipe_file_name":recipe_cooklang_file_name, "recipe_direction": recipe_direction})

@app.get("/ar-recipes", response_class=HTMLResponse)
async def read_files(request: Request):
	path = "./recipes/AllRecipes/original_recipes"
	recipe_file_names = os.listdir(path)
	recipe_names = []
	for recipe_file_name in recipe_file_names:
		recipe_name = recipe_file_name.replace(".json", "")
		recipe_names.append(recipe_name)
	return templates.TemplateResponse("recipes_list.html", {"request": request, "recipe_names": recipe_names, "recipe_file_names": recipe_file_names, "recipe_type": "AR"})

@app.get("/ar-recipes/{recipe_name}", response_class=HTMLResponse)
async def read_file(recipe_name: str, request: Request):
	path = f"./recipes/AllRecipes/original_recipes/{recipe_name}"
	with open(path, "r") as f:
		recipe_text = json.load(f)

	recipe_cooklang_file_name = recipe_name.replace("json", "cook")
	recipe_title = recipe_name.replace("_", " ").replace(".json", "")

	recipe_direction = "/ar-recipes/" + recipe_name
	
	return templates.TemplateResponse("recipe_details.html", {"request": request, "recipe_title": recipe_title, "recipe_text": recipe_text, "recipe_type": "AR", "recipe_file_name":recipe_cooklang_file_name, "recipe_direction": recipe_direction})

@app.get("/food-information", response_class=HTMLResponse)
async def get_food_information(request: Request, ingredient: str, recipe_direction: str):
	ingredient_dict = json.loads(ingredient)

	food = ingredient_dict["food"]
	food_spanish = ingredient_dict["food_spanish"]
	quantity =ingredient_dict["quantity"]
	unit = ingredient_dict["unit_spanish"]
	print(food)
	print(unit)
	print(quantity)

	BEDCA_response = ndh.get_food_nutritional_information(food, "BEDCA")
	phenol_explorer_response = ndh.get_food_nutritional_information(food, "phenol_explorer")
	print(BEDCA_response)
	print(phenol_explorer_response)

	return templates.TemplateResponse("nutritional_information.html", {"request": request, "food_name": food_spanish, "quantity": quantity, "unit": unit, "BEDCA_response": BEDCA_response, "phenol_explorer_response": phenol_explorer_response, "recipe_direction": recipe_direction})

@app.get("/complete-nutritional-info", response_class=HTMLResponse)
async def get_complete_nutritional_information(request: Request, ingredient_list: str, recipe_direction: str, recipe_title: str):
	ingredient_list_json = json.loads(ingredient_list)

	nutritional_information_dict = ndh.get_complete_food_nutritional_information(ingredient_list_json)

	return templates.TemplateResponse("complete_nutritional_information.html", {"request": request, "recipe_title":recipe_title, "nutritional_information_dict": nutritional_information_dict, "recipe_direction": recipe_direction})

@app.get("/download-cooklang-file")
async def download_cooklang_file(filename: str, recipe_type: str):
	file_path = ""
	if recipe_type == "RG":
		file_path = f"./recipes/RecetasGratis/cooklang_format_recipes/{filename}"
	elif recipe_type == "AR":
		file_path = f"./recipes/AllRecipes/cooklang_format_recipes/{filename}"
	return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
