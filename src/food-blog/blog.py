import sys
from sqlite3 import Connection, connect
from db_table_facade import DbTableFacade

INT_PK = 'integer primary key'
TABLE_DEFINITION_DATA = (
    {'name': 'measures',
     'columns': ({'name': 'measure_id', 'definition': INT_PK},
                 {'name': 'measure_name', 'definition': 'text unique'})
     },
    {'name': 'ingredients',
     'columns': ({'name': 'ingredient_id', 'definition': INT_PK},
                 {'name': 'ingredient_name', 'definition': 'text not null unique'})
     },
    {'name': 'meals',
     'columns': ({'name': 'meal_id', 'definition': INT_PK},
                 {'name': 'meal_name', 'definition': 'text not null unique'})
     },
    {'name': 'recipes',
     'columns': ({'name': 'recipe_id', 'definition': INT_PK},
                 {'name': 'recipe_name', 'definition': 'text not null'},
                 {'name': 'recipe_description', 'definition': 'text'})
     }
)
TABLE_DATA = {'meals': ('breakfast', 'brunch', 'lunch', 'supper'),
              'ingredients': ('milk', 'cacao', 'strawberry', 'blueberry', 'blackberry', 'sugar'),
              'measures': ('ml', 'g', 'l', 'cup', 'tbsp', 'tsp', 'dsp', '')}


def recipe_input_loop(connection: Connection, recipe_table: DbTableFacade):
    print('Hit return when prompted for recipe name to exit.')
    recipe_name = input('Recipe name: ')
    while recipe_name != "":
        recipe_description = input('Recipe description: ')
        recipe_table.insert(connection, ('recipe_name', 'recipe_description'),
                            (recipe_name, recipe_description))
        recipe_name = input('Recipe name: ')


def main():
    with connect(sys.argv[1]) as connection:
        db_tables = {}
        for table_entry in TABLE_DEFINITION_DATA:
            table = DbTableFacade(table_entry)
            db_tables[table.table_name] = table
            table.create(connection)
            table.single_value_inserts(connection, 1, TABLE_DATA.get(table.table_name, []))
        recipe_input_loop(connection, db_tables['recipes'])
    connection.close()


main()
