from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForSeq2SeqLM, pipeline
import re
import json
import Recipe
import scrapper

extractor_pretrained = "davanstrien/deberta-v3-base_fine_tuned_food_ner"#---
extractor_tokenizer = AutoTokenizer.from_pretrained(extractor_pretrained, model_max_length=1320)
extractor_model = AutoModelForTokenClassification.from_pretrained(extractor_pretrained)
extractor_pipe = pipeline("ner", model=extractor_model, tokenizer=extractor_tokenizer)

translator_pretrained = "Helsinki-NLP/opus-mt-es-en"
translator_tokenizer = AutoTokenizer.from_pretrained(translator_pretrained)
translator_model = AutoModelForSeq2SeqLM.from_pretrained(translator_pretrained)
translator_english_pipe = pipeline("translation", model=translator_model, tokenizer=translator_tokenizer)

translator_pretrained = "Helsinki-NLP/opus-mt-en-es"
translator_tokenizer = AutoTokenizer.from_pretrained(translator_pretrained)
translator_model = AutoModelForSeq2SeqLM.from_pretrained(translator_pretrained)
translator_spanish_pipe = pipeline("translation", model=translator_model, tokenizer=translator_tokenizer)


def process_ingredient(ingredients):
	new_ingredients = []
	for ingredient in ingredients:
		inside_parenthesis = False
		if ":" not in ingredient:
			new_ingredient = ""
			words = ingredient.split()
			
			for word in words:
				if "(" in word:
					inside_parenthesis = True
				elif ")" in word:
					inside_parenthesis = False
				elif not inside_parenthesis:
					new_ingredient += word + " "
			new_ingredients.append(new_ingredient.strip())
	return new_ingredients

def print_table(data):
	# Define the column headers
	headers = ["entity", "score", "index", "word", "start", "end"]
	# Define the width of each column
	col_width = [len(headers[i]) for i in range(len(headers))]
	for item in data:
		for i in range(len(headers)):
			# Find the width of the value in the current column
			value_width = len(str(item[headers[i]]))
			# If the width is greater than the column width, update the column width
			if value_width > col_width[i]:
				col_width[i] = value_width
	# Print the column headers
	for i in range(len(headers)):
		print(headers[i].ljust(col_width[i]), end="  ")
	print()
	# Print a separator row
	separator = "-" * sum(col_width) + "  " * (len(headers) - 1)
	print(separator)
	# Print the data rows
	for item in data:
		for i in range(len(headers)):
			print(str(item[headers[i]]).ljust(col_width[i]), end="  ")
		print()

def supr_wrong_entries(ner_entity_ingredients):
	for entry in ner_entity_ingredients:
		if entry["word"] == "s":
			ner_entity_ingredients.remove(entry)
	return ner_entity_ingredients

def create_ingredient_object_list(ner_entity_ingredient_list):
	ingredient_object_list = []
	food = None

	for ner_entity_ingredient in ner_entity_ingredient_list:
		ingredient = Recipe.Ingredient(None, None, None, None, None)
		for entry_n in range(len(ner_entity_ingredient)):
			entity = ner_entity_ingredient[entry_n]["entity"]
			word = ner_entity_ingredient[entry_n]["word"].replace("▁","")
		
			if entity == "U-QUANTITY":
				ingredient.set_quantity(word)
		
			if entity == "U-UNIT":
				ingredient.set_unit(word)
			
			if entity == "U-PROCESS":
				ingredient.set_process(word)
		
			if entity == "U-PHYSICAL_QUALITY":
				ingredient.set_physical_quality(word)
			
			if entity == "U-FOOD":
				if ingredient.get_food() == None:
					ingredient.set_food(word)
		
			if entity == "B-FOOD":
				if ingredient.get_food() == None:
					food = word + " "
		
			if entity == "I-FOOD" and food != None:
				if ingredient.get_food() == None:
					food += word + " "
		
			if entity == "L-FOOD":
				if ingredient.get_food() == None: 
					if food == None:
						food = word
					else:
						food += word
					ingredient.set_food(food)
					food = None
			
		ingredient_object_list.append(ingredient)
	
	return ingredient_object_list

def create_RG_ner_entity_ingredients_list(ingredients_section):
	ingredients_processed =  process_ingredient(ingredients_section)
	ner_entity_ingredients_processed_list = []

	for ingredient in ingredients_processed:
		translation = translator_english_pipe(ingredient)
		ner_entity_ingredients = extractor_pipe(translation[0]["translation_text"])
		ner_entity_ingredients_processed = supr_wrong_entries(ner_entity_ingredients)
		#print_table(ner_entity_ingredients_processed)
		ner_entity_ingredients_processed_list.append(ner_entity_ingredients_processed)
	
	return ner_entity_ingredients_processed_list

def create_AR_ner_entity_ingredients_list(ingredients_section):
	ingredients_processed =  process_ingredient(ingredients_section)
	ner_entity_ingredients_processed_list = []

	for ingredient in ingredients_processed:
		ner_entity_ingredients = extractor_pipe(ingredient)
		ner_entity_ingredients_processed = supr_wrong_entries(ner_entity_ingredients)
		#print_table(ner_entity_ingredients_processed)
		ner_entity_ingredients_processed_list.append(ner_entity_ingredients_processed)
	
	return ner_entity_ingredients_processed_list

def traduce_step_list(step_list, language):
	steps_traduced = []
	if language == "TO_EN":
		for step in step_list:
			step_traduced = translator_english_pipe(step)
			steps_traduced.append(step_traduced[0]["translation_text"])
	elif language == "TO_ES":
		for step in step_list:
			step_traduced = translator_spanish_pipe(step)
			steps_traduced.append(step_traduced[0]["translation_text"])
	return steps_traduced

def create_cooklang_format_steps(step_list, ingredient_object_list):
	cooklang_step_list = step_list
	for step_n in range(len(step_list)):
		for ingredient in ingredient_object_list:
			step = cooklang_step_list[step_n]
			food_name = ingredient.get_food()
	
			if food_name != None and re.search(r"\b" + food_name + r"\b", step):
				unit = ingredient.get_unit()
				if unit == None:
					unit = ""
				new_food_name = "@%s{%s%%%s}" %(food_name.strip(), ingredient.get_quantity(), unit)
				new_step = step.replace(food_name, new_food_name)
				cooklang_step_list[step_n] = new_step

	cooklang_steps = '\n\n'.join(cooklang_step_list)

	return cooklang_steps

def traduce_to_spanish(text):
	if text:
		step_traduced = translator_spanish_pipe(text)
		traduced = step_traduced[0]["translation_text"]
	else:
		traduced = text
	return traduced



def create_recipes(recipe_web):
	link_list = []


	if recipe_web == "RG":
		link_list = scrapper.get_RG_recipes_links()
	if recipe_web == "AR":
		link_list = scrapper.get_AR_recipes_links()

	recipe_n = 1
	for link in link_list:
		page = scrapper.requests.get(link)
		soup = scrapper.BeautifulSoup(page.content, 'html.parser')

		ingredient_list = []
		ner_entity_ingredients_list = []
		ingredient_object_list = []
		step_list = []
		step_list_traduced = []
		file_name_recipe = ""
		file_name_cooklang_recipe = ""
		recipe_name = ""


		#---
		if recipe_web == "RG":
			recipe_name = scrapper.get_RG_recipe_name(soup)			 

			ingredient_list = scrapper.get_RG_ingredient_list(soup)
		
			ner_entity_ingredients_list = create_RG_ner_entity_ingredients_list(ingredient_list)


			ingredient_object_list = create_ingredient_object_list(ner_entity_ingredients_list)
	
			step_list = scrapper.get_RG_step_list(soup)

			step_list_traduced = traduce_step_list(step_list, "TO_EN")
	
			file_name_recipe = "U:/TFG/Recipe Manager/recipes/RecetasGratis/original_recipes/%s.json" % (recipe_name) 
			file_name_cooklang_recipe = "U:/TFG/Recipe Manager/recipes/RecetasGratis/cooklang_format_recipes/%s.cook" % (recipe_name) 

		if recipe_web == "AR":
			recipe_name = scrapper.get_AR_recipe_name(soup)

			recipe_name_traduced = traduce_to_spanish(recipe_name)

			recipe_name_formatted = recipe_name_traduced.replace(" ", "_")

			ingredient_list = scrapper.get_AR_ingredient_list(soup)
		
			ner_entity_ingredients_list = create_AR_ner_entity_ingredients_list(ingredient_list)
			
			ingredient_object_list = create_ingredient_object_list(ner_entity_ingredients_list)

			step_list_traduced = scrapper.get_AR_step_list(soup)

			step_list = traduce_step_list(step_list_traduced, "TO_ES")
		
			file_name_recipe = "U:/TFG/Recipe Manager/recipes/AllRecipes/original_recipes/%s.json" % (recipe_name_formatted) 
			file_name_cooklang_recipe = "U:/TFG/Recipe Manager/recipes/AllRecipes/cooklang_format_recipes/%s.cook" % (recipe_name_formatted) 
		#---

		ingredients_dict_format_list = []
		for ingredient in ingredient_object_list:
			food_spanish = traduce_to_spanish(ingredient.get_food())
			unit_spanish = traduce_to_spanish(ingredient.get_unit())
			physical_quality_spanish = traduce_to_spanish(ingredient.get_physical_quality())
			process_spanish = traduce_to_spanish(ingredient.get_process())

			ingredients_dict_format = {"food_spanish": food_spanish, "food": ingredient.get_food(), "quantity": ingredient.get_quantity(), "unit_spanish": unit_spanish, "unit": ingredient.get_unit(), "physical_quality_spanish": physical_quality_spanish, "physical_quality": ingredient.get_physical_quality(), "process_spanish": process_spanish, "process": ingredient.get_process()}
			ingredients_dict_format_list.append(ingredients_dict_format)

		recipe_dict = {"ingredients": ingredients_dict_format_list, "steps": step_list}


		with open(file_name_recipe, "w", encoding='utf-8') as outfile:
			json.dump(recipe_dict, outfile, indent = 4)
			outfile.close()
		
		recipe = Recipe.Recipe(ingredient_object_list, step_list_traduced)
		
		print(file_name_cooklang_recipe)
		print(step_list_traduced)
		for ingredient in ingredient_object_list:
			print(ingredient)
		cooklang_steps = create_cooklang_format_steps(step_list_traduced, ingredient_object_list)
		
		
		with open(file_name_cooklang_recipe, "w", encoding='utf-8') as outfile:
			outfile.write(cooklang_steps)
			outfile.close()

		recipe_n += 1


if __name__ == '__main__':
	#create_recipes("RG")
	create_recipes("AR")