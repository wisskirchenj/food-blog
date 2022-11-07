from sys import argv
from sqlite3 import Connection, connect

import data
from db_table_facade import DbTableFacade
from select_definition import SelectData


def get_ingredient_id(connection, ingredient_table, ingredient):
    result = ingredient_table \
        .select(connection, SelectData(('ingredient_id',), f'ingredient_name LIKE "%{ingredient}%"'))
    if len(result) != 1:
        print(data.INVALID_INGREDIENT_MSG)
        return None
    return result[0][0]


def get_measure_id(connection, measure_table, measure):
    where_clause = 'measure_name = ""' if measure == '' else f'measure_name LIKE "{measure}%"'
    result = measure_table.select(connection, SelectData(('measure_id',), where_clause))
    if len(result) != 1:
        print(data.INVALID_MEASURE_MSG)
        return None
    return result[0][0]


def ingredient_input_loop(connection: Connection, tables: dict, recipe_id: int):
    quantity_input = input(data.QUANTITY_INPUT_MSG)
    while quantity_input != "":
        tokens = quantity_input.split()
        ingredient_id = get_ingredient_id(connection, tables['ingredients'], tokens[-1])
        if ingredient_id is not None:
            measure_id = get_measure_id(connection, tables['measures'],
                                        '' if len(tokens) == 2 else tokens[1])
            if measure_id is not None:
                tables['quantity'].insert(connection, ('quantity', 'recipe_id', 'measure_id', 'ingredient_id'),
                                          (tokens[0], recipe_id, measure_id, ingredient_id))
        quantity_input = input(data.QUANTITY_INPUT_MSG)


def recipe_input_loop(connection: Connection, tables: dict):
    print(data.RECIPE_START_MSG)
    recipe_name = input(data.RECIPE_NAME_MSG)
    while recipe_name != "":
        recipe_description = input(data.RECIPE_DESCRIPTION_MSG)
        meals = tables['meals'].select(connection, SelectData(('meal_id', 'meal_name')))
        print('  '.join(str(row[0]) + ") " + row[1] for row in meals))
        meal_ids = input(data.CHOOSE_MEALS_MSG).split()
        recipe_id = tables['recipes'].insert(connection, ('recipe_name', 'recipe_description'),
                                             (recipe_name, recipe_description))
        for meal_id in meal_ids:
            tables['serve'].insert(connection, ('recipe_id', 'meal_id'),
                                   (recipe_id, meal_id))
        ingredient_input_loop(connection, tables, recipe_id)
        recipe_name = input(data.RECIPE_NAME_MSG)


def init_database(connection: Connection):
    connection.execute('PRAGMA FOREIGN_KEYS=ON')
    connection.commit()


def main():
    with connect(argv[1]) as connection:
        init_database(connection)
        db_tables = {}
        for table_entry in data.TABLE_DEFINITION_DATA:
            table = DbTableFacade(table_entry)
            db_tables[table.table_name] = table
            table.create(connection)
            table.single_value_inserts(connection, 1, data.TABLE_DATA.get(table.table_name, []))
        recipe_input_loop(connection, db_tables)
    connection.close()


main()
