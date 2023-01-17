import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import json
from food_terminologies.BEDCA import BEDCA_food
from FoodTokenizer import Term, Subterm, Coindicence

input_directory = "./input dbs/"
phenol_foods = input_directory + "foods.xls"
foodex2_file = input_directory + "MTX.xls"
phenol_composition_file = input_directory + "composition-data.xlsx"
BEDCA_file = input_directory + "bedca-2.1.csv"

output_directory = "./output json files/"
BEDCA_lemas_file = output_directory + "BEDCA lemas.json"
foodex2_lemas_file = output_directory + "foodex2 lemas.json"
BEDCA_foodex2_matches_file = output_directory + "BEDCA_foodex2 matches.json"

stopwords_list = ["type","n/e","unspecified","not specified","i","me","my","myself","we","our","ours","ourselves","you","you're","you've","you'll","you'd","your","yours","yourself","yourselves","he","him","his","himself","she","she's","her","hers","herself","it","it's","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","that'll","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","but","if","because","as","until","while","of","at","by","for","about","against","between","into","through","during","before","after","above","below","to","from","up","down","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","don't","should","should've","now","d","ll","m","o","re","ve","y","ain","aren","aren't","couldn","couldn't","didn","didn't","doesn","doesn't","hadn","hadn't","hasn","hasn't","haven","haven't","isn","isn't","ma","mightn","mightn't","mustn","mustn't","needn","needn't","shan","shan't","shouldn","shouldn't","wasn","wasn't","weren","weren't","won","won't","wouldn","wouldn't"]
conjunction_list = ["without","with","and","or","on","in"]

lemmatizer = WordNetLemmatizer()


def create_BEDCA_dict(BEDCA_file):
	BEDCA_data = pd.read_csv(BEDCA_file, sep=';', encoding='windows-1252') 
	BEDCA_df = pd.DataFrame(BEDCA_data)		
	return dict(zip(BEDCA_df['id'], BEDCA_df['nombre_inglés']))

def create_foodex2_dict(foodex2_file):
	foodex2_data = pd.read_excel(foodex2_file, sheet_name="term")
	foodex2_df = pd.DataFrame(foodex2_data)		
	return dict(zip(foodex2_df['termCode'], foodex2_df['termExtendedName']))

def create_foodex2_facet_dict(foodex2_file):
	foodex2_data = pd.read_excel(foodex2_file, sheet_name="term")
	foodex2_df = pd.DataFrame(foodex2_data)
	facets_zipped = list(zip(foodex2_df['partParentCode'], foodex2_df['ingredParentCode'], foodex2_df['packformatParentCode'], foodex2_df['processParentCode']))
	return dict(zip(foodex2_df['termCode'], facets_zipped))


def lemmatize_modifier(modifier):
	modifier_tagged = nltk.pos_tag(nltk.regexp_tokenize(modifier, pattern=r"\s|\(|\)|\[.*\]|[.,;'-]|\"", gaps=True))
	modifier_lemas = []

	for (word, tag) in modifier_tagged:
		if word not in stopwords_list:
			if(tag.startswith('J')):
				lema = lemmatizer.lemmatize(word.lower(), wordnet.ADJ)
				modifier_lemas.append(lema)
			elif tag.startswith('V'):
				lema = lemmatizer.lemmatize(word.lower(), wordnet.VERB)
				modifier_lemas.append(lema)
			elif tag.startswith('N'):
				lema = lemmatizer.lemmatize(word.lower(), wordnet.NOUN)
				modifier_lemas.append(lema)
			elif tag.startswith('R'):
				lema = lemmatizer.lemmatize(word.lower(), wordnet.ADV)        
				modifier_lemas.append(lema)
			else:
				lema = lemmatizer.lemmatize(word.lower())
				modifier_lemas.append(lema)
		
	#ver qué hacer con foodex2 ---> Bread and rolls with special ingredients added
	return modifier_lemas

def lemmatize_dict(BEDCA_dict):
	dict_lemmatized = {}

	#[[oat, grain], [roll], [red]]
	for BEDCA_code in BEDCA_dict:
		food_name = BEDCA_dict[BEDCA_code]
		food_modifiers = food_name.split(", ")
		food_lemas = []

		for modifier in food_modifiers:
			modifier_lemas = lemmatize_modifier(modifier)
			if modifier_lemas != []:
				food_lemas.append(modifier_lemas)
		
		dict_lemmatized[BEDCA_code] = food_lemas
	
	return dict_lemmatized

def lemmatize_name(BEDCA_dict, BEDCA_code):
	food_name = BEDCA_dict[BEDCA_code]
	food_modifiers = food_name.split(", ")
	food_lemas = []

	for modifier in food_modifiers:
		modifier_lemas = lemmatize_modifier(modifier)
		if modifier_lemas != []:
			food_lemas.append(modifier_lemas)
		
	return food_lemas

def create_BEDCA_foodex2_matches_list(BEDCA_food_lemas_list, foodex2_dict_lemmatized):
	BEDCA_foodex2_matches_list = []
	maximum_matches = 0

	for foodex2_code in foodex2_dict_lemmatized:
		matches = 0

		for lema in BEDCA_food_lemas_list:
			for foodex2_food_lemas in foodex2_dict_lemmatized[foodex2_code]:
				if lema in foodex2_food_lemas:
					matches = matches+1
					break#si no puede contar el mismo match dos veces 

		matches = matches+1

		if matches > maximum_matches:
			maximum_matches = matches
			BEDCA_foodex2_matches_list = [foodex2_code]
		elif matches == maximum_matches and maximum_matches != 0:
			BEDCA_foodex2_matches_list.append(foodex2_code)

	return BEDCA_foodex2_matches_list

def get_BEDCA_ratio(BEDCA_food_lemas_list, foodex2_food_lemas_list):
	BEDCA_matches = 0
	BEDCA_food_lemas_len = 0

	for BEDCA_food_lema in BEDCA_food_lemas_list:

		for foodex2_modifier_lemas in foodex2_food_lemas_list:
			if BEDCA_food_lema in foodex2_modifier_lemas:
				BEDCA_matches = BEDCA_matches + 1
				break#si no puede contar el mismo match dos veces 

	BEDCA_food_lemas_len = len(BEDCA_food_lemas_list)

	BEDCA_ratio = BEDCA_matches / BEDCA_food_lemas_len
	return BEDCA_ratio

def get_foodex2_ratio(foodex2_food_lemas_list, BEDCA_food_lemas_list):
	foodex2_matches = 0
	foodex2_food_lemas_len = 0

	for foodex2_modifier_lemas in foodex2_food_lemas_list:
		
		for foodex2_food_lema in foodex2_modifier_lemas:
			if foodex2_food_lema in BEDCA_food_lemas_list:
				foodex2_matches = foodex2_matches + 1

		foodex2_food_lemas_len = foodex2_food_lemas_len + len(foodex2_modifier_lemas)

	foodex2_ratio = foodex2_matches / foodex2_food_lemas_len
	return foodex2_ratio

def create_BEDCA_foodex2_matches_ratio_dict(BEDCA_food_lemas_list, foodex2_dict_lemmatized, BEDCA_foodex2_matches_list):
	BEDCA_foodex2_matches_ratio_dict = {}

	for foodex2_code in BEDCA_foodex2_matches_list:
		foodex2_food_lemas_list = foodex2_dict_lemmatized[foodex2_code]
		BEDCA_ratio = get_BEDCA_ratio(BEDCA_food_lemas_list, foodex2_food_lemas_list)
		foodex2_ratio = get_foodex2_ratio(foodex2_food_lemas_list, BEDCA_food_lemas_list)
		BEDCA_foodex2_matches_ratio_dict[foodex2_code] = [foodex2_food_lemas_list, BEDCA_ratio, foodex2_ratio]

	#print(BEDCA_foodex2_matches_ratio_dict)
	return BEDCA_foodex2_matches_ratio_dict

def filter_BEDCA_foodex2_matches_ratios(BEDCA_foodex2_matches_dict, ratio_flag):
	BEDCA_ratio_flag = 1
	foodex2_ratio_flag = 2

	if ratio_flag == BEDCA_ratio_flag:

		maximum_BEDCA_ratio = 0
		foodex2_ratio_dict = {}
	
		for foodex2_code in BEDCA_foodex2_matches_dict:
			BEDCA_ratio = BEDCA_foodex2_matches_dict[foodex2_code][ratio_flag]
			foodex2_ratio = BEDCA_foodex2_matches_dict[foodex2_code][foodex2_ratio_flag]
			if BEDCA_ratio > maximum_BEDCA_ratio:
				foodex2_ratio_dict = {foodex2_code: foodex2_ratio}
				maximum_BEDCA_ratio = BEDCA_ratio
			elif BEDCA_ratio == maximum_BEDCA_ratio:
				foodex2_ratio_dict[foodex2_code] = foodex2_ratio
		return foodex2_ratio_dict

	elif ratio_flag == foodex2_ratio_flag:
		maximum_foodex2_ratio = 0
		BEDCA_foodex2_matches_list = []
	
		for foodex2_code in BEDCA_foodex2_matches_dict:
			foodex2_ratio = BEDCA_foodex2_matches_dict[foodex2_code]
			
			if foodex2_ratio > maximum_foodex2_ratio:
				maximum_foodex2_ratio = foodex2_ratio
				BEDCA_foodex2_matches_list = [foodex2_code]
			elif foodex2_ratio == maximum_foodex2_ratio:
				maximum_foodex2_ratio = foodex2_ratio
				BEDCA_foodex2_matches_list.append(foodex2_code)
	
		return BEDCA_foodex2_matches_list

def create_BEDCA_foodex2_matches_facet_lists(BEDCA_foodex2_matches_list, foodex2_facet_dict):
	parts_list = []
	ingredients_list = []
	packformats_list = []
	processes_list = []

	for foodex2_code in BEDCA_foodex2_matches_list:
		if not pd.isna(foodex2_facet_dict[foodex2_code][0]):
			parts_list.append(foodex2_code)
		if not pd.isna(foodex2_facet_dict[foodex2_code][1]):
			ingredients_list.append(foodex2_code)
		if not pd.isna(foodex2_facet_dict[foodex2_code][2]):
			packformats_list.append(foodex2_code)
		if not pd.isna(foodex2_facet_dict[foodex2_code][3]):
			processes_list.append(foodex2_code)

	BEDCA_foodex2_matches_facet_lists = [parts_list, ingredients_list, packformats_list, processes_list]

	return BEDCA_foodex2_matches_facet_lists

def get_facet_parents_list(foodex2_code, foodex2_parents_list, foodex2_facet_dict, facet):
	if foodex2_code == "root":
		return foodex2_parents_list
	else:
		foodex2_parent_code = foodex2_facet_dict[foodex2_code][facet]
		foodex2_parents_list.append(foodex2_parent_code)
		return get_facet_parents_list(foodex2_parent_code, foodex2_parents_list, foodex2_facet_dict, facet)

def order_BEDCA_foodex2_matches_facet_lists(BEDCA_foodex2_matches_facet_lists, foodex2_facet_dict):
	ordered_BEDCA_foodex2_matches_facet_lists = []
	for facet in range(0, len(BEDCA_foodex2_matches_facet_lists)):
		facet_list = BEDCA_foodex2_matches_facet_lists[facet]
		ordered_BEDCA_foodex2_matches_list = []
		
		if facet_list != []:
			childs_count_dict = {}
			facet_parents_count_dict = {}
			#crear dict con foodex2 codes ordenados por la cantidad de hijos que tengan
			#crear dict con foodex2 codes con la cantidad de padres que tiene cada uno
			for facet_foodex2_code in facet_list:
				foodex2_parents_list = get_facet_parents_list(facet_foodex2_code, [], foodex2_facet_dict, facet)
				facet_parents_count_dict[facet_foodex2_code] = len(foodex2_parents_list)
		
				for facet_element in facet_list:
					if facet_element in foodex2_parents_list:
						if facet_element in childs_count_dict:
							childs_count_dict[facet_element] = childs_count_dict[facet_element] + 1
						else:
							childs_count_dict[facet_element] = 1
				
				if facet_foodex2_code not in childs_count_dict:
					childs_count_dict[facet_foodex2_code] = 0
		
			sorted_childs_count_dict = dict(sorted(childs_count_dict.items(), key=lambda x:x[1], reverse=True))
		
			parents_dict = {}
			for parent in sorted_childs_count_dict:
				if sorted_childs_count_dict[parent] in parents_dict:
					parents_dict[sorted_childs_count_dict[parent]][parent] = facet_parents_count_dict[parent]
				else:
					parents_dict[sorted_childs_count_dict[parent]] = {parent: facet_parents_count_dict[parent]}

			for parents in parents_dict:
				sorted_parents_dict = dict(sorted(parents_dict[parents].items(), key=lambda x:x[1]))
				sorted_parents_foodex2_codes = list(sorted_parents_dict.keys())
				for foodex2_code in sorted_parents_foodex2_codes:
					ordered_BEDCA_foodex2_matches_list.append(foodex2_code)

		ordered_BEDCA_foodex2_matches_facet_lists.append(ordered_BEDCA_foodex2_matches_list)

	return ordered_BEDCA_foodex2_matches_facet_lists

def create_coincidences_list(BEDCA_food_lemas_list, foodex2_dict_lemmatized, foodex2_facet_dict):
	BEDCA_foodex2_matches_list = create_BEDCA_foodex2_matches_list(BEDCA_food_lemas_list, foodex2_dict_lemmatized)

	BEDCA_foodex2_matches_ratio_dict = create_BEDCA_foodex2_matches_ratio_dict(BEDCA_food_lemas_list, foodex2_dict_lemmatized, BEDCA_foodex2_matches_list)

	foodex2_ratio_dict = filter_BEDCA_foodex2_matches_ratios(BEDCA_foodex2_matches_ratio_dict, 1)
	filtered_BEDCA_foodex2_matches_list = filter_BEDCA_foodex2_matches_ratios(foodex2_ratio_dict, 2)

	BEDCA_foodex2_matches_facet_lists = create_BEDCA_foodex2_matches_facet_lists(filtered_BEDCA_foodex2_matches_list, foodex2_facet_dict)

	coincidences_list = []
	
	if BEDCA_foodex2_matches_facet_lists != [[],[],[],[]]:
		filtered_BEDCA_foodex2_matches_list = order_BEDCA_foodex2_matches_facet_lists(BEDCA_foodex2_matches_facet_lists, foodex2_facet_dict)
		for facet_BEDCA_foodex2_matches_list in filtered_BEDCA_foodex2_matches_list:
			facet_coincidences_list = []
	
			if facet_BEDCA_foodex2_matches_list != []:
				for code in range(0, len(facet_BEDCA_foodex2_matches_list)):
					foodex2_code = facet_BEDCA_foodex2_matches_list[code]
					foodex2_food_lemas_list = BEDCA_foodex2_matches_ratio_dict[foodex2_code][0]
					BEDCA_ratio = BEDCA_foodex2_matches_ratio_dict[foodex2_code][1]
					ratio_foodex2 = BEDCA_foodex2_matches_ratio_dict[foodex2_code][2]
			
					new_coincidence = Coindicence(foodex2_code, foodex2_food_lemas_list, BEDCA_ratio, ratio_foodex2)
					facet_coincidences_list.append(new_coincidence)
			coincidences_list.append(facet_coincidences_list)

	return coincidences_list

def create_term(BEDCA_modifier_lemas, foodex2_dict_lemmatized, foodex2_facet_dict):
	actual_term_lema = []
	actual_term_subterm_list = []
	actual_term_coincidences = []
	
	subterm_flag = False
	last_lema = 0

	for lema in range(0, len(BEDCA_modifier_lemas)):
		if BEDCA_modifier_lemas[lema] in conjunction_list:
			if subterm_flag:
				new_term_lema = BEDCA_modifier_lemas[last_lema+1:lema]
				new_term_coincidences = create_coincidences_list(new_term_lema, foodex2_dict_lemmatized, foodex2_facet_dict)
				new_term = Term(new_term_lema, [], new_term_coincidences)

				new_subterm_conjunction = BEDCA_modifier_lemas[last_lema]
				new_subterm = Subterm(new_subterm_conjunction, new_term)

				actual_term_subterm_list.append(new_subterm)
				last_lema = lema
			else:
				if lema == 0:
					subterm_flag = True
					last_lema = lema
				else:
					actual_term_lema = BEDCA_modifier_lemas[:lema]
					actual_term_coincidences = create_coincidences_list(actual_term_lema, foodex2_dict_lemmatized, foodex2_facet_dict)

					subterm_flag = True
					last_lema = lema
	
		else:
			if lema == len(BEDCA_modifier_lemas)-1:
				if subterm_flag:
					new_term_lema = BEDCA_modifier_lemas[last_lema+1:]
					new_term_coincidences = create_coincidences_list(new_term_lema, foodex2_dict_lemmatized, foodex2_facet_dict)
					new_term = Term(new_term_lema, [], new_term_coincidences)

					new_subterm_conjunction = BEDCA_modifier_lemas[last_lema]
					new_subterm = Subterm(new_subterm_conjunction, new_term)

					actual_term_subterm_list.append(new_subterm)
				else:
					actual_term_lema = BEDCA_modifier_lemas
					actual_term_coincidences = create_coincidences_list(BEDCA_modifier_lemas, foodex2_dict_lemmatized, foodex2_facet_dict)

	actual_term = Term(actual_term_lema, actual_term_subterm_list, actual_term_coincidences)

	return actual_term

def create_BEDCA_food_object(BEDCA_element, BEDCA_element_lemmatized, foodex2_dict_lemmatized, foodex2_facet_dict):
	main_term = create_term(BEDCA_element_lemmatized[0], foodex2_dict_lemmatized, foodex2_facet_dict)
	term_list = []

	if len(BEDCA_element_lemmatized) > 1:
		
		for BEDCA_modifier in range(1, len(BEDCA_element_lemmatized)):
			term = create_term(BEDCA_element_lemmatized[BEDCA_modifier], foodex2_dict_lemmatized, foodex2_facet_dict)
			term_list.append(term)

	BEDCA_food_object = BEDCA_food(BEDCA_element, main_term, term_list)

	return BEDCA_food_object

def create_search_coincidences_dict(search):
	search_dict = {}

	search_lower = search.lower()
	search_word_list = search_lower.split()

	max_words_matched = 0
	
	for key, value in BEDCA_dict.items():
		words_matched = 0

		for word in search_word_list:
			if word in value.lower() and word not in stopwords_list and word not in conjunction_list:
				words_matched = words_matched + 1

		if words_matched > max_words_matched:
			max_words_matched = words_matched
			search_dict = {key: value}
		elif words_matched == max_words_matched:
			search_dict[key] = value

	return search_dict

def create_web_service_BEDCA_food(BEDCA_code):
	#BEDCA_dict = create_BEDCA_dict(BEDCA_file)
	#foodex2_dict = create_foodex2_dict(foodex2_file)
	#foodex2_dict_lemmatized = lemmatize_dict(foodex2_dict)
	#foodex2_facet_dict = create_foodex2_facet_dict(foodex2_file)

	BEDCA_element = BEDCA_dict[BEDCA_code]
	BEDCA_element_lemmatized = lemmatize_name(BEDCA_dict, BEDCA_code)

	BEDCA_food_object = create_BEDCA_food_object(BEDCA_element, BEDCA_element_lemmatized, foodex2_dict_lemmatized, foodex2_facet_dict)

	return(BEDCA_food_object)



def check_term_coincidence_ratio(term):
	coincidences_list = term.get_coincidence_list()
	
	for facet in coincidences_list:
		if facet != []:
			coincidence = facet[0]
			if coincidence.get_ri() == 1 and coincidence.get_rf() == 1:
				subterm_list = term.get_subterm_list()
				if subterm_list != []:
					check_term = True
					for subterm in subterm_list:
						term_subterm = subterm.get_term()
						if check_term_coincidence_ratio(term_subterm) == False:
							return False
					return True
				else:
					return True
			else:
				return False

def create_BEDCA_foodex2_matches_json(BEDCA_perfect_coincidences, BEDCA_not_perfect_coincidences):
	#result = json.dumps(lemmatized_foodex2_dict, indent = 4)
	#print(result)
	with open("./output json files/perfect matches.json", "w") as outfile:
	    json.dump(BEDCA_perfect_coincidences, outfile, indent = 4)

	with open("./output json files/not perfect matches.json", "w") as outfile:
	    json.dump(BEDCA_not_perfect_coincidences, outfile, indent = 4)

BEDCA_dict = create_BEDCA_dict(BEDCA_file)
foodex2_dict = create_foodex2_dict(foodex2_file)
foodex2_dict_lemmatized = lemmatize_dict(foodex2_dict)
foodex2_facet_dict = create_foodex2_facet_dict(foodex2_file)

#create_web_service_BEDCA_food("Beer, low alcohol")

"""
BEDCA_dict = create_BEDCA_dict(BEDCA_file)
BEDCA_dict_lemmatized = lemmatize_dict(BEDCA_dict)

foodex2_dict = create_foodex2_dict(foodex2_file)
foodex2_dict_lemmatized = lemmatize_dict(foodex2_dict)

foodex2_facet_dict = create_foodex2_facet_dict(foodex2_file)

BEDCA_perfect_coincidences = {}
BEDCA_not_perfect_coincidences = {}

for code in BEDCA_dict:
	BEDCA_element = BEDCA_dict[code]
	BEDCA_element_lemmatized = BEDCA_dict_lemmatized[code]

	#code = 337                                
	#BEDCA_element = BEDCA_dict[list(BEDCA_dict.keys())[code]]
	#BEDCA_element_lemmatized = BEDCA_dict_lemmatized[list(BEDCA_dict_lemmatized.keys())[code]]
	
	BEDCA_food_object = create_BEDCA_food_object(BEDCA_element, BEDCA_element_lemmatized, foodex2_dict_lemmatized, foodex2_facet_dict)
	
	
	main_term = BEDCA_food_object.get_main_Term()
	flag_term_list_perfect = True
	
	if check_term_coincidence_ratio(main_term):
		term_list = BEDCA_food_object.get_term_list()
		for term_n in term_list:
			if not check_term_coincidence_ratio(term_n):
				flag_term_list_perfect = False
				break
	
	else:
		flag_term_list_perfect = False
	
	if flag_term_list_perfect:
		BEDCA_perfect_coincidences[BEDCA_food_object.get_text()] = BEDCA_food_object.get_BEDCA_food_dict(code)
	else:
		BEDCA_not_perfect_coincidences[BEDCA_food_object.get_text()] = BEDCA_food_object.get_BEDCA_food_dict(code)
	

create_BEDCA_foodex2_matches_json(BEDCA_perfect_coincidences, BEDCA_not_perfect_coincidences)
"""