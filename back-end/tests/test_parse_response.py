"""
This is the test suite for methods related to parsing search queries for the
Yummly API.
"""
import unittest
from unittest.mock import Mock
from api_functions import parse_response
from request_error import RequestError
from no_match_error import NoMatchError

"""
Test methods related to parsing error results of search queries in Yummly API
"""
class TestParseErrorSearchResults(unittest.TestCase):

	def setUp(self):
		self.keyword = 'search'

	# Test returning an error message for 500 response
	def test_parse_server_error_response(self):
		mock_response = Mock(status_code=500)
		self.assertRaises(RequestError, parse_response, self.keyword, mock_response)

	# Test returning an error message for 409 response
	def test_parse_rate_limit_response(self):
		mock_response = Mock(status_code=409)
		self.assertRaises(RequestError, parse_response, self.keyword, mock_response)

	# Test returning an error message for 400 response
	def test_parse_bad_request_response(self):
		mock_response = Mock(status_code=400)
		self.assertRaises(RequestError, parse_response, self.keyword, mock_response)


"""
Test method related to parsing successful results of search queries in Yummly
API
"""
class TestParseSuccessSearchResults(unittest.TestCase):

	def setUp(self):
		self.keyword = 'search'

	# Test parsing a recipe match for 200 response
	def test_parse_success_response(self):
		mock_json_data = { 'criteria': { 'excludedIngredient': None, 
										 'q': 'onion soup', 
										 'allowedIngredient': None
									   }, 
						   'totalMatchCount': 89479, 
						   'matches': [{ 'recipeName': 'Easy French Onion Soup',
										 'id': 'Easy-French-Onion-Soup-2038937', 
										 'flavors': None, 
										 'ingredients': ['butter', 
														 'onions', 
														 'au jus gravy mix', 
														 'water'], 
										 'rating': 3,
										 'attributes': {'course': ['Soups']}, 
										 'totalTimeInSeconds': 2100, 
										 'sourceDisplayName': 'McCormick', 
										 'smallImageUrls': ['https://lh3.googleusercontent.com/Bq8oxo3CpxSSY-rur00MRQ6iQAKRwcmFjIcVeLqz817x64Y7d9Py9CtU4NiN0NCxEpJi3-AT9FT9hyFJgjVXAzI=s90'],
										 'imageUrlsBySize': {'90': 'https://lh3.googleusercontent.com/l_8dJqkMDa2Ge6978mu2Tv4XVCsuHq7LZaQQIz1pfBsGgvabhCo6Q7eI_mmyc_FXVsa3Fn2-i892lWZVc_18=s90-c'}
									   }],
						   'attribution': { 'html': "Recipe search powered by <a href='http://www.yummly.co/recipes'><img alt='Yummly' src='https://static.yummly.co/api-logo.png'/></a>",
											'logo': 'https://static.yummly.co/api-logo.png',
											'url': 'http://www.yummly.co/recipes/',
											'text': 'Recipe search powered by Yummly'
										  }, 
						   'facetCounts': {}}

		mock_response = Mock(status_code=200)
		mock_response.json.return_value = mock_json_data
		expected_recipe_id = 'Easy-French-Onion-Soup-2038937'
		self.assertEqual(expected_recipe_id, parse_response(self.keyword, mock_response))

		# Test parsing a recipe response of 200 but with no matches
		no_match_mock_data = { 'criteria': { 'excludedIngredient': None, 
										 	 'q': 'onion soup', 
										 	 'allowedIngredient': None
									   	   }, 
						   	   'totalMatchCount': 89479, 
						   	   'matches': [],
						   	   'attribution': { 'html': "Recipe search powered by <a href='http://www.yummly.co/recipes'><img alt='Yummly' src='https://static.yummly.co/api-logo.png'/></a>",
												'logo': 'https://static.yummly.co/api-logo.png',
												'url': 'http://www.yummly.co/recipes/',
												'text': 'Recipe search powered by Yummly'
										  	  }, 
						   	   'facetCounts': {}}
		mock_response = Mock(status_code=200)
		mock_response.json.return_value = no_match_mock_data
		self.assertRaises(NoMatchError, parse_response, self.keyword, mock_response)

"""
Test methods related to parsing recipe result
"""
class TestParseRecipeResult(unittest.TestCase):

	def setUp(self):
		self.keyword = 'recipe'
		self.mock_response_body = { 'numberOfServings': 4, 
		  				  	   'rating': 3, 
		  				  	   'flavors': {}, 
		  				  	   'ingredientLines': [ '3 tbsps butter', 
		  					   				   		'3 medium onions, thinly sliced', 
		  					   				   		'1 package McCormick® Au Jus Gravy Mix', 
		  					   				   		'3 cups water' ], 
		  				  	   'yield': None, 
		  				  	   'name': 'Easy French Onion Soup', 
		  				  	   'totalTimeInSeconds': 2100, 
		  				  	   'source': { 'sourceDisplayName': 'McCormick', 
		  			  				       'sourceRecipeUrl': 'https://www.mccormick.com/recipes/soups-stews/easy-french-onion-soup', 
		  			  				  	   'sourceSiteUrl': 'http://www.mccormick.com' }, 
		  				  	   'nutritionEstimates': [ { 'unit': {'pluralAbbreviation': 'kcal', 
		  									 				 	  'plural': 'calories', 
		  									 				 	  'id': 'fea252f8-9888-4365-b005-e2c63ed3a776', 
		  									 				 	  'name': 'calorie', 
		  									 				 	  'decimal': True, 
		  									 				 	  'abbreviation': 'kcal'}, 
		  												'description': None, 
		  												'value': 80.0, 
		  												'attribute': 'FAT_KCAL' },
		  						  				  	   { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  				  	   'plural': 'grams', 
		  						  			  				  	   'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  				  	   'name': 'gram', 
		  						  			  				  	   'decimal': True, 
		  						  			  				  	   'abbreviation': 'g' },
		  						  						 'description': 'Potassium, K', 
		  						  						 'value': 0.12, 
		  						  						 'attribute': 'K' }, 
		  						  				 	   { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			 				 	   'plural': 'grams', 
		  						  			 				       'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			 				       'name': 'gram', 
		  						  			 			 'decimal': True, 
		  						  			 			 'abbreviation': 'g' }, 
		  						  						 'description': 'Fluoride, F', 
		  						  						 'value': 0.0, 
		  						  						 'attribute': 'FLD' }, 
		  						  					   { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  					   'plural': 'grams', 
		  						  			  					   'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  					   'name': 'gram', 
		  						  			  					   'decimal': True, 
		  						  			  					   'abbreviation': 'g' }, 
		  						  						 'description': 'Phytosterols', 
		  						  						 'value': 0.01, 
		  						  						 'attribute': 'PHYSTR' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	'description': 'Beta-sitosterol', 
		  						  	'value': 0.0, 
		  						  	'attribute': 'SITSTR' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	'description': '18:1 c', 
		  						  	'value': 1.81, 
		  						  	'attribute': 'F18D1C' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	'description': '18:2 n-6 c,c', 
		  						  	'value': 0.21, 
		  						  	'attribute': 'F18D2CN6' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8',
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	'description': 'Fatty acids, total saturated', 
		  						  	'value': 5.43, 
		  						  	'attribute': 'FASAT' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'mcg_DFE', 
		  						  			  'plural': 'mcg_DFE', 
		  						  			  'id': '4d783ee4-aa07-4958-84bf-3f4b528049dc', 
		  						  			  'name': 'mcg_DFE', 
		  						  			  'decimal': False, 
		  						  			  'abbreviation': 'mcg_DFE' }, 
		  						  	'description': 'Folate, DFE', 
		  						  	'value': 15.99, 
		  						  	'attribute': 'FOLDFE' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	'description': '12:0', 
		  						  	'value': 0.32, 
		  						  	'attribute': 'F12D0' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g'}, 
		  						  	'description': 'Glucose (dextrose)', 
		  						  	'value': 1.65, 
		  						  	'attribute': 'GLUS' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	'description': '16:1 undifferentiated', 
		  						  	'value': 0.11, 
		  						  	'attribute': 'F16D1' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	'description': '18:1 t', 
		  						  	'value': 0.32, 
		  						  	'attribute': 'F18D1T' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	'description': 'Folate, food', 
		  						  	'value': 0.0, 
		  						  	'attribute': 'FOLFD' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'kcal', 
		  						  			  'plural': 'calories', 
		  						  			  'id': 'fea252f8-9888-4365-b005-e2c63ed3a776', 
		  						  			  'name': 'calorie', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'kcal' }, 
		  						  	'description': 'Energy', 
		  						  	'value': 456.34, 
		  						  	'attribute': 'ENERC_KJ' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  				'plural': 'grams', 
		  						  				'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  				'name': 'gram', 
		  						  				'decimal': True, 
		  						  				'abbreviation': 'g' }, 
		  						  	'description': '4:0', 
		  						  	'value': 0.32, 
		  						  	'attribute': 'F4D0' }, 
		  						  { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  			  'plural': 'grams', 
		  						  			  'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  			  'name': 'gram', 
		  						  			  'decimal': True, 
		  						  			  'abbreviation': 'g' }, 
		  						  	  'description': 'Fructose', 
		  						  	  'value': 0.83, 
		  						  	  'attribute': 'FRUS' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Vitamin E (alpha-tocopherol)', 
		  						  	   'value': 0.0, 
		  						  	   'attribute': 'TOCPHA' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	 	'description': 'Water', 
		  						  	 	'value': 290.38, 
		  						  	 	'attribute': 'WATER' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': '8:0', 
		  						  	   'value': 0.11, 
		  						  	   'attribute': 'F8D0' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Retinol', 
		  						  	   'value': 0.0, 
		  						  	   'attribute': 'RETOL' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Sugars, total', 
		  						  	   'value': 3.3, 
		  						  	   'attribute': 'SUGAR' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': '6:0', 
		  						  	   'value': 0.21, 
		  						  	   'attribute': 'F6D0' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Fatty acids, total monounsaturated', 
		  						  	   'value': 2.24, 
		  						  	   'attribute': 'FAMS' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Ash', 
		  						  	   'value': 0.21, 
		  						  	   'attribute': 'ASH' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Selenium, Se', 
		  						  	   'value': 0.0, 
		  						  	   'attribute': 'SE' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Fiber, total dietary', 
		  						  	   'value': 1.65, 
		  						  	   'attribute': 'FIBTG' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Protein', 
		  						  	   'value': 0.93, 
		  						  	   'attribute': 'PROCNT' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Carbohydrate, by difference', 
		  						  	   'value': 7.43, 
		  						  	   'attribute': 'CHOCDF' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Folate, total', 
		  						  	   'value': 0.0, 
		  						  	   'attribute': 'FOL' }, 
		  						  	 { 'unit': { 'pluralAbbreviation': 'grams', 
		  						  	 			 'plural': 'grams', 
		  						  	 			 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 
		  						  	 			 'name': 'gram', 
		  						  	 			 'decimal': True, 
		  						  	 			 'abbreviation': 'g' }, 
		  						  	   'description': 'Vitamin K (phylloquinone)', 
		  						  	   'value': 0.0, 
		  						  	   'attribute': 'VITK' }, 
		  						  	   {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': '18:0', 'value': 1.07, 'attribute': 'F18D0'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Lutein + zeaxanthin', 'value': 0.0, 'attribute': 'LUT+ZEA'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Cholesterol', 'value': 0.02, 'attribute': 'CHOLE'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': '17:0', 'value': 0.11, 'attribute': 'F17D0'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Phosphorus, P', 'value': 0.03, 'attribute': 'P'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Choline, total', 'value': 0.01, 'attribute': 'CHOLN'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': '10:0', 'value': 0.32, 'attribute': 'F10D0'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Calcium, Ca', 'value': 0.03, 'attribute': 'CA'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Magnesium, Mg', 'value': 0.01, 'attribute': 'MG'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Fatty acids, total polyunsaturated', 'value': 0.32, 'attribute': 'FAPU'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': '14:0', 'value': 0.75, 'attribute': 'F14D0'}, {'unit': {'pluralAbbreviation': 'mcg_RAE', 'plural': 'mcg_RAE', 'id': '0fcf76b3-891a-403d-883f-58c8809ef151', 'name': 'mcg_RAE', 'decimal': False, 'abbreviation': 'mcg_RAE'}, 'description': 'Vitamin A, RAE', 'value': 72.85, 'attribute': 'VITA_RAE'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': '16:0', 'value': 2.34, 'attribute': 'F16D0'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': '18:1 undifferentiated', 'value': 2.13, 'attribute': 'F18D1'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': '18:2 undifferentiated', 'value': 0.32, 'attribute': 'F18D2'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Sucrose', 'value': 0.83, 'attribute': 'SUCS'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Carotene, beta', 'value': 0.0, 'attribute': 'CARTB'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': '16:1 c', 'value': 0.11, 'attribute': 'F16D1C'}, {'unit': {'pluralAbbreviation': 'IU', 'plural': 'IU', 'id': 'ed46fe0c-44fe-4c1f-b3a8-880f92e30930', 'name': 'IU', 'decimal': True, 'abbreviation': 'IU'}, 'description': 'Vitamin A, IU', 'value': 267.79, 'attribute': 'VITA_IU'}, {'unit': {'pluralAbbreviation': 'kcal', 'plural': 'calories', 'id': 'fea252f8-9888-4365-b005-e2c63ed3a776', 'name': 'calorie', 'decimal': True, 'abbreviation': 'kcal'}, 'description': 'Energy', 'value': 109.36, 'attribute': 'ENERC_KCAL'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Vitamin C, total ascorbic acid', 'value': 0.01, 'attribute': 'VITC'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Total lipid (fat)', 'value': 8.63, 'attribute': 'FAT'}, {'unit': {'pluralAbbreviation': 'IU', 'plural': 'IU', 'id': 'ed46fe0c-44fe-4c1f-b3a8-880f92e30930', 'name': 'IU', 'decimal': True, 'abbreviation': 'IU'}, 'description': 'Vitamin D', 'value': 6.39, 'attribute': 'VITD-'}, {'unit': {'pluralAbbreviation': 'grams', 'plural': 'grams', 'id': '12485d26-6e69-102c-9a8a-0030485841f8', 'name': 'gram', 'decimal': True, 'abbreviation': 'g'}, 'description': 'Sodium, Na', 'value': 0.07, 'attribute': 'NA'}], 'id': 'Easy-French-Onion-Soup-2038937', 'attribution': {'url': 'http://www.yummly.co/recipe/Easy-French-Onion-Soup-2038937', 'logo': 'https://static.yummly.co/api-logo.png', 'html': "<a href='http://www.yummly.co/recipe/Easy-French-Onion-Soup-2038937'>Easy French Onion Soup recipe</a> information powered by <img alt='Yummly' src='https://static.yummly.co/api-logo.png'/>", 'text': 'Easy French Onion Soup recipes: information powered by Yummly'}, 'images': [{'imageUrlsBySize': {'360': 'https://lh3.googleusercontent.com/l_8dJqkMDa2Ge6978mu2Tv4XVCsuHq7LZaQQIz1pfBsGgvabhCo6Q7eI_mmyc_FXVsa3Fn2-i892lWZVc_18=s360-c', '90': 'https://lh3.googleusercontent.com/l_8dJqkMDa2Ge6978mu2Tv4XVCsuHq7LZaQQIz1pfBsGgvabhCo6Q7eI_mmyc_FXVsa3Fn2-i892lWZVc_18=s90-c'}, 'hostedMediumUrl': 'https://lh3.googleusercontent.com/Bq8oxo3CpxSSY-rur00MRQ6iQAKRwcmFjIcVeLqz817x64Y7d9Py9CtU4NiN0NCxEpJi3-AT9FT9hyFJgjVXAzI=s180', 'hostedLargeUrl': 'https://lh3.googleusercontent.com/Bq8oxo3CpxSSY-rur00MRQ6iQAKRwcmFjIcVeLqz817x64Y7d9Py9CtU4NiN0NCxEpJi3-AT9FT9hyFJgjVXAzI=s360', 'hostedSmallUrl': 'https://lh3.googleusercontent.com/Bq8oxo3CpxSSY-rur00MRQ6iQAKRwcmFjIcVeLqz817x64Y7d9Py9CtU4NiN0NCxEpJi3-AT9FT9hyFJgjVXAzI=s90'}], 'totalTime': '35 min', 'attributes': {'course': ['Soups']}}
	
	# Test returning an error message for 500 response
	def test_parse_server_error_response(self):
		mock_response = Mock(status_code=500)
		self.assertRaises(RequestError, parse_response, self.keyword, mock_response)

	# Test returning an error message for 409 response
	def test_parse_rate_limit_response(self):
		mock_response = Mock(status_code=409)
		self.assertRaises(RequestError, parse_response, self.keyword, mock_response)

	# Test returning an error message for 400 response
	def test_parse_bad_request_response(self):
		mock_response = Mock(status_code=400)
		self.assertRaises(RequestError, parse_response, self.keyword, mock_response)

	# Test returning a response body for successful request
	def test_successful_request(self):
		mock_response = Mock(status_code=200)
		mock_response.json.return_value = self.mock_response_body
		self.assertEqual(self.mock_response_body, parse_response(self.keyword, mock_response))


if __name__ == '__main__':
	unittest.main()