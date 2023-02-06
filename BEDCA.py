class Group(object):
    def __init__(self, id_group, group_name):
        self.id_group = id_group
        self.group_name = group_name

    def __str__(self):
        print_message = "Group:\n                                                 id_group = %s\n                                                 group_name = %s" % (self.id_group, self.group_name)
        return print_message

class Food(object):
    def __init__(self, id_food, nombre_es, nombre_en, langual_code, edible_part, group):
        self.id_food = id_food
        self.nombre_es = nombre_es
        self.nombre_en = nombre_en
        self.langual_code = langual_code
        self.edible_part = edible_part
        self.group = group
  
    def __str__(self):
        print_message = "Food:\n                              id_food = %s\n                              nombre_es = %s\n                              nombre_en = %s\n                              langual_code = %s\n                              edible_part = %s\n                              %s" % (self.id_food, self.nombre_es, self.nombre_en, self.langual_code, self.edible_part, self.group)
        return print_message

class Proximales(object):
    def __init__(self, etanol, energia_total, grasa_total, proteina_total, agua_g):
        self.etanol = etanol
        self.energia_total = energia_total 
        self.grasa_total = grasa_total 
        self.proteina_total = proteina_total 
        self.agua_g = agua_g

    def __str__(self):
        print_message = "Proximales:\n                                                 etanol = %s\n                                                 energia_total = %s\n                                                 grasa_total = %s\n                                                 proteina_total = %s\n                                                 agua_g = %s" % (self.etanol, self.energia_total, self.grasa_total, self.proteina_total, self.agua_g)
        return print_message

class HidratosDeCarbono(object):
    def __init__(self, fibra_total, carbohidratos):
        self.fibra_total = fibra_total
        self.carbohidratos = carbohidratos 

    def __str__(self):
        print_message = "HidratosDeCarbono:\n                                                 fibra_total = %s\n                                                 carbohidratos = %s" % (self.fibra_total, self.carbohidratos)
        return print_message

class Grasas(object):
    def __init__(self, ag_22_6, ag_monoinsaturados_total, ag_poliinsaturados_total, ag_saturados_total, ag_12_0, ag_14_0, ag_16_0, ag_18_0, ag_18_1, colesterol, ag_18_2, ag_18_3, ag_20_4, ag_20_5, ag_10_0, ag_16_1, ag_20_0, ag_20_1, ag_4_0, ag_6_0, ag_8_0, ag_trans_total):
        self.ag_22_6 = ag_22_6
        self.ag_monoinsaturados_total = ag_monoinsaturados_total 
        self.ag_poliinsaturados_total = ag_poliinsaturados_total 
        self.ag_saturados_total = ag_saturados_total 
        self.ag_12_0 = ag_12_0
        self.ag_14_0 = ag_14_0
        self.ag_16_0 = ag_16_0 
        self.ag_18_0 = ag_18_0 
        self.ag_18_1 = ag_18_1 
        self.colesterol = colesterol
        self.ag_18_2 = ag_18_2
        self.ag_18_3 = ag_18_3 
        self.ag_20_4 = ag_20_4 
        self.ag_20_5 = ag_20_5
        self.ag_10_0 = ag_10_0
        self.ag_16_1 = ag_16_1
        self.ag_20_0 = ag_20_0
        self.ag_20_1 = ag_20_1
        self.ag_4_0 = ag_4_0
        self.ag_6_0 = ag_6_0
        self.ag_8_0 = ag_8_0
        self.ag_trans_total = ag_trans_total
    
    def __str__(self):
        print_message = "Grasas:\n                                                 ag_22_6 = %s\n                                                 ag_monoinsaturados_total = %s\n                                                 ag_poliinsaturados_total = %s\n                                                 ag_saturados_total = %s\n                                                 ag_12_0 = %s\n                                                 ag_14_0 = %s\n                                                 ag_16_0 = %s\n                                                 ag_18_0 = %s\n                                                 ag_18_1 = %s\n                                                 colesterol = %s\n                                                 ag_18_2 = %s\n                                                 ag_18_3 = %s\n                                                 ag_20_4 = %s\n                                                 ag_20_5 = %s\n                                                 ag_10_0 = %s\n                                                 ag_16_1 = %s\n                                                 ag_20_0 = %s\n                                                 ag_20_1 = %s\n                                                 ag_4_0 = %s\n                                                 ag_6_0 = %s\n                                                 ag_8_0 = %s\n                                                 ag_trans_total = %s" % (self.ag_22_6, self.ag_monoinsaturados_total, self.ag_poliinsaturados_total, self.ag_saturados_total, self.ag_12_0, self.ag_14_0, self.ag_16_0, self.ag_18_0, self.ag_18_1, self.colesterol, self.ag_18_2, self.ag_18_3, self.ag_20_4, self.ag_20_5, self.ag_10_0, self.ag_16_1, self.ag_20_0, self.ag_20_1, self.ag_4_0, self.ag_6_0, self.ag_8_0, self.ag_trans_total)
        return print_message


class Vitaminas(object):
    def __init__(self, vitamina_a, vitamina_d, vitamina_e, folato, equiv_niacina, riboflavina, tiamina, vitamina_b12, vitamina_b6, vitamina_c):
        self.vitamina_a = vitamina_a
        self.vitamina_d = vitamina_d
        self.vitamina_e = vitamina_e
        self.folato = folato
        self.equiv_niacina = equiv_niacina
        self.riboflavina = riboflavina
        self.tiamina = tiamina
        self.vitamina_b12 = vitamina_b12
        self.vitamina_b6 = vitamina_b6
        self.vitamina_c = vitamina_c
    
    def __str__(self):
        print_message = "Vitaminas:\n                                                 vitamina_a = %s\n                                                 vitamina_d = %s\n                                                 vitamina_e = %s\n                                                 folato = %s\n                                                 equiv_niacina = %s\n                                                 riboflavina = %s\n                                                 tiamina = %s\n                                                 vitamina_b12 = %s\n                                                 vitamina_b6 = %s\n                                                 vitamina_c = %s" % (self.vitamina_a, self.vitamina_d, self.vitamina_e, self.folato, self.equiv_niacina, self.riboflavina, self.tiamina, self.vitamina_b12, self.vitamina_b6, self.vitamina_c)
        return print_message

class Minerales(object):
    def __init__(self, calcio, hierro_total, potasio, magnesio, sodio, fosforo, ioduro, selenio, zinc):
        self.calcio = calcio
        self.hierro_total = hierro_total 
        self.potasio = potasio 
        self.magnesio = magnesio 
        self.sodio = sodio
        self.fosforo = fosforo
        self.ioduro = ioduro 
        self.selenio = selenio 
        self.zinc = zinc 

    def __str__(self):
        print_message = "Minerales:\n                                                 calcio = %s\n                                                 hierro_total = %s\n                                                 potasio = %s\n                                                 magnesio = %s\n                                                 sodio = %s\n                                                 fosforo = %s\n                                                 ioduro = %s\n                                                 selenio = %s\n                                                 zinc = %s" % (self.calcio, self.hierro_total, self.potasio, self.magnesio, self.sodio, self.fosforo, self.ioduro, self.selenio, self.zinc)
        return print_message

class Components(object):
    def __init__(self, proximales, hidratos_de_carbono, grasas, vitaminas, minerales):
        self.proximales = proximales
        self.hidratos_de_carbono = hidratos_de_carbono 
        self.grasas = grasas 
        self.vitaminas = vitaminas 
        self.minerales = minerales

    def __str__(self):
        print_message = "Components:\n                              %s\n                              %s\n                              %s\n                              %s\n                              %s" % (self.proximales, self.hidratos_de_carbono, self.grasas, self.vitaminas, self.minerales)
        return print_message

class NutritionalInfo(object):
    def __init__(self, food, components):
        self.food = food
        self.components = components

    def __str__(self):
        print_message = "NutritionalInfo:\n                 %s\n                 %s" % (self.food, self.components)
        return print_message



"""
SIN CLASIFICACIÓN:

agua_mg
luteina
luteina_y_zeaxantina
licopeno
sacarosa
lactosa
maltosa
caroteno
carotenoides
alfa_caroteno
beta_caroteno
equiv_beta_caroteno
colecalciferol
retinol
acidos_organicos_total
zeaxantina
cloruro
hierro_no_hemo
fructosa
glucosa
proteina_animal
proteina_vegetal
almidon_total
brassicasterol
campesterol
sitosterol
estigmasterol
azucares_totales
cobre
manganeso
niquel
biotina
biotina_u
beta_criptoxantina
niacina
acido_pantoteico
piridoxina
acido_folico
"""