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

stopwords_list = ["type","n/e","unspecified","not specified","i","me","my","myself","we","our","ours","ourselves","you","you're","you've","you'll","you'd","your","yours","yourself","yourselves","he","him","his","himself","she","she's","her","hers","herself","it","it's","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","that'll","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","but","if","because","as","until","while","of","at","by","for","about","against","between","into","through","during","before","after","above","below","to","from","up","down","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","don't","should","should've","now","d","ll","m","o","re","ve","y","ain","aren","aren't","couldn","couldn't","didn","didn't","doesn","doesn't","hadn","hadn't","hasn","hasn't","haven","haven't","isn","isn't","ma","mightn","mightn't","mustn","mustn't","needn","needn't","shan","shan't","shouldn","shouldn't","wasn","wasn't","weren","weren't","won","won't","wouldn","wouldn't"]
conjunction_list = ["without","with","and","or","on","in"]


class BEDCA_food(object):
	def __init__(self, text, main_Term, term_list):
		self.text = text 
		self.main_Term = main_Term 
		self.term_list = term_list

	def __str__(self): 
		print_message = "text: %s \n\nmain_Term: %s \n\nterm_list:" % (self.text, self.main_Term)
		
		if self.term_list == []:
			print_message = print_message + "[]"
		else:
			for term_n in range(0, len(self.term_list)):
				print_message = print_message + "\n    term_%s: %s" % (term_n, self.term_list[term_n])
		return print_message

class Term(object):
	def __init__(self, lema, subterm_list, coincidence_list):
		self.lema = lema 
		self.subterm_list = subterm_list 
		self.coincidence_list = coincidence_list 

	def __str__(self): 
		print_message = "\n        lema: %s\n        subterm_list: " % (self.lema)
		if self.subterm_list == []:
			print_message = print_message + "[]"
		else:
			for subterm_n in range(0, len(self.subterm_list)):
				print_message = print_message + "\n            subterm_%s: %s" % (subterm_n, self.subterm_list[subterm_n])
		
		print_message = print_message + "\n        coincidences: "
		facet_print = ["part_coincidences","ingredient_coincidences","packaging_format_coincidences","process_coincidences"]
		
		for facet_list in range(0, len(self.coincidence_list)):
			print_message = print_message + "\n            %s_coincidences: " % (facet_print[facet_list])

			if self.coincidence_list[facet_list] == []:
				print_message = print_message + "[]"
	
			else:
				print_message = print_message + "%s" % (self.coincidence_list[facet_list][0]) 
		return print_message 

class Subterm(object):
	def __init__(self, conjunction, Term):
		self.conjunction = conjunction 
		self.Term = Term 

	def __str__(self): 
		return "\n                conjunction: %s\n                term: %s" % (self.conjunction, self.Term) 

class Coindicence(object):
	def __init__(self, foodex2_code, foodex2_term, ri, rf):
		self.foodex2_code = foodex2_code
		self.foodex2_term = foodex2_term 
		self.ri = ri 
		self.rf = rf 

	def __str__(self): 
		return "foodex2_code: %s, foodex2_term: %s, ri: %s, rf: %s" % (self.foodex2_code, self.foodex2_term, self.ri, self.rf) 


def create_BEDCA_dict(BEDCA_file):
	BEDCA_data = pd.read_csv(BEDCA_file, sep=';', encoding='windows-1252') 
	BEDCA_df = pd.DataFrame(BEDCA_data)		
	return dict(zip(BEDCA_df['id'], BEDCA_df['nombre_inglés']))

def create_foodex2_dict(foodex2_file):
	foodex2_data = pd.read_excel(foodex2_file, sheet_name="term")
	foodex2_df = pd.DataFrame(foodex2_data)		
	return dict(zip(foodex2_df['termCode'], foodex2_df['termExtendedName']))

def create_foodex2_dict(foodex2_file):
	foodex2_data = pd.read_excel(foodex2_file, sheet_name="term")
	foodex2_df = pd.DataFrame(foodex2_data)		
	return dict(zip(foodex2_df['termCode'], foodex2_df['termExtendedName']))

def create_foodex2_facet_dict(foodex2_file):
	foodex2_data = pd.read_excel(foodex2_file, sheet_name="term")
	foodex2_df = pd.DataFrame(foodex2_data)
	facets_zipped = list(zip(foodex2_df['partParentCode'], foodex2_df['ingredParentCode'], foodex2_df['packformatParentCode'], foodex2_df['processParentCode']))
	return dict(zip(foodex2_df['termCode'], facets_zipped))


def lemmatize_modifier(lemmatizer, stopwords, modifier):
	modifier_tagged = nltk.pos_tag(nltk.regexp_tokenize(modifier, pattern=r"\s|\(|\)|\[.*\]|[.,;'-]|\"", gaps=True))
	modifier_lemas = []

	for (word, tag) in modifier_tagged:
		if word not in stopwords:
			if(tag.startswith('J')):
				lema = lemmatizer.lemmatize(word, wordnet.ADJ)
				modifier_lemas.append(lema.lower())
			elif tag.startswith('V'):
				lema = lemmatizer.lemmatize(word, wordnet.VERB)
				modifier_lemas.append(lema.lower())
			elif tag.startswith('N'):
				lema = lemmatizer.lemmatize(word, wordnet.NOUN)
				modifier_lemas.append(lema.lower())
			elif tag.startswith('R'):
				lema = lemmatizer.lemmatize(word, wordnet.ADV)        
				modifier_lemas.append(lema.lower())
			else:
				lema = lemmatizer.lemmatize(word)
				modifier_lemas.append(lema.lower())
		
	#ver qué hacer con foodex2 ---> Bread and rolls with special ingredients added
	return modifier_lemas

def lemmatize_dict(stopwords, BEDCA_dict):
	lemmatizer = WordNetLemmatizer()
	dict_lemmatized = {}

	#[[oat, grain], [roll], [red]]
	for BEDCA_code in BEDCA_dict:
		food_name = BEDCA_dict[BEDCA_code]
		food_modifiers = food_name.split(", ")
		food_lemas = []

		for modifier in food_modifiers:
			modifier_lemas = lemmatize_modifier(lemmatizer, stopwords, modifier)
			if modifier_lemas != []:
				food_lemas.append(modifier_lemas)
		dict_lemmatized[BEDCA_code] = food_lemas
	
	return dict_lemmatized

def create_BEDCA_foodex2_matches_list(BEDCA_food_lemas_list, foodex2_dict_lemmatized):
	BEDCA_foodex2_matches_list = []
	maximum_matches = 0

	for foodex2_code in foodex2_dict_lemmatized:
		matches = 0

		for foodex2_food_lemas in foodex2_dict_lemmatized[foodex2_code]:
	
			for lema in BEDCA_food_lemas_list:
				if lema in foodex2_food_lemas:
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

#**************#
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
				foodex2_parents_list = get_facet_parents_list(facet_foodex2_code, [], foodex2_facet_dict, 1)
				#print("foodex2_parents_list " + str(foodex2_parents_list))
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

def create_coincidences_list(BEDCA_food_lemas_list, foodex2_dict_lemmatized):
	BEDCA_foodex2_matches_list = create_BEDCA_foodex2_matches_list(BEDCA_food_lemas_list, foodex2_dict_lemmatized)

	BEDCA_foodex2_matches_ratio_dict = create_BEDCA_foodex2_matches_ratio_dict(BEDCA_food_lemas_list, foodex2_dict_lemmatized, BEDCA_foodex2_matches_list)

	foodex2_ratio_dict = filter_BEDCA_foodex2_matches_ratios(BEDCA_foodex2_matches_ratio_dict, 1)
	filtered_BEDCA_foodex2_matches_list = filter_BEDCA_foodex2_matches_ratios(foodex2_ratio_dict, 2)

	foodex2_facet_dict = create_foodex2_facet_dict(foodex2_file)

	BEDCA_foodex2_matches_facet_lists = create_BEDCA_foodex2_matches_facet_lists(filtered_BEDCA_foodex2_matches_list, foodex2_facet_dict)
	
	filtered_BEDCA_foodex2_matches_list = order_BEDCA_foodex2_matches_facet_lists(BEDCA_foodex2_matches_facet_lists, foodex2_facet_dict)
	
	coincidences_list = []

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

def create_term(BEDCA_modifier_lemas, foodex2_dict_lemmatized):
	actual_term_lema = []
	actual_term_subterm_list = []
	actual_term_coincidences = []
	
	subterm_flag = False
	last_lema = 0

	for lema in range(0, len(BEDCA_modifier_lemas)):
		if BEDCA_modifier_lemas[lema] in conjunction_list:
			if subterm_flag:
				new_term_lema = BEDCA_modifier_lemas[last_lema+1:lema]
				new_term_coincidences = create_coincidences_list(new_term_lema, foodex2_dict_lemmatized)
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
					actual_term_coincidences = create_coincidences_list(actual_term_lema, foodex2_dict_lemmatized)

					subterm_flag = True
					last_lema = lema
	
		else:
			if lema == len(BEDCA_modifier_lemas)-1:
				if subterm_flag:
					new_term_lema = BEDCA_modifier_lemas[last_lema+1:]
					new_term_coincidences = create_coincidences_list(new_term_lema, foodex2_dict_lemmatized)
					new_term = Term(new_term_lema, [], new_term_coincidences)

					new_subterm_conjunction = BEDCA_modifier_lemas[last_lema]
					new_subterm = Subterm(new_subterm_conjunction, new_term)

					actual_term_subterm_list.append(new_subterm)
				else:
					actual_term_lema = BEDCA_modifier_lemas
					actual_term_coincidences = create_coincidences_list(BEDCA_modifier_lemas, foodex2_dict_lemmatized)

	actual_term = Term(actual_term_lema, actual_term_subterm_list, actual_term_coincidences)

	return actual_term

def create_BEDCA_food_object(BEDCA_element, BEDCA_element_lemmatized, foodex2_dict_lemmatized):
	main_term = create_term(BEDCA_element_lemmatized[0], foodex2_dict_lemmatized)
	term_list = []

	if len(BEDCA_element_lemmatized) > 1:
		
		for BEDCA_modifier in range(1, len(BEDCA_element_lemmatized)):
			term = create_term(BEDCA_element_lemmatized[BEDCA_modifier], foodex2_dict_lemmatized)
			term_list.append(term)

	BEDCA_food_object = BEDCA_food(BEDCA_element, main_term, term_list)

	return BEDCA_food_object

def create_web_service_BEDCA_food(BEDCA_name):
	BEDCA_dict = create_BEDCA_dict(BEDCA_file)
	BEDCA_dict_lemmatized = lemmatize_dict(stopwords_list, BEDCA_dict)
	code = 87
	#0 multiple facets
	#87 comprobar (sugar, brown)
	#153 multiple childs
	#140
	#74
	BEDCA_element = BEDCA_dict[list(BEDCA_dict.keys())[code]]
	BEDCA_element_lemmatized = BEDCA_dict_lemmatized[list(BEDCA_dict_lemmatized.keys())[code]]
	print(BEDCA_element)

	#BEDCA_code = 0
	#for key, value in BEDCA_dict.items():
	#	if value == BEDCA_name:
	#		BEDCA_code = key
	#print(BEDCA_dict[BEDCA_code])
	#BEDCA_element = BEDCA_dict[BEDCA_code]
	#BEDCA_element_lemmatized = BEDCA_dict_lemmatized[BEDCA_code]
	
	foodex2_dict = create_foodex2_dict(foodex2_file)
	foodex2_dict_lemmatized = lemmatize_dict(stopwords_list, foodex2_dict)
	
	BEDCA_food_object = create_BEDCA_food_object(BEDCA_element, BEDCA_element_lemmatized, foodex2_dict_lemmatized)
	print(BEDCA_food_object)
	return(BEDCA_food_object)

create_web_service_BEDCA_food("")

#BEDCA_food_dict = {}
#for BEDCA_code in BEDCA_dict:
#	BEDCA_food_object = create_BEDCA_food_object(BEDCA_dict[BEDCA_code], BEDCA_dict_lemmatized[BEDCA_code])
#	BEDCA_food_dict[BEDCA_code] = new_BEDCA_food



#cambiar BEDCA por bedca