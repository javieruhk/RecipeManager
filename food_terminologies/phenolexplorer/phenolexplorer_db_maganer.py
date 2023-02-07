from food_terminologies.phenolexplorer import PhenolExplorer


def create_PhenolExplorer_obj(food_name, cursor):
    cursor.execute('''SELECT   food_group, food_sub_group, food, experimental_method_group, compound_group, compound_sub_group, compound, units, mean, min, max, sd, num, n, publication_ids, pubmed_ids, nb_of_publications
                      FROM     public.phenol_explorer
                      WHERE    food = '%s';''' % (food_name))

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