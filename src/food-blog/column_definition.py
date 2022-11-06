class ColumnDefinition:
    def __init__(self, column_data: dict):
        self.name = column_data['name']
        self.definition = column_data['definition']

    def __repr__(self):
        return ' '.join([self.name, self.definition])
