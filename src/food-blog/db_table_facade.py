from sqlite3 import Connection
from column_definition import ColumnDefinition


class DbTableFacade:
    def __init__(self, table_data: dict):
        self.table_name = table_data['name']
        self.columns = []
        for column in table_data['columns']:
            self.columns.append(ColumnDefinition(column))

    def create(self, connection: Connection):
        cols = ',\n'.join(' ' * 4 + str(col) for col in self.columns)
        create_query = f'CREATE TABLE IF NOT EXISTS {self.table_name}(\n{cols}\n)'
        print(create_query)
        connection.execute(create_query)

    def single_value_inserts(self, connection: Connection, col_index: int, values: list[str]):
        column_name = self.columns[col_index].name
        insert_query = f'INSERT INTO {self.table_name} ({column_name}) VALUES(?)'
        print(insert_query)
        connection.executemany(insert_query, ((val, ) for val in values))

