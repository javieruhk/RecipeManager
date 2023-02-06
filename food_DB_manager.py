import FoodEx2, BEDCA, PhenolExplorer
import psycopg2

#def process_tree(node):
#    result_p_t = []
#
#    if type(node) == Tree:
#        for sub_node in node:
#            data, neg_data, _, _, _ = process_tree_node(sub_node, [], [], [], False, 0)
#            if len(data)>0 or len(neg_data)>0:
#                result_p_t.append({'pos': data, 'neg': neg_data})
#    else:
#        data, neg_data, _, _, _ = process_tree_node(node, [], [], [], False, 0)
#        if len(data) > 0 or len(neg_data) > 0:
#            res.append({'pos': data, 'neg': neg_data})
#    return result_p_t

connection = psycopg2.connect(database="postgres", user="postgres", password="csicpass", host="localhost", port="5432")

cursor = connection.cursor()

def create_BEDCA_obj(food_identifier, cursor):
    cursor.execute('''SELECT   group_id, group_name, food_id, nombre_es, nombre_en, langual_codes, parte_comestible, etanol, energia_total, grasa_total, proteina_total, agua_g, fibra_total, carbohidratos, ag_22_6, ag_monoinsaturados_total, ag_poliinsaturados_total, ag_saturados_total, ag_12_0, ag_14_0, ag_16_0, ag_18_0, ag_18_1, colesterol, ag_18_2, ag_18_3, ag_20_4, ag_20_5, ag_10_0, ag_16_1, ag_20_0, ag_20_1, ag_4_0, ag_6_0, ag_8_0, ag_trans_total, vitamina_a, vitamina_d, vitamina_e, folato, equiv_niacina, riboflavina, tiamina, vitamina_b12, vitamina_b6, vitamina_c, calcio, hierro_total, potasio, magnesio, sodio, fosforo, ioduro, selenio, zinc 
                      FROM     public.bedca
                      WHERE    food_id = '%s';''' %(food_identifier))
    
    rows = cursor.fetchall()
    
    row = rows[0]
    
    id_group = row[0]
    group_name = row[1]
    group = BEDCA.Group(id_group, group_name)
    
    id_food = row[2]
    nombre_es = row[3]
    nombre_en = row[4]
    langual_code = row[5]
    edible_part = row[6]
    food = BEDCA.Food(id_food, nombre_es, nombre_en, langual_code, edible_part, group)
    
    etanol = row[7]
    energia_total = row[8]
    grasa_total = row[9]
    proteina_total = row[10]
    agua_g = row[11]
    proximales = BEDCA.Proximales(etanol, energia_total, grasa_total, proteina_total, agua_g)
    
    fibra_total = row[12]
    carbohidratos = row[13]
    hidratos_de_carbono = BEDCA.HidratosDeCarbono(fibra_total, carbohidratos)
    
    ag_22_6 = row[14]
    ag_monoinsaturados_total = row[15]
    ag_poliinsaturados_total = row[16]
    ag_saturados_total = row[17]
    ag_12_0 = row[18]
    ag_14_0 = row[19]
    ag_16_0 = row[20]
    ag_18_0 = row[21]
    ag_18_1 = row[22]
    colesterol = row[23]
    ag_18_2 = row[24]
    ag_18_3 = row[25]
    ag_20_4 = row[26]
    ag_20_5 = row[27]
    ag_10_0 = row[28]
    ag_16_1 = row[29]
    ag_20_0 = row[30]
    ag_20_1 = row[31]
    ag_4_0 = row[32]
    ag_6_0 = row[33]
    ag_8_0 = row[34]
    ag_trans_total = row[35]
    grasas = BEDCA.Grasas(ag_22_6, ag_monoinsaturados_total, ag_poliinsaturados_total, ag_saturados_total, ag_12_0, ag_14_0, ag_16_0, ag_18_0, ag_18_1, colesterol, ag_18_2, ag_18_3, ag_20_4, ag_20_5, ag_10_0, ag_16_1, ag_20_0, ag_20_1, ag_4_0, ag_6_0, ag_8_0, ag_trans_total)
    
    vitamina_a = row[36]
    vitamina_d = row[37]
    vitamina_e = row[38]
    folato = row[39]
    equiv_niacina = row[40]
    riboflavina = row[41]
    tiamina = row[42]
    vitamina_b12 = row[43]
    vitamina_b6 = row[44]
    vitamina_c = row[45]
    vitaminas = BEDCA.Vitaminas(vitamina_a, vitamina_d, vitamina_e, folato, equiv_niacina, riboflavina, tiamina, vitamina_b12, vitamina_b6, vitamina_c)
    
    calcio = row[46]
    hierro_total = row[47]
    potasio = row[48]
    magnesio = row[49]
    sodio = row[50]
    fosforo = row[51]
    ioduro = row[52]
    selenio = row[53]
    zinc = row[54]
    minerales = BEDCA.Minerales(calcio, hierro_total, potasio, magnesio, sodio, fosforo, ioduro, selenio, zinc)
    
    components = BEDCA.Components(proximales, hidratos_de_carbono, grasas, vitaminas, minerales)
    
    nutritional_info = BEDCA.NutritionalInfo(food, components)

    return nutritional_info

def create_FoodEx2_obj(foodex2_code, cursor):
    cursor.execute('''SELECT   part_flag, part_parent_code, part_order, part_reportable, part_hierarchy_code, process_flag, process_parent_code, process_order, process_reportable, process_hierarchy_code, ingred_flag, ingred_parent_code, ingred_order, ingred_reportable, ingred_hierarchy_code, packformat_flag, packformat_parent_code, packformat_order, packformat_reportable, packformat_hierarchy_code, term_code, term_extended_name, scientific_names, all_facets 
                      FROM     public.foodex2_mtx_terms
                      WHERE    term_code = '%s';''' %(foodex2_code))
    
    rows = cursor.fetchall()
    
    row = rows[0]

    part_flag = row[0]
    part_parent_code = row[1]
    part_order = row[2]
    part_reportable = row[3]
    part_hierarchy_code = row[4]
    part_info = FoodEx2.PartInfo(part_flag, part_parent_code, part_order, part_reportable, part_hierarchy_code)
    
    process_flag = row[5]
    process_parent_code = row[6]
    process_order = row[7]
    process_reportable = row[8]
    process_hierarchy_code = row[9]
    process_info = FoodEx2.ProcessInfo(process_flag, process_parent_code, process_order, process_reportable, process_hierarchy_code)

    ingred_flag = row[10]
    ingred_parent_code = row[11]
    ingred_order = row[12]
    ingred_reportable = row[13]
    ingred_hierarchy_code = row[14]
    ingred_info = FoodEx2.IngredInfo(ingred_flag, ingred_parent_code, ingred_order, ingred_reportable, ingred_hierarchy_code)
    
    packformat_flag = row[15]
    packformat_parent_code = row[16]
    packformat_order = row[17]
    packformat_reportable = row[18]
    packformat_hierarchy_code = row[19]
    packformat_info = FoodEx2.PackformatInfo(packformat_flag, packformat_parent_code, packformat_order, packformat_reportable, packformat_hierarchy_code)
    
    term_code = row[20]
    term_extended_name = row[21]
    scientific_names = row[22]
    all_facets = row[23]
    food_info = FoodEx2.FoodInfo(term_code, term_extended_name, scientific_names, all_facets, part_info, process_info, ingred_info, packformat_info)

    return food_info

def create_PhenolExplorer_obj(food_name, cursor):
    cursor.execute('''SELECT   food_group, food_sub_group, food, experimental_method_group, compound_group, compound_sub_group, compound, units, mean, min, max, sd, num, n, publication_ids, pubmed_ids, nb_of_publications
                      FROM     public.phenol_explorer
                      WHERE    food = '%s';''' %(food_name))
    
    rows = cursor.fetchall()
    
    row = rows[1]

    id_food_group = row[0]
    food_group = PhenolExplorer.FoodGroup(id_food_group)
    id_food_sub_group = row[1]
    food_sub_group = PhenolExplorer.FoodSubGroup(id_food_sub_group, food_group)
    id_food = row[2]
    food = PhenolExplorer.Food(id_food, food_sub_group)

    id_experimental_method_group = row[3]
    experimental_method_group = PhenolExplorer.ExperimentalMethodGroup(id_experimental_method_group)
    id_compound_group = row[4]
    compound_group = PhenolExplorer.CompoundGroup(id_compound_group, experimental_method_group)
    id_compound_sub_group = row[5]
    compound_sub_group = PhenolExplorer.CompoundSubGroup(id_compound_sub_group, compound_group)
    id_compound = row[6]
    compound = PhenolExplorer.Compound(id_compound, compound_sub_group)

    units = row[7]
    mean = row[8]
    minimum = row[9]
    maximum = row[10]
    sd = row[11]
    num = row[12]
    n = row[13]
    measurement = PhenolExplorer.Measurement(units, mean, minimum, maximum, sd, num, n)

    ids_publication = row[14].split("; ")
    ids_pubmed = row[15].split("; ")

    publication_list = []
    for id_publication in ids_publication:
        publication = PhenolExplorer.Publication(id_publication)
        publication_list.append(publication)

    pubmed_list = []
    for id_pubmed in ids_pubmed:
        pubmed = PhenolExplorer.Publication(id_pubmed)
        pubmed_list.append(pubmed)

    nb_of_publications = row[16]
    publication_info = PhenolExplorer.PublicationInfo(nb_of_publications, publication_list, pubmed_list)

    measurement_info = PhenolExplorer.MeasurementInfo(food, compound, measurement, publication_info)
    
    return measurement_info

food_identifier = 2450
nutritional_info = create_BEDCA_obj(food_identifier, cursor)
print(nutritional_info)

print("---------------------------------------------------------------------------------------------------")

foodex2_code = "A000D"
food_info = create_FoodEx2_obj(foodex2_code, cursor)
print(food_info)

print("---------------------------------------------------------------------------------------------------")

food_name = "Beer [Regular]"
measurement_info = create_PhenolExplorer_obj(food_name, cursor)
print(measurement_info)



connection.commit()
connection.close()
