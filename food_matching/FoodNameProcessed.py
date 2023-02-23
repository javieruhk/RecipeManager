from json import JSONEncoder

class FacetProcessed(object):
    def __init__(self, name_lematized_list, contain_flag, probable_type, facet_n):
        self.name_lematized_list = name_lematized_list
        self.contain_flag = contain_flag
        self.probable_type = probable_type
        self.facet_n = facet_n

    def __str__(self):
        return "name_lematized_list: %s\ncontain_flag: %s\nprobable_type: %s\nfacet_n: %s\n" % (self.name_lematized_list, self.contain_flag, self.probable_type, self.facet_n)

    def get_name_lematized_list(self):
        return self.name_lematized_list

    def get_contain_flag(self):
        return self.facet_n

    def get_probable_type(self):
        return self.probable_type

class FoodNameProcessed(object):
    def __init__(self, facet_processed_list):
        self.facet_processed_list = facet_processed_list

    def __str__(self):
        print_message = ""

        for facet in self.facet_processed_list:
            print_message = print_message + "%s\n" % (facet)

        return print_message

    def get_facet_processed_list(self):
        return self.facet_processed_list

    def from_json_to_food_name_processed_dict(dict_lemmatized_encoded):
        food_name_processed_dict = {}
        
        for code in dict_lemmatized_encoded:
            food_lemmatized = dict_lemmatized_encoded[code]
            facet_processed_list = []
        
            for facet in food_lemmatized["facet_processed_list"]:
                name_lematized_list = facet["name_lematized_list"]
                contain_flag = facet["contain_flag"]
                probable_type = facet["probable_type"]
                facet_n = facet["facet_n"]
                facet_processed = FacetProcessed(name_lematized_list, contain_flag, probable_type, facet_n)
                facet_processed_list.append(facet_processed)
            food_name_processed = FoodNameProcessed(facet_processed_list)
            food_name_processed_dict[code] = food_name_processed
        
        return food_name_processed_dict  

class FoodNameProcessedEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__ 
