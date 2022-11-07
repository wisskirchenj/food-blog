INT_PK = 'integer primary key'
INT_NN = 'integer not null'
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
                 {'name': 'meal_id', 'definition': INT_NN},
                 {'name': 'recipe_id', 'definition': INT_NN}),
     'foreign_keys': ({'column': 'meal_id', 'parent_table': 'meals',
                       'parent_column': 'meal_id'},
                      {'column': 'recipe_id', 'parent_table': 'recipes',
                       'parent_column': 'recipe_id'})
     },
    {'name': 'quantity',
     'columns': ({'name': 'quantity_id', 'definition': INT_PK},
                 {'name': 'quantity', 'definition': INT_NN},
                 {'name': 'recipe_id', 'definition': INT_NN},
                 {'name': 'measure_id', 'definition': INT_NN},
                 {'name': 'ingredient_id', 'definition': INT_NN}),
     'foreign_keys': ({'column': 'recipe_id', 'parent_table': 'recipes',
                       'parent_column': 'recipe_id'},
                      {'column': 'measure_id', 'parent_table': 'measures',
                       'parent_column': 'measure_id'},
                      {'column': 'ingredient_id', 'parent_table': 'ingredients',
                       'parent_column': 'ingredient_id'})
     }
)
TABLE_DATA = {'meals': ('breakfast', 'brunch', 'lunch', 'supper'),
              'ingredients': ('milk', 'cacao', 'strawberry', 'blueberry', 'blackberry', 'sugar'),
              'measures': ('ml', 'g', 'l', 'cup', 'tbsp', 'tsp', 'dsp', '')}

RECIPE_START_MSG = 'Hit return when prompted for recipe name to exit.'
RECIPE_NAME_MSG = 'Recipe name: '
RECIPE_DESCRIPTION_MSG = 'Recipe description: '
CHOOSE_MEALS_MSG = 'Choose meals from above (#s space-separated), where the dish can be served: '
QUANTITY_INPUT_MSG = 'Input quantity, measure and ingredient <enter to stop>:'
INVALID_INGREDIENT_MSG = 'The ingredient is not conclusive!'
INVALID_MEASURE_MSG = 'The measure is not conclusive!'
