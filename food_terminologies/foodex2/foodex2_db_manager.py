from food_terminologies.foodex2 import FoodEx2

def create_FoodEx2_obj(foodex2_code, cursor):
    cursor.execute('''SELECT   part_flag, part_parent_code, part_order, part_reportable, part_hierarchy_code, process_flag, process_parent_code, process_order, process_reportable, process_hierarchy_code, ingred_flag, ingred_parent_code, ingred_order, ingred_reportable, ingred_hierarchy_code, packformat_flag, packformat_parent_code, packformat_order, packformat_reportable, packformat_hierarchy_code, term_code, term_extended_name, scientific_names, all_facets 
                          FROM     public.foodex2_mtx_terms
                          WHERE    term_code = '%s';''' % (foodex2_code))

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
    process_info = FoodEx2.ProcessInfo(process_flag, process_parent_code, process_order, process_reportable,
                                       process_hierarchy_code)

    ingred_flag = row[10]
    ingred_parent_code = row[11]
    ingred_order = row[12]
    ingred_reportable = row[13]
    ingred_hierarchy_code = row[14]
    ingred_info = FoodEx2.IngredInfo(ingred_flag, ingred_parent_code, ingred_order, ingred_reportable,
                                     ingred_hierarchy_code)

    packformat_flag = row[15]
    packformat_parent_code = row[16]
    packformat_order = row[17]
    packformat_reportable = row[18]
    packformat_hierarchy_code = row[19]
    packformat_info = FoodEx2.PackformatInfo(packformat_flag, packformat_parent_code, packformat_order,
                                             packformat_reportable, packformat_hierarchy_code)

    term_code = row[20]
    term_extended_name = row[21]
    scientific_names = row[22]
    all_facets = row[23]
    food_info = FoodEx2.FoodInfo(term_code, term_extended_name, scientific_names, all_facets, part_info, process_info,
                                 ingred_info, packformat_info)

    return food_info