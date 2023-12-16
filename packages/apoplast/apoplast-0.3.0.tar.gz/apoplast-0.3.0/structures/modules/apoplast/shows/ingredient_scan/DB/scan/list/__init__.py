
'''
#
#	actual
#
import apoplast.shows.ingredient_scan.DB.scan.list as ingredients_DB_list_scan
ingredients_list = ingredients_DB_list_scan.retrieve ()
'''	

'''
#
#	extra
#
import apoplast.shows.ingredient_scan.DB.scan.list as ingredients_DB_list_scan
import apoplast.shows.ingredient_scan.DB.access as access
ingredients_list = ingredients_DB_list_scan.retrieve (
	ingredients_DB = access.DB ()
)
'''
	
import apoplast.shows.ingredient_scan.DB.access as access

def retrieve (
	ingredients_DB = access.DB ()
):	
	return ingredients_DB.all ()