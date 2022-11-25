import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import json


input_directory = "./input dbs/"
phenol_foods_file = input_directory + "foods.xls"
phenol_composition_data_file = input_directory + "composition-data.xlsx"
foodex2_file = input_directory + "MTX.xls"

output_directory = "./output json files/"
foodex2_phenol_explorer_matches_file = output_directory + "foodex2_phenol_explorer matches.json"

def create_phenol_explorer_foods_scientific_names_dict(phenol_explorer_file):
	phenol_explorer_data = pd.read_excel(phenol_explorer_file, sheet_name="Phenol-Explorer Foods")
	phenol_explorer_df = pd.DataFrame(phenol_explorer_data)		
	return dict(zip(phenol_explorer_df['Name'], phenol_explorer_df['Scientific Name']))

def create_phenol_explorer_foods_names_dict(phenol_explorer_file):
	phenol_explorer_data = pd.read_excel(phenol_explorer_file, sheet_name="Phenol-Explorer Foods")
	phenol_explorer_df = pd.DataFrame(phenol_explorer_data)		
	return dict(zip(phenol_explorer_df['ID'], phenol_explorer_df['Name']))

def create_foodex2_scientific_names_dict(foodex2_file):
	foodex2_data = pd.read_excel(foodex2_file, sheet_name="term")
	foodex2_df = pd.DataFrame(foodex2_data)		
	return dict(zip(foodex2_df['termCode'], foodex2_df['scientificNames']))

def process_foodex2_scientific_names(foodex2_dict):
	foodex2_dict_processed = {}
	for entry in foodex2_dict:
		scientific_name = foodex2_dict[entry]
		scientific_name_filtered = ""
		if isinstance(scientific_name, str):
			main_scientific_name = scientific_name.split("$")
			scientific_name_splitted = main_scientific_name[0].split(" ")
	
			if scientific_name_splitted[0].islower():
				scientific_name_mayus_list = []
				copy_flag = False
				for pos in range(0, len(scientific_name_splitted)):
					word = scientific_name_splitted[pos]
					first_letter = word[0]
					if first_letter.isupper():
						copy_flag = True
					if copy_flag:
						scientific_name_mayus_list.append(word)
				scientific_name_splitted = scientific_name_mayus_list
	
			scientific_name_filtered_list = []
			copy_flag = False
			for pos in range(0, len(scientific_name_splitted)):
				word = scientific_name_splitted[pos]
				
				if word != "":
					if  "." not in word and "(" not in word and (pos == 0 or (pos != 0 and word.islower())):
						scientific_name_filtered_list.append(word)
					else:
						break
			scientific_name_filtered = " ".join(scientific_name_filtered_list)
			foodex2_dict_processed[entry] = scientific_name_filtered
	return foodex2_dict_processed


def create_scientific_names_matches_list(foodex2_scientific_name, phenol_explorer_food_dict):
	scientific_names_matches_list = []
	for phenol_explorer_entry in phenol_explorer_food_dict:
		if foodex2_scientific_name in str(phenol_explorer_food_dict[phenol_explorer_entry]):
			scientific_names_matches_list.append(phenol_explorer_entry)
			print(phenol_explorer_entry + " => " + phenol_explorer_food_dict[phenol_explorer_entry])
	return scientific_names_matches_list


"""

foodex2_scientific_names_dict = create_foodex2_scientific_names_dict(foodex2_file)
foodex2_dict_processed = process_foodex2_scientific_names(foodex2_scientific_names_dict)

##casos de ejemplo que tienen coincidencias
#foodex2_scientific_name = foodex2_dict_processed[list(foodex2_dict_processed.keys())[6]]
#foodex2_scientific_name = foodex2_dict_processed[list(foodex2_dict_processed.keys())[8]]
#foodex2_scientific_name = foodex2_dict_processed[list(foodex2_dict_processed.keys())[9]]
#foodex2_scientific_name = foodex2_dict_processed[list(foodex2_dict_processed.keys())[12]]
#foodex2_scientific_name = foodex2_dict_processed[list(foodex2_dict_processed.keys())[145]]
#foodex2_scientific_name = foodex2_dict_processed[list(foodex2_dict_processed.keys())[503]]
#foodex2_scientific_name = foodex2_dict_processed["A000T"]
#foodex2_scientific_name = foodex2_dict_processed["A000J"] #no tiene nombre científico

foodex2_code = "A000T"
foodex2_scientific_name = ""
if foodex2_code in foodex2_dict_processed:
	foodex2_scientific_name = foodex2_dict_processed[foodex2_code]

phenol_explorer_food_dict = create_phenol_explorer_foods_scientific_names_dict(phenol_foods_file)

scientific_names_matches_list = create_scientific_names_matches_list(foodex2_scientific_name, phenol_explorer_food_dict)

print(scientific_names_matches_list)


##imprimir los nombres cientificos procesados numerados
#num = 0
#for entry in foodex2_dict_processed:
#	print(str(num) + " => " + entry + " => " + foodex2_dict_processed[entry])
#	num = num + 1 

"""

phenol_explorer_foods_names_dict = create_phenol_explorer_foods_names_dict(phenol_foods_file)
print(phenol_explorer_foods_names_dict)

word_list = ["raw", "fresh", "peeled", "whole", "dehulled", "dried"]

phenol_explorer_foods_names_dict_processed = {}
for phenol_explorer_code in phenol_explorer_foods_names_dict:
	food_name = phenol_explorer_foods_names_dict[phenol_explorer_code]
#	print(food_name)
	splitted_name_by_commas = food_name.split(", ")
#	print(splitted_name_by_commas)

	ordered_name_list = []
	for modifier in splitted_name_by_commas:
		if "[" in modifier and "]" in modifier:
			start = modifier.index('[')
			end = modifier.index(']')
			first_words = modifier[:start-1]
			last_words = modifier[start+1:end]
			modifier = last_words + " " + first_words

		splitted_name_by_spaces = modifier.split(" ")
		for word in splitted_name_by_spaces:
			if word not in word_list:
				ordered_name_list.append(word)

	ordered_name = " ".join(ordered_name_list)
	phenol_explorer_foods_names_dict_processed[phenol_explorer_code] = ordered_name


print(phenol_explorer_foods_names_dict_processed)

