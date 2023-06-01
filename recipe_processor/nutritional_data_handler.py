import re
import requests
import json

def get_food_nutritional_information(food, nutritional_service):
	if nutritional_service == "BEDCA":
		url = "https://sanger.dia.fi.upm.es/foodnorm/bedcafoods/" + food
	elif nutritional_service == "phenol_explorer":
		url = "https://sanger.dia.fi.upm.es/foodnorm/phenolfoods/" + food

	try:
		response = requests.get(url)
		response_code = response.status_code
		if response_code == 200:
			response_json = response.json()
			if response_json != []:
				return (response_code, response_json[0])
			else:
				return (response_code, {})	
		else:
			return (response_code, {})
	except requests.exceptions.RequestException as e:
		exception = str(e)
		return (-1, exception)

def format_quantity(quantity):
	fraction_match_1 = re.match(r'(\d+)⁄(\d+)', quantity)
	fraction_match_2 = re.match(r'(\d+)/(\d+)', quantity)

	if fraction_match_1:
		numerator = int(fraction_match_1.group(1))
		denominator = int(fraction_match_1.group(2))
		quantity = numerator / denominator

	elif fraction_match_2:
		numerator = int(fraction_match_2.group(1))
		denominator = int(fraction_match_2.group(2))
		quantity = numerator / denominator
	else:
		quantity = float(quantity)

	return quantity

def convert_unit_to_grams(unit, quantity):	
	if unit == None:
		return 0

	unit = unit.lower()

	if unit == "pinch" or unit == "pinches":
		return 0.5 * quantity
	elif unit == "milliliter" or unit == "milliliters":
		return 1 * quantity
	elif unit == "gram" or unit == "grams":
		return 1 * quantity
	elif unit == "clove" or unit == "cloves":
		return 3 * quantity
	elif unit == "teaspoon" or unit == "teaspoons":
		return 5 * quantity
	elif unit == "tablespoon" or unit == "tablespoons":
		return 15 * quantity
	elif unit == "ounce" or unit == "ounces":
		return 28.35 * quantity
	elif unit == "cup" or unit == "cups" or unit == "glass" or unit == "glasses":
		return 240 * quantity
	elif unit == "pound" or unit == "pounds":
		return 453.592 * quantity
	elif unit == "quart" or unit == "quarts":
		return 946 * quantity
	elif unit == "kilo" or unit == "kilo" or unit == "kilogram" or unit == "kilograms":
		return 1000 * quantity
	elif unit == "liter" or unit == "liters" or unit == "litre" or unit == "litres":
		return 1000 * quantity
	elif unit == "jar" or unit == "jars":
		return 1000 * quantity
	else:
		return 0

def get_ingredient_grams(unit, quantity):
	if quantity != "⁄" and quantity != "/":
		quantity = format_quantity(quantity)
		print(quantity)
		print(unit)
		grams = convert_unit_to_grams(unit, quantity)
		return grams
	else:
		return 0 

def get_complete_food_nutritional_information(ingredient_list_json):
	nutritional_information_dict = {
		'proteina_total': 0,
		'carbohidratos': 0,
		'fibra_total': 0,
		'azucares_totales': 0,
		'grasa_total': 0,
		'ag_saturados_total': 0,
		'ag_poliinsaturados_total': 0,
		'ag_monoinsaturados_total': 0,
		'ag_trans_total': 0,
		'colesterol': 0,
		'sodio': 0,
		'potasio': 0, 
		'vitamina_a': 0, 
		'vitamina_c': 0, 
		'calcio': 0, 
		'hierro_total': 0,
		'polifenoles_total': 0

	}
	empty = True
	for ingredient in ingredient_list_json:
		if ingredient["food"] != None and ingredient["quantity"] != None:
			food = ingredient["food"]
			grams = get_ingredient_grams(ingredient["unit"], ingredient["quantity"])
			print(grams)
			print("food: " + str(food))
			print("unit: " + str(ingredient["unit"]))
			print("quantity: " + str(ingredient["quantity"]))
			print()
			if grams != 0:
				(response_BEDCA_code, response_BEDCA_json) = get_food_nutritional_information(food, "BEDCA")
				if response_BEDCA_code == 200 and response_BEDCA_json != {}:
					empty = False
					componentes_dict = response_BEDCA_json["micronutrientes"]
					print(componentes_dict)
					componentes = componentes_dict.keys()
					for componente in componentes:
						if componentes_dict[componente] != None:
							nutritional_information_dict[componente] += (grams*float(componentes_dict[componente]))/100 

				(response_phenol_explorer_code, response_phenol_explorer_json) = get_food_nutritional_information(food, "phenol_explorer")
				if response_phenol_explorer_code == 200 and response_phenol_explorer_json != {}:
					empty = False
					print(response_phenol_explorer_json)
					for compound in response_phenol_explorer_json['compounds']:
						if compound["compound_group"] == "Polyphenols, total":
							print(food)
							polyphenol_quantity = compound['compound_subgroups'][0]["compound_quantity"][0]["mean"]
							nutritional_information_dict["polifenoles_total"] += (grams*float(polyphenol_quantity))/100 
	if empty:
		nutritional_information_dict = {}

	print(nutritional_information_dict)

	return nutritional_information_dict