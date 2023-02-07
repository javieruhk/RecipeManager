from food_terminologies.FoodTerm import FoodTerm

class FoodGroup(object):
    def __init__(self, id_food_group):
        self.id_food_group = id_food_group

    def __str__(self):
        print_message = "FoodGroup:\n                                                                   id_food_group = %s" % (self.id_food_group)
        return print_message


class FoodSubGroup(object):
    def __init__(self, id_food_sub_group, food_group):
        self.id_food_sub_group = id_food_sub_group
        self.food_group = food_group

    def __str__(self):
        print_message = "FoodSubGroup:\n                                                    id_food_sub_group = %s\n                                                    %s" % (self.id_food_sub_group, self.food_group)
        return print_message


class Food(FoodTerm):
    def __init__(self, id_food, food_sub_group):
        self.food_term = FoodTerm(id_food, None, # Add translation
                            id_food, food_sub_group)

    def __str__(self):
        print_message = "Food:\n                                  id_food = %s\n                                  %s" % (self.food_term.id_food, self.food_term.id_group)
        return print_message


class ExperimentalMethodGroup(object):
    def __init__(self, id_experimental_method_group):
        self.id_experimental_method_group = id_experimental_method_group

    def __str__(self):
        print_message = "ExperimentalMethodGroup:\n                                                                                            id_experimental_method_group = %s" % (self.id_experimental_method_group)
        return print_message


class CompoundGroup(object):
    def __init__(self, id_compound_group, experimental_method_group):
        self.id_compound_group = id_compound_group
        self.experimental_method_group = experimental_method_group

    def __str__(self):
        print_message = "CompoundGroup:\n                                                                   id_compound_group = %s\n                                                                   %s" % (self.id_compound_group, self.experimental_method_group)
        return print_message


class CompoundSubGroup(object):
    def __init__(self, id_compound_sub_group, compound_group):
        self.id_compound_sub_group = id_compound_sub_group
        self.compound_group = compound_group

    def __str__(self):
        print_message = "CompoundSubGroup:\n                                                    id_compound_sub_group = %s\n                                                    %s" % (self.id_compound_sub_group, self.compound_group)
        return print_message


class Compound(object):
    def __init__(self, id_compound, compound_sub_group):
        self.id_compound = id_compound
        self.compound_sub_group = compound_sub_group

    def __str__(self):
        print_message = "Compound:\n                                  id_compound = %s\n                                  %s" % (self.id_compound, self.compound_sub_group)
        return print_message


class Measurement(object):
    def __init__(self, units, mean, minimum, maximum, sd, num, n):
        self.units = units
        self.mean = mean
        self.minimum = minimum
        self.maximum = maximum
        self.sd = sd
        self.num = num
        self.n = n

    def __str__(self):
        print_message = "Measurement:\n                                  units = %s\n                                  mean = %s\n                                  minimum = %s\n                                  maximum = %s\n                                  sd = %s\n                                  num = %s\n                                  n = %s" % (self.units, self.mean, self.minimum, self.maximum, self.sd, self.num, self.n)
        return print_message


class Publication(object):
    def __init__(self, id_publication):
        self.id_publication = id_publication

    def __str__(self):
        print_message = "                                                   " + str(self.id_publication) + "\n"
        return print_message


class PublicationInfo(object):
    def __init__(self, nb_of_publications, publication_list, pubmed_list):
        self.nb_of_publications = nb_of_publications
        self.publication_list = publication_list
        self.pubmed_list = pubmed_list

    def __str__(self):
        print_message = "PublicationInfo:\n                                  nb_of_publications = %s\n                                  PublicationList:\n" % (self.nb_of_publications)
        
        for id_publication in self.publication_list:
            print_message = print_message + str(id_publication)

        print_message = print_message + "                                  PubmedList:\n"

        for id_publication in self.pubmed_list:
            print_message = print_message + str(id_publication)
        
        return print_message


class MeasurementInfo(object):
    def __init__(self, food, compound, measurement, publication_info):
        self.food = food
        self.compound = compound
        self.measurement = measurement
        self.publication_info = publication_info

    def __str__(self):
        print_message = "MeasurementInfo:\n                 %s\n                 %s\n                 %s\n                 %s" % (self.food, self.compound, self.measurement, self.publication_info)
        return print_message