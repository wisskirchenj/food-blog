from argparse import ArgumentParser
from sqlite3 import Connection, connect

import data
from db_table_facade import DbTableFacade
from select_definition import SelectData
from recipe_selector import RecipeSelector


def get_ingredient_id(conn, ingredient_table, ingredient):
    result = ingredient_table \
        .select(conn, SelectData(('ingredient_id',), f'ingredient_name LIKE "%{ingredient}%"'))
    if len(result) != 1:
        print(data.INVALID_INGREDIENT_MSG)
        return None
    return result[0][0]


def get_measure_id(conn, measure_table, measure):
    where_clause = 'measure_name = ""' if measure == '' else f'measure_name LIKE "{measure}%"'
    result = measure_table.select(conn, SelectData(('measure_id',), where_clause))
    if len(result) != 1:
        print(data.INVALID_MEASURE_MSG)
        return None
    return result[0][0]


def ingredient_input_loop(conn: Connection, tables: dict, recipe_id: int):
    quantity_input = input(data.QUANTITY_INPUT_MSG)
    while quantity_input != "":
        tokens = quantity_input.split()
        ingredient_id = get_ingredient_id(conn, tables['ingredients'], tokens[-1])
        if ingredient_id is not None:
            measure_id = get_measure_id(conn, tables['measures'],
                                        '' if len(tokens) == 2 else tokens[1])
            if measure_id is not None:
                tables['quantity'].insert(conn, ('quantity', 'recipe_id', 'measure_id', 'ingredient_id'),
                                          (tokens[0], recipe_id, measure_id, ingredient_id))
        quantity_input = input(data.QUANTITY_INPUT_MSG)


def recipe_input_loop(conn: Connection, tables: dict[str, DbTableFacade]):
    print(data.RECIPE_START_MSG)
    recipe_name = input(data.RECIPE_NAME_MSG)
    while recipe_name != "":
        recipe_description = input(data.RECIPE_DESCRIPTION_MSG)
        meals = tables['meals'].select(conn, SelectData(('meal_id', 'meal_name')))
        print('  '.join(str(row[0]) + ") " + row[1] for row in meals))
        meal_ids = input(data.CHOOSE_MEALS_MSG).split()
        recipe_id = tables['recipes'].insert(conn, ('recipe_name', 'recipe_description'),
                                             (recipe_name, recipe_description))
        for meal_id in meal_ids:
            tables['serve'].insert(conn, ('recipe_id', 'meal_id'),
                                   (recipe_id, meal_id))
        ingredient_input_loop(conn, tables, recipe_id)
        recipe_name = input(data.RECIPE_NAME_MSG)


def init_database(conn: Connection) -> dict[str, DbTableFacade]:
    conn.execute('PRAGMA FOREIGN_KEYS=ON')
    db_tables = {}
    for table_entry in data.TABLE_DEFINITION_DATA:
        table = DbTableFacade(table_entry)
        db_tables[table.table_name] = table
        table.create(conn)
        table.single_value_inserts(conn, 1, data.TABLE_DATA.get(table.table_name, []))
    return db_tables


def parse_commandline_arguments():
    parser = ArgumentParser(description='Food blog backend where you can enter recipes to store')
    parser.add_argument('database_path', help="path to your database")
    parser.add_argument('--ingredients', help='Enter ingredients comma-separated without blanks')
    parser.add_argument('--meals', help='Enter meals comma-separated without blanks')
    return parser.parse_args()


def main():
    args = parse_commandline_arguments()
    with connect(args.database_path) as conn:
        tables = init_database(conn)
        if (args.ingredients, args.meals) == (None, None):
            recipe_input_loop(conn, tables)
        else:
            RecipeSelector(conn, tables).print_matching_recipes(args)
    conn.close()


main()
