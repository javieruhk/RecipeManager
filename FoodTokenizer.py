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
                print_message = print_message + "\n            subterm_%s: %s" % (
                subterm_n, self.subterm_list[subterm_n])

        print_message = print_message + "\n        coincidences: "
        facet_print = ["part", "ingredient", "packaging_format", "process"]

        if self.coincidence_list == []:
            print_message = print_message + "[]"
        else:
            for facet_list in range(0, len(self.coincidence_list)):
                print_message = print_message + "\n            %s_coincidences: " % (facet_print[facet_list])

                if self.coincidence_list[facet_list] == []:
                    print_message = print_message + "[]"

                else:
                    print_message = print_message + "%s" % (self.coincidence_list[facet_list][0])
        return print_message

    def get_lema(self):
        return self.lema

    def get_subterm_list(self):
        return self.subterm_list

    def get_coincidence_list(self):
        return self.coincidence_list

    def get_term_dict(self):
        term_dict = {}
        term_dict["lema"] = self.lema
        if self.subterm_list == []:
            term_dict["subterm list"] = []
        else:
            subterm_dict = {}
            for subterm_n in range(0, len(self.subterm_list)):
                subterm_name = "subterm_%s" % (subterm_n)
                subterm_dict[subterm_name] = self.subterm_list[subterm_n].get_subterm_dict()
            term_dict["subterm list"] = subterm_dict

        coincidence_dict = {}
        facet = ["part coincidences", "ingredient coincidences", "packaging format coincidences",
                 "process coincidences"]
        for coincidence_n in range(0, len(self.coincidence_list)):
            if self.coincidence_list[coincidence_n] != []:
                coincidence_dict[facet[coincidence_n]] = self.coincidence_list[coincidence_n][0].get_coincidence_dict()
        term_dict["coincidences"] = coincidence_dict
        return term_dict


class Subterm(object):
    def __init__(self, conjunction, Term):
        self.conjunction = conjunction
        self.Term = Term

    def __str__(self):
        return "\n                conjunction: %s\n                term: %s" % (self.conjunction, self.Term)

    def get_term(self):
        return self.Term

    def get_subterm_dict(self):
        subterm_dict = {}
        subterm_dict["conjunction"] = self.conjunction
        subterm_dict["term"] = self.Term.get_term_dict()
        return subterm_dict


class Coindicence(object):
    def __init__(self, foodex2_code, foodex2_term, ri, rf):
        self.foodex2_code = foodex2_code
        self.foodex2_term = foodex2_term
        self.ri = ri
        self.rf = rf

    def __str__(self):
        return "foodex2_code: %s, foodex2_term: %s, ri: %s, rf: %s" % (
        self.foodex2_code, self.foodex2_term, self.ri, self.rf)

    def get_ri(self):
        return self.ri

    def get_rf(self):
        return self.rf

    def get_coincidence_dict(self):
        coincidence_dict = {}
        coincidence_dict["foodex2_code"] = self.foodex2_code
        coincidence_dict["foodex2_term"] = self.foodex2_term
        coincidence_dict["ri"] = self.ri
        coincidence_dict["rf"] = self.rf
        return coincidence_dict
