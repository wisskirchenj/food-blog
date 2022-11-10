from sqlite3 import Connection
from db_table_facade import DbTableFacade
from select_definition import SelectData

NO_RECIPES = 'There are no such recipes in the database.'
FOUND_RECIPES = 'Recipes selected for you:'


def where_id_in(column_name: str, ids: list[int] | set[int]) -> str:
    if len(ids) == 1:
        return f'{column_name} = {ids.pop()}'
    else:
        ids = ', '.join(str(an_id) for an_id in ids)
        return f'{column_name} IN ({ids})'


class RecipeSelector:
    def __init__(self, connection: Connection, tables: dict[str, DbTableFacade]):
        self.conn = connection
        self.tables = tables

    def print_matching_recipes(self, args):
        recipe_ids = set()
        if args.ingredients is not None:
            recipe_ids = self.find_recipe_ids_with_all_ingredients(args.ingredients.split(','))
        if args.meals is not None:
            meal_recipe_ids = self.find_recipe_ids_for_meals(args.meals.split(','))
            recipe_ids = meal_recipe_ids if args.ingredients is None else recipe_ids & meal_recipe_ids
        recipes = self.find_recipes_by_id(recipe_ids)
        print(FOUND_RECIPES, ', '.join(recipes) if len(recipes) else NO_RECIPES)

    def find_recipe_ids_with_all_ingredients(self, ingredients: list[str]) -> set[int]:
        ingred_ids = self.find_ingredient_ids(ingredients)
        if ingred_ids is None:
            return set()
        where_clause = where_id_in('ingredient_id', ingred_ids)
        rows = self.tables['quantity'].select(self.conn, SelectData(('recipe_id', 'ingredient_id'), where_clause))
        contained_recipe_ids = {row[0] for row in rows}
        good_recipe_ids = set()
        for recipe_id in contained_recipe_ids:
            if {row[1] for row in rows if row[0] == recipe_id}.intersection(ingred_ids) == set(ingred_ids):
                good_recipe_ids.add(recipe_id)
        return good_recipe_ids

    def find_recipe_ids_for_meals(self, meals: list[str]) -> set[int]:
        meal_ids = [self.tables['meals'].select(self.conn, SelectData(('meal_id',), f'meal_name = "{meal}"'))[0][0]
                    for meal in meals]
        where_clause = where_id_in('meal_id', meal_ids)
        return set(row[0] for row in self.tables['serve'].select(self.conn, SelectData(('recipe_id',), where_clause)))

    def find_recipes_by_id(self, recipe_ids: set[int]) -> list[str]:
        select_data = SelectData(('recipe_name',), where_id_in('recipe_id', recipe_ids))
        rows = self.tables['recipes'].select(self.conn, select_data)
        return [row[0] for row in rows]

    # returns list of ids for the ingredients-list given or None as soon as one ingredient is not found
    # because then there may not be recipes with it...
    def find_ingredient_ids(self, ingredients) -> list[int] | None:
        ids = []
        for ing in ingredients:
            select_data = SelectData(('ingredient_id',), f'ingredient_name LIKE "%{ing.strip()}%"')
            rows = self.tables['ingredients'].select(self.conn, select_data)
            if len(rows):
                ids.append(rows[0][0])
            else:
                return None
        return ids
