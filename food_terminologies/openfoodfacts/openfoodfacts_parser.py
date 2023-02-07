import gzip
import json
import time


class Ingredient:
    def __init__(self, dict):
        self.id = dict['id']
        self.percent_estimate = dict['percent_estimate']
        self.percent_max = dict.get('percent_max')
        self.percent_min = dict.get('percent_min')
        self.text = dict['text']
        if 'vegetarian' in dict:
            self.vegetarian = dict['vegetarian']
        if 'vegan' in dict:
            self.vegan = dict['vegan']
        self.ingredients = []
        if 'ingredients' in dict:
            for ingredient in dict['ingredients']:
                self.ingredients.append(Ingredient(ingredient))


class Nutriments:
    def __init__(self, dict):
        self.sodium = dict.get('sodium')
        self.sodium_value = dict.get('sodium_value')
        self.sodium_unit = dict.get('sodium_unit')
        self.sodium_100g = dict.get('sodium_100g')
        self.salt = dict.get('salt')
        self.salt_value = dict.get('salt_value')
        self.salt_unit = dict.get('salt_unit')
        self.salt_100g = dict.get('salt_100g')

        self.sugars = dict.get('sugars')
        self.sugars_value = dict.get('sugars_value')
        self.sugars_unit = dict.get('sugars_unit')
        self.sugars_100g = dict.get('sugars_100g')

        self.fat = dict.get('fat')
        self.fat_value = dict.get('fat_value')
        self.fat_unit = dict.get('fat_unit')
        self.fat_100g = dict.get('fat_100g')
        self.saturated_fat = dict.get('saturated-fat')
        self.saturated_fat_value = dict.get('saturated_fat_value')
        self.saturated_fat_unit = dict.get('saturated-fat_unit')
        self.saturated_fat_100g = dict.get('saturated-fat_100g')

        self.proteins = dict.get('proteins')
        self.proteins_value = dict.get('proteins_value')
        self.proteins_unit = dict.get('proteins_unit')
        self.proteins_100g = dict.get('proteins_100g')

        self.carbohydrates = dict.get('carbohydrates')
        self.carbohydrates_value = dict.get('carbohydrates_value')
        self.carbohydrates_unit = dict.get('carbohydrates_unit')
        self.carbohydrates_100g = dict.get('carbohydrates_100g')

        self.energy_value = dict.get('energy_value')
        self.energy_unit = dict.get('energy_unit')
        self.energy_100g = dict.get('energy_100g')
        self.energy_kcal = dict.get('energy_kcal')
        self.energy_kcal_value = dict.get('energy-kcal_value')
        self.energy_kcal_unit = dict.get('energy-kcal_unit')
        self.energy_kcal_100g = dict.get('energy_kcal_100g')

        self.fruits_vegetables_nuts_estimate_from_ingredients_100g = dict.get('fruits-vegetables-nuts-estimate-from-ingredients_100g')
        self.fruits_vegetables_nuts_estimate_from_ingredients_serving = dict.get('fruits-vegetables-nuts-estimate-from-ingredients_serving')


class Nutriscore:
    def __init__(self, dict):
        self.sodium = dict.get('sodium')
        self.sodium_value = dict.get('sodium_value')
        self.sodium_points = dict.get('sodium_points')

        self.proteins = dict.get('proteins')
        self.proteins_value = dict.get('proteins_value')
        self.proteins_points = dict.get('proteins_points')

        self.fiber = dict.get('fiber')
        self.fiber_value = dict.get('fiber_value')
        self.fiber_points = dict.get('fiber_points')

        self.sugars = dict.get('sugars')
        self.sugars_value = dict.get('sugars_value')
        self.sugars_points = dict.get('sugars_points')

        self.energy = dict.get('energy')
        self.energy_value = dict.get('energy_value')
        self.energy_points = dict.get('energy_points')

        self.fruits_vegetables_nuts_colza_walnut_olive_oils = dict.get('fruits_vegetables_nuts_colza_walnut_olive_oils')
        self.fruits_vegetables_nuts_colza_walnut_olive_oils_value = dict.get('fruits_vegetables_nuts_colza_walnut_olive_oils_value')
        self.fruits_vegetables_nuts_colza_walnut_olive_oils_points = dict.get('fruits_vegetables_nuts_colza_walnut_olive_oils_points')

        self.saturated_fat = dict.get('saturated_fat')
        self.saturated_fat_value = dict.get('saturated_fat_value')
        self.saturated_fat_points = dict.get('saturated_fat_points')
        self.saturated_fat_ratio = dict.get('saturated_fat')
        self.saturated_fat_ratio_value = dict.get('saturated_fat_ratio_value')
        self.saturated_fat_ratio_points = dict.get('saturated_fat_ratio_points')

        self.is_water = dict.get('is_water')
        self.is_beverage = dict.get('is_beverage')
        self.is_fat = dict.get('is_fat')
        self.is_cheese = dict.get('is_cheese')

        self.score = dict.get('score')
        self.positive_points = dict.get('positive_points')
        self.negative_points = dict.get('negative_points')
        self.grade = dict.get('grade')


class Packaging:
    def __init__(self, dict):
        self.shape = dict.get('shape')
        self.material = dict.get('material')


class FoodFacts:
    def __init__(self, dict):
        self._id = dict['_id']
        if 'id' in dict:
            self.id = dict['id']
        else:
            self.id = self._id
        self.product_name = ''
        if 'product_name' in dict:
            self.product_name = dict['product_name']
        self.keywords = dict['_keywords']
        self.last_update = dict['last_modified_t']
        self.creation_update = dict['created_t']
        self.pnns_groups_2 = ''
        if 'pnns_groups_2' in dict:
            self.pnns_groups_2 = dict['pnns_groups_2']
        self.lc = dict['lc']
        self.brand = ''
        self.packagings = []
        if 'packagings' in dict:
            for packaging in dict['packagings']:
                self.packagings.append(Packaging(packaging))
        if 'brands' in dict:
            self.brand = dict['brands']
        self.ingredients = []
        if 'ingredients' in dict:
            for ingredient in dict['ingredients']:
                self.ingredients.append(Ingredient(ingredient))
        if 'food_groups' in dict:
            self.food_groups =  dict['food_groups']
        if 'additives_tags' in dict:
            self.additives_tags = dict['additives_tags']
        if 'allergens_tags' in dict:
            self.allergens_tags = dict['allergens_tags']
        if 'codes_tags' in dict:
            self.allergens_tags = dict['codes_tags']
        if 'vitamins_tags' in dict:
            self.allergens_tags = dict['vitamins_tags']
        if 'nutrition_grades_tags' in dict:
            self.nutrition_grades_tags = dict['nutrition_grades_tags']
        if 'nutrition_data_per' in dict:
            self.nutrition_data_per = dict['nutrition_data_per']
        if 'nutriments' in dict:
            self.nutriments = Nutriments(dict['nutriments'])
        if 'nutriscore_data' in dict:
            self.nutriscore_data = Nutriscore(dict['nutriscore_data'])

    def __str__(self) -> str:
        return self.id + '/' + self._id + ' ' + self.product_name + ' - ' + self.brand + ' [' + self.pnns_groups_2 + '] ' + self.lc


if __name__ == '__main__':
    already_processed = 0
    filename = 'openfoodfacts-products.jsonl.gz'
    file_path = 'C:\\Users\\ralonso\\Downloads\\'

    start = time.time()

    elements = []
    with gzip.open(file_path + filename, 'rt', encoding='UTF-8') as f:
        i = 0
        n = 0
        for line in f:
            i = i + 1
            if i < already_processed:
                continue

            aDict = json.loads(line)
            if not aDict.get("countries") is None and aDict.get("countries").find('Spain')>0:
                n = n + 1
                #print(line)
                element = FoodFacts(aDict)
                print(element)
                elements.append(line)


            if (i % 100000) == 0:
                print(i)
        print(n)
        print(i)
        done = time.time()
        elapsed = done - start
        print(elapsed)

        with open(file_path + 'json_data_openff.json', 'w', encoding="UTF-8") as outfile:
            for line in elements:
                outfile.write(line)