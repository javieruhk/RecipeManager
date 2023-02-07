from food_terminologies.bedca import BEDCA


def create_BEDCA_obj(food_identifier, cursor):
    cursor.execute('''SELECT   group_id, group_name, food_id, nombre_es, nombre_en, langual_codes, parte_comestible, etanol, energia_total, grasa_total, proteina_total, agua_g, fibra_total, carbohidratos, ag_22_6, ag_monoinsaturados_total, ag_poliinsaturados_total, ag_saturados_total, ag_12_0, ag_14_0, ag_16_0, ag_18_0, ag_18_1, colesterol, ag_18_2, ag_18_3, ag_20_4, ag_20_5, ag_10_0, ag_16_1, ag_20_0, ag_20_1, ag_4_0, ag_6_0, ag_8_0, ag_trans_total, vitamina_a, vitamina_d, vitamina_e, folato, equiv_niacina, riboflavina, tiamina, vitamina_b12, vitamina_b6, vitamina_c, calcio, hierro_total, potasio, magnesio, sodio, fosforo, ioduro, selenio, zinc 
                      FROM     public.bedca
                      WHERE    food_id = '%s';''' % (food_identifier))

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
    grasas = BEDCA.Grasas(ag_22_6, ag_monoinsaturados_total, ag_poliinsaturados_total, ag_saturados_total, ag_12_0,
                          ag_14_0, ag_16_0, ag_18_0, ag_18_1, colesterol, ag_18_2, ag_18_3, ag_20_4, ag_20_5, ag_10_0,
                          ag_16_1, ag_20_0, ag_20_1, ag_4_0, ag_6_0, ag_8_0, ag_trans_total)

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
    vitaminas = BEDCA.Vitaminas(vitamina_a, vitamina_d, vitamina_e, folato, equiv_niacina, riboflavina, tiamina,
                                vitamina_b12, vitamina_b6, vitamina_c)

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