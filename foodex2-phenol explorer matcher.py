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

lemmatizer = WordNetLemmatizer()

def create_phenol_explorer_food_scientific_names_dict(phenol_explorer_file):
	phenol_explorer_data = pd.read_excel(phenol_explorer_file, sheet_name="Phenol-Explorer Foods")
	phenol_explorer_df = pd.DataFrame(phenol_explorer_data)		
	return dict(zip(phenol_explorer_df['ID'], phenol_explorer_df['Scientific Name']))

def create_phenol_explorer_food_names_dict(phenol_explorer_file):
	phenol_explorer_data = pd.read_excel(phenol_explorer_file, sheet_name="Phenol-Explorer Foods")
	phenol_explorer_df = pd.DataFrame(phenol_explorer_data)		
	return dict(zip(phenol_explorer_df['ID'], phenol_explorer_df['Name']))

def create_foodex2_scientific_names_dict(foodex2_file):
	foodex2_data = pd.read_excel(foodex2_file, sheet_name="term")
	foodex2_df = pd.DataFrame(foodex2_data)		
	return dict(zip(foodex2_df['termCode'], foodex2_df['scientificNames']))

def create_foodex2_dict(foodex2_file):
	foodex2_data = pd.read_excel(foodex2_file, sheet_name="term")
	foodex2_df = pd.DataFrame(foodex2_data)		
	return dict(zip(foodex2_df['termCode'], foodex2_df['termExtendedName']))

def process_foodex2_scientific_names_dict(foodex2_dict):
	foodex2_scientific_names_dict_processed = {}
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
			foodex2_scientific_names_dict_processed[entry] = scientific_name_filtered
	return foodex2_scientific_names_dict_processed


def create_scientific_names_matches_list(foodex2_scientific_name, phenol_explorer_food_dict):
	scientific_names_matches_list = []
	for phenol_explorer_code in phenol_explorer_food_dict:
		phenol_explorer_scientific_name = str(phenol_explorer_food_dict[phenol_explorer_code])
		if foodex2_scientific_name in phenol_explorer_scientific_name:
			scientific_names_matches_list.append(phenol_explorer_code)
			#print(str(phenol_explorer_code) + " => " + phenol_explorer_scientific_name)
	return scientific_names_matches_list

stopwords_list = ["type","n/e","unspecified","not specified","i","me","my","myself","we","our","ours","ourselves","you","you're","you've","you'll","you'd","your","yours","yourself","yourselves","he","him","his","himself","she","she's","her","hers","herself","it","it's","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","that'll","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","but","if","because","as","until","while","of","at","by","for","about","against","between","into","through","during","before","after","above","below","to","from","up","down","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","don't","should","should've","now","d","ll","m","o","re","ve","y","ain","aren","aren't","couldn","couldn't","didn","didn't","doesn","doesn't","hadn","hadn't","hasn","hasn't","haven","haven't","isn","isn't","ma","mightn","mightn't","mustn","mustn't","needn","needn't","shan","shan't","shouldn","shouldn't","wasn","wasn't","weren","weren't","won","won't","wouldn","wouldn't"]

def lemmatize_modifier(modifier):
	modifier_tagged = nltk.pos_tag(nltk.regexp_tokenize(modifier, pattern=r"\s|\(|\)|\[.*\]|[.,;'-]|\"", gaps=True))
	modifier_lemas_list = []

	for (word, tag) in modifier_tagged:
		if word not in stopwords_list:
			if(tag.startswith('J')):
				lema = lemmatizer.lemmatize(word.lower(), wordnet.ADJ)
				modifier_lemas_list.append(lema)
			elif tag.startswith('V'):
				lema = lemmatizer.lemmatize(word.lower(), wordnet.VERB)
				modifier_lemas_list.append(lema)
			elif tag.startswith('N'):
				lema = lemmatizer.lemmatize(word.lower(), wordnet.NOUN)
				modifier_lemas_list.append(lema)
			elif tag.startswith('R'):
				lema = lemmatizer.lemmatize(word.lower(), wordnet.ADV)        
				modifier_lemas_list.append(lema)
			else:
				lema = lemmatizer.lemmatize(word.lower())
				modifier_lemas_list.append(lema)

	modifier_lemas = " ".join(modifier_lemas_list)
	return modifier_lemas

def process_phenol_explorer_food_names_dict(phenol_explorer_food_names_dict, scientific_names_matches_list):
	phenol_explorer_food_names_dict_processed = {}
	phenol_explorer_iterable = []

	if scientific_names_matches_list != []:
		phenol_explorer_iterable = scientific_names_matches_list
	else:
		phenol_explorer_iterable = phenol_explorer_food_names_dict

	for phenol_explorer_code in phenol_explorer_iterable:
		food_name = phenol_explorer_food_names_dict[phenol_explorer_code]
		food_name_splitted_by_comma = food_name.split(", ")
	
		ordered_food_name_list = []
		for modifier in food_name_splitted_by_comma:
			if "[" in modifier and "]" in modifier:
				start = modifier.index('[')
				end = modifier.index(']')
				first_words = modifier[:start-1]
				last_words = modifier[start+1:end]
				modifier = last_words + " " + first_words
	
			food_name_splitted_by_spaces = modifier.split(" ")
			for word in food_name_splitted_by_spaces:
				if word not in word_list:
					ordered_food_name_list.append(word)
	
		ordered_food_name = " ".join(ordered_food_name_list)
		food_name_lemmatized = lemmatize_modifier(ordered_food_name)
		phenol_explorer_food_names_dict_processed[phenol_explorer_code] = food_name_lemmatized.split(" ")
	
	return phenol_explorer_food_names_dict_processed


"""

foodex2_scientific_names_dict = create_foodex2_scientific_names_dict(foodex2_file)
foodex2_scientific_names_dict_processed = process_foodex2_scientific_names_dict(foodex2_scientific_names_dict)

##casos de ejemplo que tienen coincidencias
#foodex2_scientific_name = foodex2_scientific_names_dict_processed[list(foodex2_scientific_names_dict_processed.keys())[6]]
#foodex2_scientific_name = foodex2_scientific_names_dict_processed[list(foodex2_scientific_names_dict_processed.keys())[8]]
#foodex2_scientific_name = foodex2_scientific_names_dict_processed[list(foodex2_scientific_names_dict_processed.keys())[9]]
#foodex2_scientific_name = foodex2_scientific_names_dict_processed[list(foodex2_scientific_names_dict_processed.keys())[12]]
#foodex2_scientific_name = foodex2_scientific_names_dict_processed[list(foodex2_scientific_names_dict_processed.keys())[145]]
#foodex2_scientific_name = foodex2_scientific_names_dict_processed[list(foodex2_scientific_names_dict_processed.keys())[503]]
#foodex2_scientific_name = foodex2_scientific_names_dict_processed["A000T"]
#foodex2_scientific_name = foodex2_scientific_names_dict_processed["A000J"] #no tiene nombre científico

foodex2_code = "A000T"
foodex2_scientific_name = ""
if foodex2_code in foodex2_scientific_names_dict_processed:
	foodex2_scientific_name = foodex2_scientific_names_dict_processed[foodex2_code]

phenol_explorer_food_dict = create_phenol_explorer_food_scientific_names_dict(phenol_foods_file)

scientific_names_matches_list = create_scientific_names_matches_dict(foodex2_scientific_name, phenol_explorer_food_dict)

print(scientific_names_matches_list)


##imprimir los nombres cientificos procesados numerados
#num = 0
#for entry in foodex2_scientific_names_dict_processed:
#	print(str(num) + " => " + entry + " => " + foodex2_scientific_names_dict_processed[entry])
#	num = num + 1 

"""

def create_foodex2_phenol_explorer_matches_dict(foodex2_name_list, phenol_explorer_names_dict):
	foodex2_phenol_explorer_matches_dict = {}
	maximum_matches = 0

	for phenol_explorer_code in phenol_explorer_names_dict:
		matches = 0

		for word in foodex2_name_list:
			if word in phenol_explorer_names_dict[phenol_explorer_code]:
				matches = matches+1

		if matches > maximum_matches:
			maximum_matches = matches
			foodex2_phenol_explorer_matches_dict = {phenol_explorer_code: phenol_explorer_names_dict[phenol_explorer_code]}
		elif matches == maximum_matches and maximum_matches != 0:
			foodex2_phenol_explorer_matches_dict[phenol_explorer_code] = phenol_explorer_names_dict[phenol_explorer_code]

	return foodex2_phenol_explorer_matches_dict


def get_foodex2_ratio(foodex2_name_list, phenol_explorer_food_name_list):
	foodex2_matches = 0
	foodex2_food_lemas_len = 0

	for foodex2_food_lema in foodex2_name_list:
		if foodex2_food_lema in phenol_explorer_food_name_list:
			foodex2_matches = foodex2_matches + 1

	foodex2_food_lemas_len = len(foodex2_name_list)

	foodex2_ratio = foodex2_matches / foodex2_food_lemas_len
	return foodex2_ratio

def get_phenol_explorer_ratio(phenol_explorer_food_name_list, foodex2_name_list):
	phenol_explorer_matches = 0
	phenol_explorer_food_lemas_len = 0

	for phenol_explorer_food_lema in phenol_explorer_food_name_list:
		if phenol_explorer_food_lema in foodex2_name_list:
			phenol_explorer_matches = phenol_explorer_matches + 1

	phenol_explorer_food_lemas_len = len(phenol_explorer_food_name_list)

	phenol_explorer_ratio = phenol_explorer_matches / phenol_explorer_food_lemas_len
	return phenol_explorer_ratio

def create_foodex2_phenol_explorer_matches_ratio_dict(foodex2_name_list, foodex2_phenol_explorer_matches_dict):
	foodex2_phenol_explorer_matches_ratio_dict = {}

	for phenol_explorer_code in foodex2_phenol_explorer_matches_dict:
		phenol_explorer_food_name_list = foodex2_phenol_explorer_matches_dict[phenol_explorer_code]
		foodex2_ratio = get_foodex2_ratio(foodex2_name_list, phenol_explorer_food_name_list)
		phenol_explorer_ratio = get_phenol_explorer_ratio(phenol_explorer_food_name_list, foodex2_name_list)
		foodex2_phenol_explorer_matches_ratio_dict[phenol_explorer_code] = [phenol_explorer_food_name_list, foodex2_ratio, phenol_explorer_ratio]

	return foodex2_phenol_explorer_matches_ratio_dict

def format_foodex2_food_name_word_list(foodex2_food_name):	
	foodex2_food_name_word_list = []
	food_name_splitted_by_comma = foodex2_food_name.split(", ")
	for food_name_comma_part in food_name_splitted_by_comma:
		food_name_lemmatized = lemmatize_modifier(food_name_comma_part)
		food_name_splitted_by_spaces = food_name_lemmatized.split(" ")
		for food_name_space_part in food_name_splitted_by_spaces:
			foodex2_food_name_word_list.append(food_name_space_part)

	return foodex2_food_name_word_list

def filter_foodex2_phenol_explorer_matches_ratios(foodex2_phenol_explorer_matches_ratio_dict):
	new_foodex2_phenol_explorer_matches_ratio_dict = {}
	maximum_foodex2_ratio = 0
	
	for phenol_explorer_code in foodex2_phenol_explorer_matches_ratio_dict:
		maximum_ratio = foodex2_phenol_explorer_matches_ratio_dict[phenol_explorer_code][1]
		if maximum_ratio > maximum_foodex2_ratio:
			maximum_foodex2_ratio = maximum_ratio
			new_foodex2_phenol_explorer_matches_ratio_dict = {phenol_explorer_code: foodex2_phenol_explorer_matches_ratio_dict[phenol_explorer_code]}
		elif maximum_ratio == maximum_foodex2_ratio:
			new_foodex2_phenol_explorer_matches_ratio_dict[phenol_explorer_code] = foodex2_phenol_explorer_matches_ratio_dict[phenol_explorer_code]

	foodex2_phenol_explorer_matches_ratios_dict_filtered = {}
	maximum_phenol_explorer_ratio = 0

	for phenol_explorer_code in new_foodex2_phenol_explorer_matches_ratio_dict:
		maximum_ratio = new_foodex2_phenol_explorer_matches_ratio_dict[phenol_explorer_code][2]
		if maximum_ratio > maximum_phenol_explorer_ratio:
			maximum_phenol_explorer_ratio = maximum_ratio
			foodex2_phenol_explorer_matches_ratios_dict_filtered = {phenol_explorer_code: new_foodex2_phenol_explorer_matches_ratio_dict[phenol_explorer_code]}
		elif maximum_ratio == maximum_phenol_explorer_ratio:
			foodex2_phenol_explorer_matches_ratios_dict_filtered[phenol_explorer_code] = new_foodex2_phenol_explorer_matches_ratio_dict[phenol_explorer_code]

	return foodex2_phenol_explorer_matches_ratios_dict_filtered

word_list = ["raw", "fresh", "peeled", "whole", "dehulled", "dried"]




def get_foodex2_phenol_explorer_match(foodex2_code):
	scientific_names_matches_list = []
	if foodex2_code in foodex2_scientific_names_dict_processed:
		foodex2_scientific_name = foodex2_scientific_names_dict_processed[foodex2_code]
	
	
		previous_scientific_names_matches_list = create_scientific_names_matches_list(foodex2_scientific_name, phenol_explorer_food_dict)
		
		if previous_scientific_names_matches_list != {}:
			scientific_names_matches_list = previous_scientific_names_matches_list
	
	foodex2_food_name = foodex2_dict[foodex2_code]

	foodex2_food_name_word_list = format_foodex2_food_name_word_list(foodex2_food_name)
	print(foodex2_food_name_word_list)
	
	foodex2_phenol_explorer_matches_dict = create_foodex2_phenol_explorer_matches_dict(foodex2_food_name_word_list, phenol_explorer_food_names_dict_processed)
	
	foodex2_phenol_explorer_matches_ratio_dict = create_foodex2_phenol_explorer_matches_ratio_dict(foodex2_food_name_word_list, foodex2_phenol_explorer_matches_dict)

	foodex2_phenol_explorer_matches_ratio_dict_filtered = filter_foodex2_phenol_explorer_matches_ratios(foodex2_phenol_explorer_matches_ratio_dict)

	print(foodex2_phenol_explorer_matches_ratio_dict_filtered)


foodex2_scientific_names_dict = create_foodex2_scientific_names_dict(foodex2_file)
foodex2_scientific_names_dict_processed = process_foodex2_scientific_names_dict(foodex2_scientific_names_dict)
phenol_explorer_food_dict = create_phenol_explorer_food_scientific_names_dict(phenol_foods_file)
foodex2_dict = create_foodex2_dict(foodex2_file)
phenol_explorer_food_names_dict = create_phenol_explorer_food_names_dict(phenol_foods_file)
phenol_explorer_food_names_dict_processed = process_phenol_explorer_food_names_dict(phenol_explorer_food_names_dict, scientific_names_matches_list)

foodex2_code = "A002Z"
#foodex2_code = "A000T"
foodex2_code = "A005G"
get_foodex2_phenol_explorer_match(foodex2_code)