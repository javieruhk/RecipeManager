import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import json


input_directory = "./input dbs/"
phenol_foods_file = input_directory + "foods.xls"
phenol_composition_data_file = input_directory + "composition-data.xlsx"

output_directory = "./output json files/"
foodex2_phenol_explorer_matches_file = output_directory + "foodex2_phenol_explorer matches.json"


def create_phenol_explorer_composition_data_list(phenol_explorer_file):
	phenol_info_data = pd.read_excel(phenol_explorer_file, sheet_name="Sheet1")
	phenol_info_df = pd.DataFrame(phenol_info_data)
	#return dict(zip(phenol_info_df['food'], (phenol_info_df['compound_group'], phenol_info_df['compound_sub_group'])))
	phenol_explorer_composition_data_list = list(zip(phenol_info_df['food'], phenol_info_df['compound_group'], phenol_info_df['compound_sub_group'], phenol_info_df['mean']))
	return phenol_explorer_composition_data_list

def create_phenol_explorer_food_dict(phenol_explorer_file):
	phenol_explorer_data = pd.read_excel(phenol_explorer_file, sheet_name="Phenol-Explorer Foods")
	phenol_explorer_df = pd.DataFrame(phenol_explorer_data)		
	return dict(zip(phenol_explorer_df['Name'], phenol_explorer_df['Scientific Name']))

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

def lemmatize_phenol_explorer_food_dict(stopwords, phenol_explorer_food_dict):
	stopwords = set(stopwords.words('english'))
	lemmatizer = WordNetLemmatizer()
	lemmatized_dict = {}

	for phenol_explorer_food_name in phenol_explorer_food_dict:
		scientific_food_name = phenol_explorer_food_dict[phenol_explorer_food_name]
		#tiene nombre científico en foods
		if isinstance(scientific_food_name, str):
			scientific_food_name_lemas = lemmatize_food_name(lemmatizer, stopwords, scientific_food_name)
			lemmatized_dict[phenol_explorer_food_name] = scientific_food_name_lemas
		#else
		#no tiene nombre científico en foods (ver otro método para buscarlo)
	
	#print(lemmatized_dict)
	return lemmatized_dict

def update_foodex2_phenol_explorer_food_matches_dict(scientific_food_lemas_list, lemmatized_phenol_explorer_food_dict):
	foodex2_phenol_explorer_food_matches_dict = {}
	foodex2_phenol_explorer_food_matches_name_list = [] 
	most_matches_n = 0

	for phenol_explorer_food_name in lemmatized_phenol_explorer_food_dict:
		matches_n = 0
		
		for modifier_n in range(0, len(scientific_food_lemas_list)):#ver si poner a partir de la coma todos en una lista
			if scientific_food_lemas_list[modifier_n] in lemmatized_phenol_explorer_food_dict[phenol_explorer_food_name]:
				matches_n = matches_n+1
		
		if matches_n > most_matches_n:
			most_matches_n = matches_n
			foodex2_phenol_explorer_food_matches_name_list = [phenol_explorer_food_name]
		elif matches_n == most_matches_n:
			foodex2_phenol_explorer_food_matches_name_list.append(phenol_explorer_food_name)

	if most_matches_n > 0:
		for phenol_explorer_food_name in foodex2_phenol_explorer_food_matches_name_list:
			foodex2_phenol_explorer_food_matches_dict[phenol_explorer_food_name] = lemmatized_phenol_explorer_food_dict[phenol_explorer_food_name]

	#print(most_BEDCA_foodex2_matches_dict)
	return foodex2_phenol_explorer_food_matches_dict

def create_composition_data_dict(foodex2_phenol_explorer_food_matches_dict, phenol_explorer_composition_data_list):
	phenol_explorer_food_dict = {}
	for foodex2_phenol_explorer_food_match in foodex2_phenol_explorer_food_matches_dict:
		
		for phenol_explorer_composition_data_elem in range(0, len(phenol_explorer_composition_data_list)):
			compound_name = phenol_explorer_composition_data_list[phenol_explorer_composition_data_elem][0]
			if foodex2_phenol_explorer_food_match == compound_name:
				compound_mean = phenol_explorer_composition_data_list[phenol_explorer_composition_data_elem][3]
				compound_group = phenol_explorer_composition_data_list[phenol_explorer_composition_data_elem][1]
				if compound_group == 'Flavonoids':
					compound_sub_group = phenol_explorer_composition_data_list[phenol_explorer_composition_data_elem][2]
					if foodex2_phenol_explorer_food_match in phenol_explorer_food_dict.keys():
						if compound_group in phenol_explorer_food_dict[foodex2_phenol_explorer_food_match].keys():
							if compound_sub_group in phenol_explorer_food_dict[foodex2_phenol_explorer_food_match][compound_group].keys():
								phenol_explorer_food_dict[foodex2_phenol_explorer_food_match][compound_group][compound_sub_group] = phenol_explorer_food_dict[foodex2_phenol_explorer_food_match][compound_group][compound_sub_group] + compound_mean
							else:
								phenol_explorer_food_dict[foodex2_phenol_explorer_food_match][compound_group][compound_sub_group] = compound_mean
						else:
							compound_sub_group_dict = {}
							compound_sub_group_dict[compound_sub_group] = compound_mean
							phenol_explorer_food_dict[foodex2_phenol_explorer_food_match][compound_group] = compound_sub_group_dict
					else:
						compound_group_dict = {}
						compound_sub_group_dict = {}
						compound_sub_group_dict[compound_sub_group] = compound_mean
						compound_group_dict[compound_group] = compound_sub_group_dict
						phenol_explorer_food_dict[foodex2_phenol_explorer_food_match] = compound_group_dict
	
				else:
					if foodex2_phenol_explorer_food_match in phenol_explorer_food_dict.keys():
						if compound_group in phenol_explorer_food_dict[foodex2_phenol_explorer_food_match].keys():
							phenol_explorer_food_dict[foodex2_phenol_explorer_food_match][compound_group] = phenol_explorer_food_dict[foodex2_phenol_explorer_food_match][compound_group] + compound_mean
						else:
							phenol_explorer_food_dict[foodex2_phenol_explorer_food_match][compound_group] = compound_mean
					else:
						compound_group_dict = {}
						compound_group_dict[compound_group] = compound_mean
						phenol_explorer_food_dict[foodex2_phenol_explorer_food_match] = compound_group_dict
	return phenol_explorer_food_dict

def create_json(lemmatized_dict, file_name):
	#result = json.dumps(lemmatized_dict, indent = 4)
	#print(result)
	with open(file_name, "w") as outfile:
	    json.dump(lemmatized_dict, outfile, indent = 4)

phenol_explorer_dict = create_phenol_explorer_food_dict(phenol_foods_file)
#print(phenol_explorer_dict)

lemmatized_phenol_explorer_dict = lemmatize_phenol_explorer_food_dict(stopwords, phenol_explorer_dict)
#print(lemmatized_phenol_explorer_dict)
	
stopwords = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
#name = "Sorghum bicolor L." #solo un caso (3 matches)
#name = "Triticum aestivum L." #más de un caso (3 matches)
#name = "Setaria italica (L.) P.Beauv." #muchos casos (coincide la L.)(1 match)
#name = "Eragrostis tef (Zucc.) Trotter" #todos los casos (0 matches)
#name = input("Introduce a scientific name: ")
name = "Sorghum bicolor L."
lemmatized_food_name = lemmatize_food_name(lemmatizer, stopwords, name)
foodex2_phenol_explorer_food_matches_dict = update_foodex2_phenol_explorer_food_matches_dict(lemmatized_food_name, lemmatized_phenol_explorer_dict)
phenol_explorer_composition_data_list = create_phenol_explorer_composition_data_list(phenol_composition_data_file)
composition_data_dict = create_composition_data_dict(foodex2_phenol_explorer_food_matches_dict, phenol_explorer_composition_data_list)
create_json(composition_data_dict, foodex2_phenol_explorer_matches_file)
print(composition_data_dict)