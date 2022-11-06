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
     },
    {'name': 'serve',
     'columns': ({'name': 'serve_id', 'definition': INT_PK},
                 {'name': 'meal_id', 'definition': 'integer not null'},
                 {'name': 'recipe_id', 'definition': 'integer not null'}),
     'foreign_keys': ({'column': 'meal_id', 'parent_table': 'meals',
                       'parent_column': 'meal_id'},
                      {'column': 'recipe_id', 'parent_table': 'recipes',
                       'parent_column': 'recipe_id'})
     }
)
TABLE_DATA = {'meals': ('breakfast', 'brunch', 'lunch', 'supper'),
              'ingredients': ('milk', 'cacao', 'strawberry', 'blueberry', 'blackberry', 'sugar'),
              'measures': ('ml', 'g', 'l', 'cup', 'tbsp', 'tsp', 'dsp', '')}


def recipe_input_loop(connection: Connection, tables: dict):
    print('Hit return when prompted for recipe name to exit.')
    recipe_name = input('Recipe name: ')
    while recipe_name != "":
        recipe_description = input('Recipe description: ')
        print('  '.join(f'{i + 1}) {meal}' for i, meal in enumerate(TABLE_DATA['meals'])))
        meal_ids = input('Choose meals from above (#s space-separated), where the dish can be served: ').split()
        recipe_id = tables['recipes'].insert(connection, ('recipe_name', 'recipe_description'),
                                             (recipe_name, recipe_description))
        for meal_id in meal_ids:
            tables['serve'].insert(connection, ('recipe_id', 'meal_id'),
                                   (recipe_id, int(meal_id)))
        recipe_name = input('Recipe name: ')


def init_database(connection: Connection):
    connection.execute('pragma foreign_keys=ON')
    connection.commit()


def main():
    with connect(sys.argv[1]) as connection:
        init_database(connection)
        db_tables = {}
        for table_entry in TABLE_DEFINITION_DATA:
            table = DbTableFacade(table_entry)
            db_tables[table.table_name] = table
            table.create(connection)
            table.single_value_inserts(connection, 1, TABLE_DATA.get(table.table_name, []))
        recipe_input_loop(connection, db_tables)
    connection.close()


main()
