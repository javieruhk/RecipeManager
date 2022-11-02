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
#without
#type
#n/e
#unspecified
#not specified
#
conjunction_list = ["without","with","and","or","on","in"]

def create_foodex2_dict(foodex2_file):
	foodex2_data = pd.read_excel(foodex2_file, sheet_name="term")
	foodex2_df = pd.DataFrame(foodex2_data)		
	return dict(zip(foodex2_df['termCode'], foodex2_df['termExtendedName']))

def create_BEDCA_dict(BEDCA_file):
	BEDCA_data = pd.read_csv(BEDCA_file, sep=';', encoding='windows-1252') 
	BEDCA_df = pd.DataFrame(BEDCA_data)		
	return dict(zip(BEDCA_df['id'], BEDCA_df['nombre_inglés']))

def create_foodex2_dict(foodex2_file):
	foodex2_data = pd.read_excel(foodex2_file, sheet_name="term")
	foodex2_df = pd.DataFrame(foodex2_data)		
	return dict(zip(foodex2_df['termCode'], foodex2_df['termExtendedName']))

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
		
		print_message = print_message + "\n        coincidence_list: " 
		
		if self.coincidence_list == []:
			print_message = print_message + "[]"

		else:
			for coincidence_n in range(0, len(self.coincidence_list)):
				print_message = print_message + "\n            coincidence_%s: %s" % (coincidence_n, self.coincidence_list[coincidence_n]) 
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
		return "foodex2_code: %s, foodex2_term: %s, ri is %s, rf is %s" % (self.foodex2_code, self.foodex2_term, self.ri, self.rf) 

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
	extended_food_name_tagged = nltk.pos_tag(nltk.regexp_tokenize(extended_food_name, pattern=r"\s|\(.*\)|\[.*\]|[.,;'-]|\"", gaps=True))
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
		
	#ver qué hacer con foodex2 ---> Bread and rolls with special ingredients added
	return extended_food_name_lemas

def lemmatize_dict(stopwords, BEDCA_dict):
	lemmatizer = WordNetLemmatizer()
	lemmatized_dict = {}

	#[[oat, grain], [roll], [red]]
	for BEDCA_code in BEDCA_dict:
		extended_food_name = BEDCA_dict[BEDCA_code]
		extended_food_modifiers = extended_food_name.split(", ")
		extended_food_lemas = []

		for modifier in extended_food_modifiers:
			modifier_lemas = lemmatize_food_name(lemmatizer, stopwords, modifier)
			#print(modifier_lemas)
			#si hay una conjunción y tiene un elemento delante dividir en dos listas
			if modifier_lemas != []:
				extended_food_lemas.append(modifier_lemas)
		#print("----------------")
		#print(extended_food_lemas)
		lemmatized_dict[BEDCA_code] = extended_food_lemas
	
	#print(lemmatized_dict)
	return lemmatized_dict

def get_ratio_BEDCA(BEDCA_food_lemas_list, foodex2_food_lemas_list):
	matches_BEDCA = 0
	len_BEDCA = 0
	for facets_BEDCA in BEDCA_food_lemas_list:
		for lema_BEDCA in facets_BEDCA:

			for facets_foodex2 in foodex2_food_lemas_list:
				if lema_BEDCA in facets_foodex2:
					matches_BEDCA = matches_BEDCA + 1

		len_BEDCA = len_BEDCA + len(facets_BEDCA)

	ratio_BEDCA = matches_BEDCA / len_BEDCA
	return ratio_BEDCA

def get_ratio_foodex2(foodex2_food_lemas_list, BEDCA_food_lemas_list):
	matches_foodex2 = 0
	len_foodex2 = 0
	for facets_foodex2 in foodex2_food_lemas_list:
		for lema_foodex2 in facets_foodex2:
			
			for facets_BEDCA in BEDCA_food_lemas_list:
				if lema_foodex2 in facets_BEDCA:
					matches_foodex2 = matches_foodex2 + 1

		len_foodex2 = len_foodex2 + len(facets_foodex2)

	ratio_foodex2 = matches_foodex2 / len_foodex2
	return ratio_foodex2

def calculate_coincidences(BEDCA_food_lemas_list, lemmatized_foodex2_dict):
	BEDCA_foodex2_matches_list = []
	BEDCA_foodex2_matches_code_list = []
	most_matches_n = 0

	for foodex2_code in lemmatized_foodex2_dict:
		matches_n = 0

		for foodex2_lema in lemmatized_foodex2_dict[foodex2_code]:

			for lema in BEDCA_food_lemas_list:
				if lema in foodex2_lema:
					matches_n = matches_n+1

		if matches_n > most_matches_n:
			most_matches_n = matches_n
			BEDCA_foodex2_matches_code_list = [foodex2_code]
		elif matches_n == most_matches_n:
			BEDCA_foodex2_matches_code_list.append(foodex2_code)
##revisar
	for foodex2_code in BEDCA_foodex2_matches_code_list:#calcular las ri y rf
		foodex2_food_lemas_list = lemmatized_foodex2_dict[foodex2_code]
		ratio_BEDCA = get_ratio_BEDCA(BEDCA_food_lemas_list, foodex2_food_lemas_list)
		ratio_foodex2 = get_ratio_foodex2(foodex2_food_lemas_list, BEDCA_food_lemas_list)
		#reducir a los que tengan mejores ratios

		new_coincidence = Coindicence(foodex2_code, foodex2_food_lemas_list, ratio_BEDCA, ratio_foodex2)
		BEDCA_foodex2_matches_list.append(new_coincidence)

	return BEDCA_foodex2_matches_list

def create_term(first_lema, lemmatized_foodex2_dict):
	actual_term_lema = []
	actual_term_subterm_list = []
	actual_term_coincidences = []
	
	subterm = False
	last_n = 0
	for word in range(0, len(first_lema)):
		if first_lema[word] in conjunction_list:
			if subterm:
				new_coincidences = calculate_coincidences(first_lema[last_n+1:word], lemmatized_foodex2_dict)
				new_term = Term(first_lema[last_n+1:word], [], new_coincidences)
				new_subterm = Subterm(first_lema[last_n], new_term)
				actual_term_subterm_list.append(new_subterm)
				last_n = word
			else:
				if word == 0:
					subterm = True
					last_n = word
				else:
					actual_term_lema = first_lema[:word]
					actual_term_coincidences = calculate_coincidences(first_lema[:word], lemmatized_foodex2_dict)
					
					subterm = True
					last_n = word
	
		else:
			if word == len(first_lema)-1:
				if subterm:
					new_coincidences = calculate_coincidences(first_lema[last_n+1:], lemmatized_foodex2_dict)
					new_term = Term(first_lema[last_n+1:], [], new_coincidences)
					new_subterm = Subterm(first_lema[last_n], new_term)
					actual_term_subterm_list.append(new_subterm)
				else:
					actual_term_lema = first_lema
					actual_term_coincidences = calculate_coincidences(first_lema, lemmatized_foodex2_dict)

	actual_term = Term(actual_term_lema, actual_term_subterm_list, actual_term_coincidences)

	return actual_term

def create_BEDCA_food(BEDCA_dict_element, first_element_lemmatized, lemmatized_foodex2_dict):

	main_term = create_term(first_element_lemmatized[0], lemmatized_foodex2_dict)

	term_list = []
	if len(first_element_lemmatized) > 1:
		for lema_group_n in range(1, len(first_element_lemmatized)):
			new_term = create_term(first_element_lemmatized[lema_group_n], lemmatized_foodex2_dict)
			term_list.append(new_term)

	new_BEDCA_food = BEDCA_food(BEDCA_dict_element, main_term, term_list)

	return new_BEDCA_food


BEDCA_dict = create_BEDCA_dict(BEDCA_file)
lemmatized_BEDCA_dict = lemmatize_dict(stopwords_list, BEDCA_dict)

"""
for BEDCA_code in lemmatized_BEDCA_dict:

	main_Term = Term()
	food_entry = BEDCA_food(main_Term, term_list)
"""


code = 147
first_element_text = BEDCA_dict[list(BEDCA_dict.keys())[code]]
first_element_lemmatized = lemmatized_BEDCA_dict[list(lemmatized_BEDCA_dict.keys())[code]]
#print(first_element_text)
#print(first_element_lemmatized)

foodex2_dict = create_foodex2_dict(foodex2_file)
lemmatized_foodex2_dict = lemmatize_dict(stopwords_list, foodex2_dict)

new_BEDCA_food = create_BEDCA_food(first_element_text, first_element_lemmatized, lemmatized_foodex2_dict)
#new_term = create_Term(first_lema)
print(new_BEDCA_food)

#BEDCA_food_dict = {}
#for BEDCA_code in BEDCA_dict:
#	new_BEDCA_food = create_BEDCA_food(BEDCA_dict[BEDCA_code], lemmatized_BEDCA_dict[BEDCA_code])
#	BEDCA_food_dict[BEDCA_code] = new_BEDCA_food