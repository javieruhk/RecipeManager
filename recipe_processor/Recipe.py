class Recipe(object):
    def __init__(self, ingredient_list, step_list):
        self.ingredient_list = ingredient_list
        self.step_list = step_list

    def __str__(self):
        print_message = "INGREDIENTS:\n____________\n\n"
        for ingredient_n in range(0, len(self.ingredient_list)):
            print_message = print_message + "Ingredient_%s:\n%s\n" % (ingredient_n+1, self.ingredient_list[ingredient_n])

        print_message += "STEPS:\n______\n\n"
        
        for step_n in range(0, len(self.step_list)):
            print_message = print_message + "Step_%s:\n       %s\n\n" % (step_n+1, self.step_list[step_n])
        return print_message

    def get_ingredient_list(self):
        return self.ingredient_list

    def set_ingredient_list(self, ingredient_list):
        self.ingredient_list = ingredient_list

    def set_step_list(self, step_list):
        self.step_list = step_list

class Step(object):
    def __init__(self, step_text):
        self.step_text = step_text

class Ingredient(object):
    def __init__(self, food, quantity, unit, physical_quality, process):
        self.food = food
        self.quantity = quantity
        self.unit = unit
        self.physical_quality = physical_quality
        self.process = process

    def __str__(self):
        print_message = "       food:             %s\n       quantity:         %s\n       unit:             %s\n       physical_quality: %s\n       process:          %s\n" % (self.food, self.quantity, self.unit, self.physical_quality, self.process)
        return print_message


    def set_food(self, food):
        self.food = food

    def set_quantity(self, quantity):
        self.quantity = quantity
    
    def set_unit(self, unit):
        self.unit = unit
    
    def set_physical_quality(self, physical_quality):
        self.physical_quality = physical_quality
    
    def set_process(self, process):
        self.process = process

    def get_food(self):
        return self.food

    def get_quantity(self):
        return self.quantity
    
    def get_unit(self):
        return self.unit
    
    def get_physical_quality(self):
        return self.physical_quality
    
    def get_process(self):
        return self.process


