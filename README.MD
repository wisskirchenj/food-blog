# IDEA EDU Course ...

Implemented in the Track 'SQL with Python' of hyperskill.org's JetBrains Academy.

## Technology / External Libraries

- Python 3.10.8,
- with packages: sqlite3, sys, sty, argparse, scikit-learn, tox, black and isort

## Repository Contents

The sources of main project tasks (5 stages) and testing.

## Installation

Install the wheel file using pip after clone/fork:

> $ pip install dist/food_blog-3.10-py3-none-any.whl

## Program description

The toy project implements a simple Python backend that will allow to populate an SQLite3 database with recipes. 
We deal from Python with an auto-increment primary key and use foreign keys to create relationships
between tables. We work with many-to-many relations, with SQL queries, and with database cursor methods.

Stage 1: just database creation and initialization

Stage 2: first recipe entry loop by the user

Stage 3: recipes for dishes may now be entered in N:N-relation to the meals they belong to

Stage 4: now ingredients with quantities can be added to the recipe. The input of arbitrary many ingredients per recipe
with quantity and measures is (too ?) sophisticated: 
1) ingredient: any substring of an ingredient is valid, as long unique over all ingredients
2) for a measure (as l, kg, tsp, ...) the table-entry must _start_ with the given user input and be unique.
3) If no measure is given, an empty measure is taken (e.g. 3 apples).
For persistence of ingredients a quantity table is used, that has 3 FKs to the recipes, ingredients and measures table

Stage 5: new CL parameters --ingredients and --meals are possible with list values (e.g. --ingredients="sugar,milk" or
--meals="breakfast, lunch"), that when given select all recipes in the database, that contain ALL ingredients and
are served at at least one of the given meals. If both are npt provided, the application takes new input exactly
as in stage 4.

Have fun!


## Project completion

Project was completed on 10.11.22.)

## Progress

05.11.22 Project started - gitHub repo and project structure setup.

06.11.22 Stage 1 completed - create SQLite3 database tables from Python and populate them with initial data, 
some OOP design used here (first time with Python)

06.11.22 Stage 2 completed - add recipe table, ask for dishes and recipes in a loop and persist them

06.11.22 Stage 3 completed - add serve table as many-to-many relation table between meals and recipes,
use Cursors lastrowid method, handle IntegrityError for already inserted data

06.11.22 Stage 4 completed - another many-to-many relation quantity table added with 3 foreign keys.
The DbTableFacade gets a generic select()-method, that uses a SelectData-class as input. Logging of
queries and Select-result sets is done in colored messages using package sty

10.11.22 Stage 5 completed - a new RecipeSelector class is added to handle the complex recipe queries
for the provided filters (intense use of Python's set operation as well as list, tuple)
