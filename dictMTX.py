import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
import json
import warnings
from collections import OrderedDict

#from nltk.tokenize import word_tokenize

phenol_foods = "./dbs/foods.xls"
foodex2_file = "./dbs/MTX.xls"
phenol_composition_file = "./dbs/composition-data.xlsx"

"""
foodex2_data = pd.read_excel(foodex2_file, sheet_name="term")
foodex2_df = pd.DataFrame(foodex2_data)
foodex2_dict = dict(zip(foodex2_df['termCode'], foodex2_df['termExtendedName']))


stopwords = set(stopwords.words('english'))


lemmatizer = WordNetLemmatizer()

for code in foodex2_dict:
	extended_name = foodex2_dict.get(code)

	tk_content = word_tokenize(extended_name)
	wordsFiltered=[]
	for i in tk_content:
		if i not in stopwords:
			wordsFiltered.append(i)

	lemmatized_words = [lemmatizer.lemmatize(i) for i in wordsFiltered] 
	foodex2_dict[code] = lemmatized_words
	
print(foodex2_dict)
"""

#warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

def create_foodex2_dict():
	foodex2_data = pd.read_excel(foodex2_file, sheet_name="term")
	foodex2_df = pd.DataFrame(foodex2_data)		
	return dict(zip(foodex2_df['termCode'], foodex2_df['termExtendedName']))

def lemmatize_foodex2_dict(stopwords, foodex2_dict):
	stopwords = set(stopwords.words('english'))
	lemmatizer = WordNetLemmatizer()
	lemmatized_foodex2_dict = {}

	for foodex2_code in foodex2_dict:
		extended_food_name = foodex2_dict[foodex2_code]
		#extended_food_name_tagged = nltk.pos_tag(word_tokenize(extended_food_name))
		#print(extended_food_name_tagged)
		extended_food_name_tagged = nltk.pos_tag(nltk.regexp_tokenize(extended_food_name, pattern=r"\s|[\.,;'()-]", gaps=True))
		extended_food_name_lema = []
		
		for (word, tag) in extended_food_name_tagged:
			if word not in stopwords:
				if(tag.startswith('J')):
					lema = lemmatizer.lemmatize(word, wordnet.ADJ)
					extended_food_name_lema.append(lema.lower())
				elif tag.startswith('V'):
					lema = lemmatizer.lemmatize(word, wordnet.VERB)
					extended_food_name_lema.append(lema.lower())
				elif tag.startswith('N'):
					lema = lemmatizer.lemmatize(word, wordnet.NOUN)
					extended_food_name_lema.append(lema.lower())
				elif tag.startswith('R'):
					lema = lemmatizer.lemmatize(word, wordnet.ADV)        
					extended_food_name_lema.append(lema.lower())
				else:
					lema = lemmatizer.lemmatize(word)
					extended_food_name_lema.append(lema.lower())
		
		lemmatized_foodex2_dict[foodex2_code] = extended_food_name_lema
	
	#print(lemmatized_foodex2_dict)
	return lemmatized_foodex2_dict

def create_foodex2_json(lemmatized_foodex2_dict):
	#result = json.dumps(lemmatized_foodex2_dict, indent = 4)
	#print(result)
	with open("./dbs/sample.json", "w") as outfile:
	    json.dump(lemmatized_foodex2_dict, outfile, indent = 4)

"""
name_BEDCA = "oat"
matches_dict = {}
for code in foodex2_dict:
	extended_name = foodex2_dict.get(code)
	for words in extended_name:
		if words == name_BEDCA:
			matches_dict[code] = extended_name

print(matches_dict)
"""
#foodex2_dict = {'A': ["oat", "fee", "parpa", "paco"],
#				'B': ["paco", "oat"],
#				'C': ["pepe", "amancio"]}

def format_BEDCA_name(BEDCA_food_name):
	BEDCA_food_ingredients_list = []
	BEDCA_food_ingredient = BEDCA_food_name.split(", ")
	
	for BEDCA_food_modifier in BEDCA_food_ingredient:
		BEDCA_food_ingredients_list.append(BEDCA_food_modifier.split(" "))
	
	return BEDCA_food_ingredients_list
	#BEDCA_food_ingredients_list = [[oat, fee], [fee, parpa], [papa, paprre, perd]]

def create_BEDCA_foodex2_matches_dict(BEDCA_food_ingredients_list, lemmatized_foodex2_dict):
	BEDCA_foodex2_matches_dict = {}
	
	matched = True
	for foodex2_code in lemmatized_foodex2_dict:
		for ingredient_to_match in BEDCA_food_ingredients_list[0]:						#primer elemento de la lista oat de [oat, fee]
			if ingredient_to_match not in lemmatized_foodex2_dict[foodex2_code]:
				matched = False
				break
	
		if matched == True:
			BEDCA_foodex2_matches_dict[foodex2_code] = (0, lemmatized_foodex2_dict[foodex2_code])
		
		matched = True

	#print(BEDCA_foodex2_matches_dict)
	return BEDCA_foodex2_matches_dict

def update_BEDCA_foodex2_matches_dict(BEDCA_food_ingredients_list, BEDCA_foodex2_matches_dict):
	matched = True
	for foodex2_code in BEDCA_foodex2_matches_dict:
		for modifier_n in range(1, len(BEDCA_food_ingredients_list)):
			for modifier_to_match in BEDCA_food_ingredients_list[modifier_n]:
				(matches_accumulator, extended_food_name_lema) = BEDCA_foodex2_matches_dict[foodex2_code]
				if modifier_to_match not in extended_food_name_lema:
					matched = False
					break
			
			if matched == True:
				(matches_accumulator, extended_food_name_lema) = BEDCA_foodex2_matches_dict[foodex2_code]
				BEDCA_foodex2_matches_dict[foodex2_code] = (matches_accumulator+1, extended_food_name_lema)
			
			matched = True
	
	#print(BEDCA_foodex2_matches_dict)
	return BEDCA_foodex2_matches_dict


def create_BEDCA_foodex2_matches_dict_sorted(BEDCA_foodex2_matches_dict):
	reverse_order_BEDCA_foodex2_matches_dict = OrderedDict()

	for foodex2_code in BEDCA_foodex2_matches_dict:
		(matches_accumulator, extended_food_name_lema) = BEDCA_foodex2_matches_dict[foodex2_code]
		reverse_order_BEDCA_foodex2_matches_list = sorted(reverse_order_BEDCA_foodex2_matches_dict.keys())
		last_key = -1
		
		if reverse_order_BEDCA_foodex2_matches_list != []:
			last_key = reverse_order_BEDCA_foodex2_matches_list[-1]

		if matches_accumulator > last_key or last_key == -1:
			reverse_order_BEDCA_foodex2_matches_dict[matches_accumulator] = [(foodex2_code, extended_food_name_lema)]
		else:
			reverse_order_BEDCA_foodex2_matches_dict[matches_accumulator].append((foodex2_code, extended_food_name_lema))

	sorted_BEDCA_foodex2_matches_dict = OrderedDict(reversed(list(reverse_order_BEDCA_foodex2_matches_dict.items())))
	
	print("\nSorted BEDCA-foodex2 matches dict: " + str(sorted_BEDCA_foodex2_matches_dict), end='\n\n')
	return sorted_BEDCA_foodex2_matches_dict	

def create_most_BEDCA_foodex2_matches_dict(sorted_BEDCA_foodex2_matches_dict):
	most_BEDCA_foodex2_matches_list = list(sorted_BEDCA_foodex2_matches_dict.items())[0]
	(matches_accumulator, matches_list) = most_BEDCA_foodex2_matches_list
	most_BEDCA_foodex2_matches_dict = {}
	
	for match in matches_list:
		(code, extended_name_lemas) = match
		most_BEDCA_foodex2_matches_dict[code] = extended_name_lemas
	
	print("Most BEDCA-foodex2 matches: " + str(most_BEDCA_foodex2_matches_dict), end='\n\n')
	return most_BEDCA_foodex2_matches_dict

"""
def create_most_matches_dict1(matches_dict):
	biggest_match = 0
	for code in matches_dict:
		(acc, entry) = matches_dict[code]
		if acc > biggest_match:
			biggest_match = acc
	#print(biggest_match)

	most_matched_dict = {}
	for code in matches_dict:
		(acc, entry) = matches_dict[code]
		if acc == biggest_match:
			most_matched_dict[code] = (acc, entry)
	print(most_matched_dict)
"""

foodex2_dict = create_foodex2_dict()
lemmatized_foodex2_dict = lemmatize_foodex2_dict(stopwords, foodex2_dict)
create_foodex2_json(lemmatized_foodex2_dict)
BEDCA_name = "oat grain, roll, red"
#BEDCA_name = input("Introduce a BEDCA food name: ") #"oat grain, roll, red"
BEDCA_food_ingredients_list = format_BEDCA_name(BEDCA_name)
BEDCA_foodex2_matches_dict = create_BEDCA_foodex2_matches_dict(BEDCA_food_ingredients_list, lemmatized_foodex2_dict)
BEDCA_foodex2_matches_dict = update_BEDCA_foodex2_matches_dict(BEDCA_food_ingredients_list, BEDCA_foodex2_matches_dict)
BEDCA_foodex2_matches_dict_sorted = create_BEDCA_foodex2_matches_dict_sorted(BEDCA_foodex2_matches_dict)
most_BEDCA_foodex2_matches_dict = create_most_BEDCA_foodex2_matches_dict(BEDCA_foodex2_matches_dict_sorted)