from food_terminologies.FoodTerm import FoodTerm


class PartInfo(object):
    def __init__(self, part_flag, part_parent_code, part_order, part_reportable, part_hierarchy_code):
        self.part_flag = part_flag
        self.part_parent_code = part_parent_code
        self.part_order = part_order
        self.part_reportable = part_reportable
        self.part_hierarchy_code = part_hierarchy_code

    def __str__(self):
        print_message = "PartInfo:\n                          part_flag = %s\n                          part_parent_code = %s\n                          part_order = %s\n                          part_reportable = %s\n                          part_hierarchy_code = %s" % (self.part_flag, self.part_parent_code, self.part_order, self.part_reportable, self.part_hierarchy_code)
        return print_message

class ProcessInfo(object):
    def __init__(self, process_flag, process_parent_code, process_order, process_reportable, process_hierarchy_code):
        self.process_flag = process_flag
        self.process_parent_code = process_parent_code
        self.process_order = process_order
        self.process_reportable = process_reportable
        self.process_hierarchy_code = process_hierarchy_code

    def __str__(self):
        print_message = "ProcessInfo:\n                          process_flag = %s\n                          process_parent_code = %s\n                          process_order = %s\n                          process_reportable = %s\n                          process_hierarchy_code = %s" % (self.process_flag, self.process_parent_code, self.process_order, self.process_reportable, self.process_hierarchy_code)
        return print_message

class IngredInfo(object):
    def __init__(self, ingred_flag, ingred_parent_code, ingred_order, ingred_reportable, ingred_hierarchy_code):
        self.ingred_flag = ingred_flag
        self.ingred_parent_code = ingred_parent_code
        self.ingred_order = ingred_order
        self.ingred_reportable = ingred_reportable
        self.ingred_hierarchy_code = ingred_hierarchy_code

    def __str__(self):
        print_message = "IngredInfo:\n                          ingred_flag = %s\n                          ingred_parent_code = %s\n                          ingred_order = %s\n                          ingred_reportable = %s\n                          ingred_hierarchy_code = %s" % (self.ingred_flag, self.ingred_parent_code, self.ingred_order, self.ingred_reportable, self.ingred_hierarchy_code)
        return print_message

class PackformatInfo(object):
    def __init__(self, packformat_flag, packformat_parent_code, packformat_order, packformat_reportable, packformat_hierarchy_code):
        self.packformat_flag = packformat_flag
        self.packformat_parent_code = packformat_parent_code
        self.packformat_order = packformat_order
        self.packformat_reportable = packformat_reportable
        self.packformat_hierarchy_code = packformat_hierarchy_code

    def __str__(self):
        print_message = "PackformatInfo:\n                          packformat_flag = %s\n                          packformat_parent_code = %s\n                          packformat_order = %s\n                          packformat_reportable = %s\n                          packformat_hierarchy_code = %s" % (self.packformat_flag, self.packformat_parent_code, self.packformat_order, self.packformat_reportable, self.packformat_hierarchy_code)
        return print_message


class FoodInfo(FoodTerm):
    def __init__(self, term_code, term_extended_name, scientific_names, all_facets, part_info, process_info, ingred_info, packformat_info):
        self.food_term = FoodTerm(term_code, None, # add translation
            term_extended_name, None # add category/group
            )
        self.scientific_names = scientific_names
        self.all_facets = all_facets
        self.part_info = part_info
        self.process_info = process_info
        self.ingred_info = ingred_info
        self.packformat_info = packformat_info

    def __str__(self):
        print_message = "FoodInfo:\n          term_code = %s\n          term_extended_name = %s\n          scientific_names = %s\n          all_facets = %s\n          %s\n          %s\n          %s\n          %s" % (self.food_term.id_food, self.food_term.name_en, self.scientific_names, self.all_facets, self.part_info, self.process_info, self.ingred_info, self.packformat_info)
        return print_message
    