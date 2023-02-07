class BEDCATerm(object):
    def __init__(self, text, main_Term, term_list):
        self.text = text
        self.main_Term = main_Term
        self.term_list = term_list


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

    def get_text(self):
        return self.text

    def get_main_Term(self):
        return self.main_Term

    def get_term_list(self):
        return self.term_list

    def get_BEDCA_food_dict(self, code):
        BEDCA_food_dict = {}
        BEDCA_food_dict["BEDCA code"] = code
        BEDCA_food_dict["main term"] = self.main_Term.get_term_dict()
        term_list_dict = {}
        for term_n in range(0, len(self.term_list)):
            term_name = "term_%s" % (term_n)
            term_list_dict[term_name] = self.term_list[term_n].get_term_dict()
        BEDCA_food_dict["term list"] = term_list_dict
        return BEDCA_food_dict
