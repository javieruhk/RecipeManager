import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
import json


input_directory = "./input dbs/"
phenol_foods = input_directory + "foods.xls"
foodex2_file = input_directory + "MTX.xls"
phenol_composition_file = input_directory + "composition-data.xlsx"
BEDCA_file = input_directory + "bedca-2.1.csv"

output_directory = "./output json files/"
BEDCA_lemas_file = output_directory + "BEDCA lemas.json"
foodex2_lemas_file = output_directory + "foodex2 lemas.json"
BEDCA_foodex2_matches_file = output_directory + "BEDCA_foodex2 matches.json"


def create_foodex2_dict(foodex2_file):
	foodex2_data = pd.read_excel(foodex2_file, sheet_name="term")
	foodex2_df = pd.DataFrame(foodex2_data)		
	return dict(zip(foodex2_df['termCode'], foodex2_df['termExtendedName']))

def create_BEDCA_dict(BEDCA_file):
	BEDCA_data = pd.read_csv(BEDCA_file, sep=';', encoding='windows-1252') 
	BEDCA_df = pd.DataFrame(BEDCA_data)		
	return dict(zip(BEDCA_df['id'], BEDCA_df['nombre_inglés']))

def create_foodex2_facets_dict(foodex2_file):
	foodex2_data = pd.read_excel(foodex2_file, sheet_name="term")
	foodex2_df = pd.DataFrame(foodex2_data)	
	return dict(zip(foodex2_df['termCode'], foodex2_df['allFacets']))

class Foodex2_food(object):
	def __init__(self, part, ingredient, packaging_format, process):
		self.part = part 
		self.ingredient = ingredient 
		self.packaging_format = packaging_format 
		self.process = process

	def set_foodex2_part(self, part):
		self.part.append(part)

	def set_foodex2_ingredient(self, ingredient):
		self.ingredient.append(ingredient)

	def set_foodex2_packaging_format(self, packaging_format):
		self.packaging_format.append(packaging_format)

	def set_foodex2_process(self, process):
		self.process.append(process)

	def get_foodex2_part(self):
		return self.part

	def get_foodex2_ingredient(self):
		return self.ingredient

	def get_foodex2_packaging_format(self):
		return self.packaging_format

	def get_foodex2_process(self):
		return self.process

def lemmatize_food_name(lemmatizer, stopwords, extended_food_name):
	extended_food_name_tagged = nltk.pos_tag(nltk.regexp_tokenize(extended_food_name, pattern=r"\s|[\.,;'(/)-]", gaps=True))
	extended_food_name_lemas = []
	
	for (word, tag) in extended_food_name_tagged:
		if word not in stopwords:
			if(tag.startswith('J')):
				lema = lemmatizer.lemmatize(word, wordnet.ADJ)
				extended_food_name_lemas.append(lema.lower())
			elif tag.startswith('V'):
				lema = lemmatizer.lemmatize(word, wordnet.VERB)
				extended_food_name_lemas.append(lema.lower())
			elif tag.startswith('N'):
				lema = lemmatizer.lemmatize(word, wordnet.NOUN)
				extended_food_name_lemas.append(lema.lower())
			elif tag.startswith('R'):
				lema = lemmatizer.lemmatize(word, wordnet.ADV)        
				extended_food_name_lemas.append(lema.lower())
			else:
				lema = lemmatizer.lemmatize(word)
				extended_food_name_lemas.append(lema.lower())
	
	return extended_food_name_lemas

def lemmatize_foodex2_dict(stopwords, foodex2_dict):
	stopwords = set(stopwords.words('english'))
	lemmatizer = WordNetLemmatizer()
	lemmatized_dict = {}

	for foodex2_code in foodex2_dict:
		extended_food_name = foodex2_dict[foodex2_code]
		#extended_food_name_tagged = nltk.pos_tag(word_tokenize(extended_food_name))
		#print(extended_food_name_tagged)
		extended_food_name_lemas = lemmatize_food_name(lemmatizer, stopwords, extended_food_name)
		lemmatized_dict[foodex2_code] = extended_food_name_lemas
	
	#print(lemmatized_dict)
	return lemmatized_dict

def lemmatize_BEDCA_dict(stopwords, BEDCA_dict):
	stopwords = set(stopwords.words('english'))
	lemmatizer = WordNetLemmatizer()
	lemmatized_dict = {}

	#[[oat, grain], [roll], [red]]
	for BEDCA_code in BEDCA_dict:
		extended_food_name = BEDCA_dict[BEDCA_code]
		extended_food_modifiers = extended_food_name.split(", ")
		extended_food_lemas = []

		for modifier in extended_food_modifiers:
			modifier_lemas = lemmatize_food_name(lemmatizer, stopwords, modifier)
			extended_food_lemas.append(modifier_lemas)
			
		lemmatized_dict[BEDCA_code] = extended_food_lemas
	
	#print(lemmatized_dict)
	return lemmatized_dict

def create_json(lemmatized_dict, file_name):
	#result = json.dumps(lemmatized_dict, indent = 4)
	#print(result)
	with open(file_name, "w") as outfile:
	    json.dump(lemmatized_dict, outfile, indent = 4)

def create_BEDCA_foodex2_matches_dict(BEDCA_food_ingredients_list, lemmatized_foodex2_dict):
	BEDCA_foodex2_matches_dict = {}
	BEDCA_foodex2_matches_code_list = [] 
	most_matches_n = 0

	for foodex2_code in lemmatized_foodex2_dict:
		matches_n = 0
		
		for ingredient_to_match in BEDCA_food_ingredients_list[0]:
			if ingredient_to_match in lemmatized_foodex2_dict[foodex2_code]:
				matches_n = matches_n+1
		
		if matches_n > most_matches_n:
			most_matches_n = matches_n
			BEDCA_foodex2_matches_code_list = [foodex2_code]
		elif matches_n == most_matches_n:
			BEDCA_foodex2_matches_code_list.append(foodex2_code)

	for foodex2_code in BEDCA_foodex2_matches_code_list:
		BEDCA_foodex2_matches_dict[foodex2_code] = lemmatized_foodex2_dict[foodex2_code]

	#print(BEDCA_foodex2_matches_dict)
	return BEDCA_foodex2_matches_dict

def update_BEDCA_foodex2_matches_dict(BEDCA_food_ingredients_list, BEDCA_foodex2_matches_dict):
	most_BEDCA_foodex2_matches_dict = {}
	most_BEDCA_foodex2_matches_code_list = [] 
	most_matches_n = 0

	for foodex2_code in BEDCA_foodex2_matches_dict:
		matches_n = 0
		
		for modifier_n in range(1, len(BEDCA_food_ingredients_list)):#ver si poner a partir de la coma todos en una lista
			for modifier_to_match in BEDCA_food_ingredients_list[modifier_n]:
				if modifier_to_match in BEDCA_foodex2_matches_dict[foodex2_code]:
					matches_n = matches_n+1
		
		if matches_n > most_matches_n:
			most_matches_n = matches_n
			most_BEDCA_foodex2_matches_code_list = [foodex2_code]
		elif matches_n == most_matches_n:
			most_BEDCA_foodex2_matches_code_list.append(foodex2_code)

	for foodex2_code in most_BEDCA_foodex2_matches_code_list:
		most_BEDCA_foodex2_matches_dict[foodex2_code] = BEDCA_foodex2_matches_dict[foodex2_code]

	#print(most_BEDCA_foodex2_matches_dict)
	return most_BEDCA_foodex2_matches_dict

def create_foodex2_object_dict(foodex2_facets_dict, BEDCA_foodex2_matches_dict):
	foodex2_dict_facets = {}
	for foodex2_code in BEDCA_foodex2_matches_dict:
		allfacets = foodex2_facets_dict[foodex2_code].split("#")
		
		if len(allfacets) > 1:
			facets = allfacets[1].split("$")
			foodex2_food = Foodex2_food([], [], [], [])
			
			for facet in range(0, len(facets)):
				foodex2_facet_codes = facets[facet].split(".")
				
				if foodex2_facet_codes[0] == "F02":
					foodex2_food.set_foodex2_part(foodex2_dict[foodex2_facet_codes[1]])
				if foodex2_facet_codes[0] == "F04":
					foodex2_food.set_foodex2_ingredient(foodex2_dict[foodex2_facet_codes[1]])
				if foodex2_facet_codes[0] == "F18":
					foodex2_food.set_foodex2_packaging_format(foodex2_dict[foodex2_facet_codes[1]])
				if foodex2_facet_codes[0] == "F28":
					foodex2_food.set_foodex2_process(foodex2_dict[foodex2_facet_codes[1]])

				foodex2_dict_facets[foodex2_code] = foodex2_food

	return foodex2_dict_facets

def select_foodex2_entry(foodex2_object_dict, foodex2_dict):
	for foodex2_object in foodex2_object_dict:
		part_facet = foodex2_object_dict[foodex2_object].get_foodex2_part()
		ingredient_facet = foodex2_object_dict[foodex2_object].get_foodex2_ingredient()
		packaging_format_facet = foodex2_object_dict[foodex2_object].get_foodex2_packaging_format()
		process_facet = foodex2_object_dict[foodex2_object].get_foodex2_process()
		print("(" + foodex2_object + ") " + foodex2_dict[foodex2_object])
		print("part: " + str(part_facet))
		print("ingredient: " + str(ingredient_facet))
		print("packaging_format: " + str(packaging_format_facet))
		print("process: " + str(process_facet) + "\n")

	foodex2_code_selected = input("Introduce the foodex2 code of the food selected: ")

	if foodex2_code_selected in foodex2_object_dict:
		part_facet = foodex2_object_dict[foodex2_code_selected].get_foodex2_part()
		ingredient_facet = foodex2_object_dict[foodex2_code_selected].get_foodex2_ingredient()
		packaging_format_facet = foodex2_object_dict[foodex2_code_selected].get_foodex2_packaging_format()
		process_facet = foodex2_object_dict[foodex2_code_selected].get_foodex2_process()
		print("\n(" + foodex2_code_selected + ") " + foodex2_dict[foodex2_code_selected])
		print("part: " + str(part_facet))
		print("ingredient: " + str(ingredient_facet))
		print("packaging_format: " + str(packaging_format_facet))
		print("process: " + str(process_facet) + "\n")


foodex2_dict = create_foodex2_dict(foodex2_file)
lemmatized_foodex2_dict = lemmatize_foodex2_dict(stopwords, foodex2_dict)
create_json(lemmatized_foodex2_dict, foodex2_lemas_file)

BEDCA_dict = create_BEDCA_dict(BEDCA_file)
lemmatized_BEDCA_dict = lemmatize_BEDCA_dict(stopwords, BEDCA_dict)
create_json(lemmatized_BEDCA_dict, BEDCA_lemas_file)

BEDCA_food_ingredients_list = lemmatized_BEDCA_dict.keys()
BEDCA_foodex2_matches_dict = create_BEDCA_foodex2_matches_dict(lemmatized_BEDCA_dict[list(BEDCA_food_ingredients_list)[0]], lemmatized_foodex2_dict)
BEDCA_foodex2_matches_dict = update_BEDCA_foodex2_matches_dict(lemmatized_BEDCA_dict[list(BEDCA_food_ingredients_list)[0]], BEDCA_foodex2_matches_dict)


foodex2_facets_dict = create_foodex2_facets_dict(foodex2_file)
foodex2_object_dict = create_foodex2_object_dict(foodex2_facets_dict, BEDCA_foodex2_matches_dict)
select_foodex2_entry(foodex2_object_dict, foodex2_dict)

"""
BEDCA_all_foodex2_matches_dict = {}
for BEDCA_food_ingredients_list in lemmatized_BEDCA_dict:
	BEDCA_foodex2_matches_dict = create_BEDCA_foodex2_matches_dict(lemmatized_BEDCA_dict[BEDCA_food_ingredients_list], lemmatized_foodex2_dict)
	BEDCA_foodex2_matches_dict = update_BEDCA_foodex2_matches_dict(lemmatized_BEDCA_dict[BEDCA_food_ingredients_list], BEDCA_foodex2_matches_dict)
	BEDCA_all_foodex2_matches_dict[BEDCA_food_ingredients_list] = BEDCA_foodex2_matches_dict
create_json(BEDCA_all_foodex2_matches_dict, BEDCA_foodex2_matches_file)

"""
