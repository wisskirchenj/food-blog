import sys
import sqlite3
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
     }
)
TABLE_DATA = {'meals': ('breakfast', 'brunch', 'lunch', 'supper'),
              'ingredients': ('milk', 'cacao', 'strawberry', 'blueberry', 'blackberry', 'sugar'),
              'measures': ('ml', 'g', 'l', 'cup', 'tbsp', 'tsp', 'dsp', '')}


def main():
    with sqlite3.connect(sys.argv[1]) as database:
        for table_entry in TABLE_DEFINITION_DATA:
            db_table = DbTableFacade(table_entry)
            db_table.create(database)
            db_table.single_value_inserts(database, 1, TABLE_DATA[db_table.table_name])
    database.close()


main()
