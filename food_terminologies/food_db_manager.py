from food_terminologies.bedca.bedca_db_manager import create_BEDCA_obj
from food_terminologies.foodex2.foodex2_db_manager import create_FoodEx2_obj
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
from food_terminologies.phenolexplorer.phenolexplorer_db_maganer import create_PhenolExplorer_obj

if __name__ == '__main__':
    connection = psycopg2.connect(database="foodnorm", user="postgres", password="ge0graf0!", host="sanger.dia.fi.upm.es", port="5432")
    cursor = connection.cursor()

    ''' TESTs'''
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
