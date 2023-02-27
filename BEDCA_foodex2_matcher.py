import pandas as pd
import nltk
import json
from flair.models import MultiTagger
from flair.data import Sentence
from nltk import Tree
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from operator import is_, xor
from food_matching.FoodTokenizer import Term, Subterm, Coincidence
from food_terminologies.bedca.old_csv.BEDCA import BEDCA_food
from food_matching.FoodNameProcessed import FoodNameProcessed, FacetProcessed, FoodNameProcessedEncoder
from collections import namedtuple

stopwords_list = ["part", "type","n/e","unspecified","not specified","i","me","my","myself","we","our","ours","ourselves","you","you're","you've","you'll","you'd","your","yours","yourself","yourselves","he","him","his","himself","she","she's","her","hers","herself","it","it's","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","that'll","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","but","if","because","as","until","while","of","at","by","for","about","against","between","into","through","during","before","after","above","below","to","from","up","down","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","don't","should","should've","now","d","ll","m","o","re","ve","y","ain","aren","aren't","couldn","couldn't","didn","didn't","doesn","doesn't","hadn","hadn't","hasn","hasn't","haven","haven't","isn","isn't","ma","mightn","mightn't","mustn","mustn't","needn","needn't","shan","shan't","shouldn","shouldn't","wasn","wasn't","weren","weren't","won","won't","wouldn","wouldn't"]
conjunction_list = ["without","with","and","or","on","in"]
negative_conjunction_list = ['without', 'not', 'no', 'non', 'negative', 'free', '-free', 'zero', '0']

input_directory = "./input dbs/"
BEDCA_file = input_directory + "bedca-2.1.csv"
input2_directory = "./prueba/"
foodex2_file = input_directory + "MTX.xls"

lemmatizer = WordNetLemmatizer()
flair_pos_tagger = MultiTagger.load(['pos', 'ner'])

def create_BEDCA_dict(BEDCA_file):
	BEDCA_data = pd.read_csv(BEDCA_file, sep=';', encoding='windows-1252') 
	BEDCA_df = pd.DataFrame(BEDCA_data)		
	return dict(zip(BEDCA_df['id'], BEDCA_df['nombre_inglés']))

def create_foodex2_dict(foodex2_file):
	foodex2_data = pd.read_excel(foodex2_file, sheet_name="term")
	foodex2_df = pd.DataFrame(foodex2_data)		
	return dict(zip(foodex2_df['termCode'], foodex2_df['termExtendedName']))

def parse_conjuctions(node):
	word, category = node
	return word.lower() in negative_conjunction_list # 'nor',

def process_tree(node):
    result_p_t = []
    l0_cum = []
    l0_neg_cum = []
    if type(node) == Tree:
        for sub_node in node:
            data, neg_data, _, _, _, l0_cum, l0_neg_cum = process_tree_node(sub_node, [], [], [], False, 0, l0_cum, l0_neg_cum)
            if len(data) > 0 or len(neg_data) > 0:
                result_p_t.append({'pos': data, 'neg': neg_data})
            #elif len(last_el) >0:
            #    result_p_t.append({'pos': data.append(last_el), 'neg': neg_data})
        if len(l0_cum)>0 or len(l0_neg_cum)>0 :
            result_p_t.append({'pos': l0_cum, 'neg': l0_neg_cum})
    else:
        data, neg_data, _, _, _, l0_cum, l0_neg_cum = process_tree_node(node, [], [], [], False, 0, l0_cum, l0_neg_cum)
        if len(data) > 0 or len(neg_data) > 0:
            result_p_t.append({'pos': data, 'neg': neg_data})
        #elif len(last_el) > 0:
        #    result_p_t.append({'pos': data.append(last_el), 'neg': neg_data})
    return result_p_t


def process_tree_node(node, data, neg_data, cur_el, is_negation, level, l0_cum, l0_neg_cum):
    # simple NP
    if type(node) == tuple:
        word, category = node
        if category in ('PP', 'JJ') or category.startswith('N'): # NN, NPP, NP
            contains_free = False
            if '-free' in word:
                is_negation = not is_negation
                word = word.replace('-free', '')
                cur_el.append(dict(term='free', probable_type='MODIFIER', category='JJ', negating=is_negation))
            elif 'free' in word:
                is_negation = not is_negation
                cur_el.append(dict(term='free', probable_type='MODIFIER', category='JJ', negating=is_negation))
            if not word == '':
                probable_type = 'INGREDIENT'
                if contains_free:
                    category = 'NN_F'
                elif category in ('JJ'):
                    probable_type = 'MODIFIER'
                cur_el.append(dict(term=word, probable_type=probable_type, category=category, negated=is_negation))
        elif category.startswith('V'):
            cur_el.append(dict(term=word, probable_type='METHOD', category=category, negated=is_negation))
        elif category in ('IN', 'RB', 'CD', 'TO'): # TODO: IN -> accumulate to same sentenec or split (with, of)
            is_negation = xor(parse_conjuctions(node), is_negation)
            cur_el.append(dict(term=word, probable_type='MODIFIER', category=category, negating=is_negation))
        else:  # , . DT CC
            is_negation = xor(parse_conjuctions(node), is_negation)

        # acumulate those sentences without NOUNS until ',' OR CC
        if level == 0:
            if len(cur_el) > 0:
                if is_negation:
                    l0_neg_cum += cur_el.copy()
                else:
                    l0_cum += cur_el.copy()
            else:
                if is_negation:
                    neg_data += l0_neg_cum.copy()
                else:
                    data += l0_cum.copy()
                cur_el = []
                l0_cum = []
                l0_neg_cum = []
            is_negation = False

        return data, neg_data, cur_el, is_negation, level, l0_cum, l0_neg_cum
    # subtree NP
    if type(node) == Tree:
        for sub_node in node:
            data_r, neg_data_r, cur_el, is_negation, _, _, _ = process_tree_node(sub_node, data, neg_data, cur_el, is_negation, level + 1, [], [])
        if level == 1 and len(cur_el) > 0:
            if is_negation:
                neg_data_r += cur_el.copy()
            else:
                data_r += cur_el.copy()
            cur_el = []
            is_negation = False

        return data_r, neg_data_r, cur_el, is_negation, level, l0_cum, l0_neg_cum


def create_tree(BEDCA_name):
	modifier_tagged = nltk.regexp_tokenize(BEDCA_name, pattern=r"\s|\(|\)|\[.*\]|[.;-]|\"", gaps=True)
	sentence = " ".join(str(modifier) for modifier in modifier_tagged if modifier not in stopwords_list)

	flair_sentence = Sentence(sentence)
	flair_pos_tagger.predict(flair_sentence)
	flair_tagged_sentence = []
	
	
	if len(flair_sentence.get_labels('pos')) > 0:
		for token in flair_sentence.tokens:
			label = token.get_labels('pos')[0]
			flair_tagged_sentence.append((token.text, label.value))
	
	grammar = r"""
	  NP: {<DT|CD|PRP\$>*<JJ>*<PRP|NN.*|RB>+}          # Chunk sequences of DT, JJ, NN
	  PP: {<IN|TO>+<NP>}               # Chunk prepositions followed by NP   -- RB|    <CC>?<NP>?
	  V: {<VB.*>}
	  CLAUSE: {<NP|V>*<NP|LNP|PP>*}     # Chunk verbs and their arguments  
	  """ # CC ? CLAUSE: {<NP><V|PP>+}           # Chunk NP, VP
	cp = nltk.RegexpParser(grammar)
	
	result = cp.parse(flair_tagged_sentence)
	
	res = process_tree(result)

	#result.draw()
	return res

def lemmatize_modifier(word, tag):
	modifier_lemas = []
	lema = ""

	if word not in stopwords_list:
		if(tag.startswith('J')):
			lema = lemmatizer.lemmatize(word.lower(), wordnet.ADJ)
		elif tag.startswith('V'):
			lema = lemmatizer.lemmatize(word.lower(), wordnet.VERB)
		elif tag.startswith('N'):
			lema = lemmatizer.lemmatize(word.lower(), wordnet.NOUN)
		elif tag.startswith('R'):
			lema = lemmatizer.lemmatize(word.lower(), wordnet.ADV)        
		else:
			lema = lemmatizer.lemmatize(word.lower())
		
	return lema

def lemmatize_dict(dictionary):
	dict_lemmatized = {}
	BEDCA_list_keys = list(dictionary.keys())

	#[[oat, grain], [roll], [red]]
	#for BEDCA_code in range(0, len(BEDCA_list_keys)):
	for BEDCA_code in range(0, 3):
		BEDCA_name = dictionary[BEDCA_list_keys[BEDCA_code]]
		name_lemmatized = lemmatize_name(BEDCA_name)

		dict_lemmatized[BEDCA_list_keys[BEDCA_code]] = name_lemmatized

	return dict_lemmatized

def create_foodex2_facet_dict(foodex2_file):
	foodex2_data = pd.read_excel(foodex2_file, sheet_name="term")
	foodex2_df = pd.DataFrame(foodex2_data)
	facets_zipped = list(zip(foodex2_df['partParentCode'], foodex2_df['ingredParentCode'], foodex2_df['packformatParentCode'], foodex2_df['processParentCode']))
	return dict(zip(foodex2_df['termCode'], facets_zipped))

def lemmatize_name(BEDCA_name):
	name_tree = create_tree(BEDCA_name) 
	#print(name_tree)

	facet_processed_list = []
	#modifiers = []
	facet_n = 1

	for modifier in name_tree:
		for sign in modifier:
			for mod in modifier[sign]:
				modifier_lemas = []
				positive = True
				probable_type = ""
				for pos in mod:
					lema = lemmatize_modifier(pos["term"], pos["category"])
					if lema != "":
						modifier_lemas.append(lema)
						aux_type = pos["probable_type"]
						probable_type = aux_type
						
				positive = not pos["negated"]
				#modifiers.append((modifier_lemas, positive, probable_type)) 
				facet_processed_list.append(FacetProcessed(modifier_lemas, positive, probable_type, facet_n))
				facet_n = facet_n+1

	food_name_processed = FoodNameProcessed(facet_processed_list)
	#print(modifiers)
	return food_name_processed

def create_BEDCA_foodex2_matches_list(BEDCA_food_lemas_list, foodex2_dict_lemmatized):
	BEDCA_foodex2_matches_list = []
	maximum_matches = 0

	for foodex2_code in foodex2_dict_lemmatized:
		matches = 0

		for lema in BEDCA_food_lemas_list:
			facet_processed_list = foodex2_dict_lemmatized[foodex2_code].get_facet_processed_list()
			for foodex2_food_lemas in facet_processed_list:
				if lema in foodex2_food_lemas.get_name_lematized_list():
					matches = matches+1
					break#si no puede contar el mismo match dos veces 

		matches = matches+1

		if matches > maximum_matches:
			maximum_matches = matches
			BEDCA_foodex2_matches_list = [foodex2_code]
		elif matches == maximum_matches and maximum_matches != 0:
			BEDCA_foodex2_matches_list.append(foodex2_code)

	return BEDCA_foodex2_matches_list

def filter_contains_modifier_BEDCA_foodex2_matches_list(BEDCA_food_lemas_list, BEDCA_foodex2_matches_list, foodex2_dict_lemmatized, contains_modifier_flag):
	matches_list = []

	for BEDCA_lema in BEDCA_food_lemas_list:
		for foodex2_code in BEDCA_foodex2_matches_list:
			add_element = False
			foodex2_element = foodex2_dict_lemmatized[foodex2_code].get_facet_processed_list()

			for foodex2_name in foodex2_element:
				lema = foodex2_name.get_name_lematized_list()

				if BEDCA_lema in lema: 
					if contains_modifier_flag == foodex2_name.get_contain_flag():
						add_element = True

			if add_element and not foodex2_code in matches_list:
				matches_list.append(foodex2_code)

	return matches_list

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
		foodex2_food_lemas_list = []
		facet_processed_list = foodex2_dict_lemmatized[foodex2_code].get_facet_processed_list()
		for lema in range(0, len(facet_processed_list)):
			foodex2_food_lemas_list.append(facet_processed_list[lema].get_name_lematized_list())
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

def create_coincidences_list(BEDCA_food_lemas_list, foodex2_dict_lemmatized, foodex2_facet_dict, probable_facet, contains_modifier_flag):
	BEDCA_foodex2_matches_list = create_BEDCA_foodex2_matches_list(BEDCA_food_lemas_list, foodex2_dict_lemmatized)

	BEDCA_foodex2_matches_list = filter_contains_modifier_BEDCA_foodex2_matches_list(BEDCA_food_lemas_list, BEDCA_foodex2_matches_list, foodex2_dict_lemmatized, contains_modifier_flag)

	BEDCA_foodex2_matches_ratio_dict = create_BEDCA_foodex2_matches_ratio_dict(BEDCA_food_lemas_list, foodex2_dict_lemmatized, BEDCA_foodex2_matches_list)

	foodex2_ratio_dict = filter_BEDCA_foodex2_matches_ratios(BEDCA_foodex2_matches_ratio_dict, 1)
	filtered_BEDCA_foodex2_matches_list = filter_BEDCA_foodex2_matches_ratios(foodex2_ratio_dict, 2)

	BEDCA_foodex2_matches_facet_lists = create_BEDCA_foodex2_matches_facet_lists(filtered_BEDCA_foodex2_matches_list, foodex2_facet_dict)

	while BEDCA_foodex2_matches_facet_lists == [[],[],[],[]] and foodex2_ratio_dict != {}:
		for foodex2_code in filtered_BEDCA_foodex2_matches_list:
			foodex2_ratio_dict.pop(foodex2_code)
	
		filtered_BEDCA_foodex2_matches_list = filter_BEDCA_foodex2_matches_ratios(foodex2_ratio_dict, 2)

		BEDCA_foodex2_matches_facet_lists = create_BEDCA_foodex2_matches_facet_lists(filtered_BEDCA_foodex2_matches_list, foodex2_facet_dict)

	coincidences_list = []
	
	if BEDCA_foodex2_matches_facet_lists != [[],[],[],[]]:
		filtered_BEDCA_foodex2_matches_list = order_BEDCA_foodex2_matches_facet_lists(BEDCA_foodex2_matches_facet_lists, foodex2_facet_dict)

		if probable_facet == "INGREDIENT" and filtered_BEDCA_foodex2_matches_list[1] != []:
			filtered_BEDCA_foodex2_matches_list = [[], filtered_BEDCA_foodex2_matches_list[1], [], []]
		elif probable_facet == "METHOD" and filtered_BEDCA_foodex2_matches_list[3] != []:
			filtered_BEDCA_foodex2_matches_list = [[], [], [], filtered_BEDCA_foodex2_matches_list[3]]
		
		for facet_BEDCA_foodex2_matches_list in filtered_BEDCA_foodex2_matches_list:
			facet_coincidences_list = []
	
			if facet_BEDCA_foodex2_matches_list != []:
				for code in range(0, len(facet_BEDCA_foodex2_matches_list)):
					foodex2_code = facet_BEDCA_foodex2_matches_list[code]
					foodex2_food_lemas_list = BEDCA_foodex2_matches_ratio_dict[foodex2_code][0]
					BEDCA_ratio = BEDCA_foodex2_matches_ratio_dict[foodex2_code][1]
					ratio_foodex2 = BEDCA_foodex2_matches_ratio_dict[foodex2_code][2]
			
					new_coincidence = Coincidence(foodex2_code, foodex2_food_lemas_list, BEDCA_ratio, ratio_foodex2)
					facet_coincidences_list.append(new_coincidence)
			coincidences_list.append(facet_coincidences_list)

	return coincidences_list

def create_term(BEDCA_modifier_lemas_structure, foodex2_dict_lemmatized, foodex2_facet_dict, contains_modifier_flag):
	actual_term_lema = []
	actual_term_subterm_list = []
	actual_term_coincidences = []
	
	subterm_flag = False
	last_lema = 0

	BEDCA_modifier_lemas = BEDCA_modifier_lemas_structure.get_name_lematized_list()
	probable_type = BEDCA_modifier_lemas_structure.get_probable_type()

	for lema in range(0, len(BEDCA_modifier_lemas)):
		if BEDCA_modifier_lemas[lema] in conjunction_list:
			if subterm_flag:
				new_term_lema = BEDCA_modifier_lemas[last_lema+1:lema]
				new_term_coincidences = create_coincidences_list(new_term_lema, foodex2_dict_lemmatized, foodex2_facet_dict, probable_type, contains_modifier_flag)
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
					actual_term_coincidences = create_coincidences_list(actual_term_lema, foodex2_dict_lemmatized, foodex2_facet_dict, probable_type, contains_modifier_flag)

					subterm_flag = True
					last_lema = lema
	
		else:
			if lema == len(BEDCA_modifier_lemas)-1:
				if subterm_flag:
					new_term_lema = BEDCA_modifier_lemas[last_lema+1:]
					new_term_coincidences = create_coincidences_list(new_term_lema, foodex2_dict_lemmatized, foodex2_facet_dict, probable_type, contains_modifier_flag)
					new_term = Term(new_term_lema, [], new_term_coincidences)

					new_subterm_conjunction = BEDCA_modifier_lemas[last_lema]
					new_subterm = Subterm(new_subterm_conjunction, new_term)

					actual_term_subterm_list.append(new_subterm)
				else:
					actual_term_lema = BEDCA_modifier_lemas
					actual_term_coincidences = create_coincidences_list(BEDCA_modifier_lemas, foodex2_dict_lemmatized, foodex2_facet_dict, probable_type, contains_modifier_flag)

	actual_term = Term(actual_term_lema, actual_term_subterm_list, actual_term_coincidences)

	return actual_term

def create_BEDCA_food_object(BEDCA_element, BEDCA_element_lemmatized, foodex2_dict_lemmatized, foodex2_facet_dict):
	facet_processed = BEDCA_element_lemmatized.get_facet_processed_list()[0]

	contain_flag = facet_processed.get_contain_flag()
	main_term = create_term(facet_processed, foodex2_dict_lemmatized, foodex2_facet_dict, contain_flag)
	term_list = []

	facets_list_processed = BEDCA_element_lemmatized.get_facet_processed_list()

	if len(facets_list_processed) > 1:
		
		for BEDCA_modifier in range(1, len(facets_list_processed)):
			facet_processed = facets_list_processed[BEDCA_modifier]
			contain_flag = facet_processed.get_contain_flag()
			term = create_term(facet_processed, foodex2_dict_lemmatized, foodex2_facet_dict, contain_flag)
			term_list.append(term)

	BEDCA_food_object = BEDCA_food(BEDCA_element, main_term, term_list)

	return BEDCA_food_object

def create_web_service_BEDCA_food(BEDCA_code):
	BEDCA_element = BEDCA_dict[BEDCA_code]
	BEDCA_element_lemmatized = lemmatize_name(BEDCA_element)

	BEDCA_food_object = []
	BEDCA_food_object = create_BEDCA_food_object(BEDCA_element, BEDCA_element_lemmatized, foodex2_dict_lemmatized, foodex2_facet_dict)

	return(BEDCA_food_object)

#---------------------------------------------------------------------------------------------------

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
	with open("./output json files/perfect_matches_1.json", "w") as outfile:
		json.dump(BEDCA_perfect_coincidences, outfile, indent = 4)

	with open("./output json files/not_perfect_matches_1.json", "w") as outfile:
		json.dump(BEDCA_not_perfect_coincidences, outfile, indent = 4)

def create_BEDCA_foodex2_matches(BEDCA_dict, BEDCA_dict_lemmatized, foodex2_dict_lemmatized, foodex2_facet_dict):
	BEDCA_perfect_coincidences = {}
	BEDCA_not_perfect_coincidences = {}
	
	for code in BEDCA_dict:
	
		BEDCA_element = BEDCA_dict[code]
		BEDCA_element_lemmatized = BEDCA_dict_lemmatized[str(code)]	
		
		if BEDCA_element_lemmatized != []:
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
BEDCA_dict = create_BEDCA_dict(BEDCA_file)
#BEDCA_dict_lemmatized = {}
#BEDCA_dict_lemmatized = lemmatize_dict(BEDCA_dict)

#with open("./output json files/BEDCA_dict_lemmatized_objects.json", "w") as outfile:
#	json.dump(BEDCA_dict_lemmatized, outfile, indent = 4, cls = FoodNameProcessedEncoder)

with open("./output json files/BEDCA_dict_lemmatized_objects.json") as json_file:
	BEDCA_dict_lemmatized_encoded = json.load(json_file)

BEDCA_dict_lemmatized = FoodNameProcessed.from_json_to_food_name_processed_dict(BEDCA_dict_lemmatized_encoded)


foodex2_dict = create_foodex2_dict(foodex2_file)
foodex2_dict_lemmatized = {}
#foodex2_dict_lemmatized = lemmatize_dict(foodex2_dict)

#with open("./output json files/foodex2_dict_lemmatized_objects.json", "w") as outfile:
#	json.dump(foodex2_dict_lemmatized, outfile, indent = 4, cls = FoodNameProcessedEncoder)

with open("./output json files/foodex2_dict_lemmatized_objects.json") as json_file:
	foodex2_dict_lemmatized_encoded = json.load(json_file)

foodex2_dict_lemmatized = FoodNameProcessed.from_json_to_food_name_processed_dict(foodex2_dict_lemmatized_encoded)


foodex2_facet_dict = create_foodex2_facet_dict(foodex2_file)

create_BEDCA_foodex2_matches(BEDCA_dict, BEDCA_dict_lemmatized, foodex2_dict_lemmatized, foodex2_facet_dict)
"""