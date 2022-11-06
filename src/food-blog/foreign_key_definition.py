class FkDefinition:
    def __init__(self, fk_data: dict):
        self.child_column = fk_data['column']
        self.parent_table = fk_data['parent_table']
        self.parent_column = fk_data['parent_column']

    def __repr__(self):
        return f'    FOREIGN KEY ({self.child_column})\n' + \
               f'        REFERENCES {self.parent_table} ({self.parent_column})'
