from sqlite3 import Connection, IntegrityError
from sty import fg

from column_definition import ColumnDefinition
from foreign_key_definition import FkDefinition


class DbTableFacade:
    def __init__(self, table_data: dict):
        self.table_name = table_data['name']
        self.columns = []
        for column in table_data['columns']:
            self.columns.append(ColumnDefinition(column))
        self.foreign_keys = []
        for foreign_key in table_data.get('foreign_keys', []):
            self.foreign_keys.append(FkDefinition(foreign_key))

    def create(self, connection: Connection):
        in_query = ',\n'.join(' ' * 4 + str(col) for col in self.columns)
        if len(self.foreign_keys) > 0:
            fks = ',\n'.join(str(fk) for fk in self.foreign_keys)
            in_query = ',\n'.join((in_query, fks))
        create_query = f'CREATE TABLE IF NOT EXISTS {self.table_name}(\n{in_query}\n)'
        print(create_query)
        connection.execute(create_query)

    def single_value_inserts(self, connection: Connection, col_index: int, values: list[str]):
        column_name = self.columns[col_index].name
        insert_query = f'INSERT INTO {self.table_name} ({column_name}) VALUES(?)'
        print(insert_query)
        try:
            connection.executemany(insert_query, ((val, ) for val in values))
            connection.commit()
        except IntegrityError as error:
            print(fg.red + str(error) + '. Data were already inserted.' + fg.rs)

    def insert(self, connection: Connection, col_names: tuple, values: tuple):
        values_str = ', '.join(f'"{val}"' for val in values)
        col_str = ', '.join(col_names)
        insert_query = f'INSERT INTO {self.table_name} ({col_str}) VALUES({values_str})'
        print(insert_query)
        return connection.execute(insert_query).lastrowid
