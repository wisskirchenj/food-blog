class SelectData:
    def __init__(self, column_names: tuple, where_clause=None):
        self.columns = column_names
        self.where_clause = where_clause

    def __repr__(self):
        cols = ', '.join(self.columns)
        return "SELECT " + cols + " FROM {}"\
               + (" WHERE " + self.where_clause if self.where_clause is not None else "")
