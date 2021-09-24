import sqlite3

class DataBaseFunctions:
    def __init__(self):
        pass
    def connection(func):
        def accepting_arguments(self, arg1, arg2, arg3=None):
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            if func.__name__ == 'insert':
                cur.execute(func(self, arg1, arg2), arg1)
            elif func.__name__ == 'delete':
                cur.execute(func(self, arg1, arg2))
            else:
                cur.execute(func(self, arg1, arg2, arg3))
            result = cur.fetchall()
            conn.commit()
            conn.close()
            if not len(result): return []
            return list(list(x) if len(x) > 1 else x[0] for x in result)
        return accepting_arguments
    @connection
    def select(self, select_data, table_name, filter=None):
        return f'SELECT {select_data} FROM {table_name}' + int(filter is not None)*f' WHERE {filter}'
    @connection
    def update(self, update_data, table_name, filter=None):
        return f'UPDATE {table_name} SET {update_data}' + int(filter is not None)*f' WHERE {filter}'
    @connection
    def insert(self, insert_data, table_name):
        return f'INSERT INTO {table_name} VALUES ({("?, "*len(insert_data))[:-2]})'
    @connection
    def delete(self, delete_filter, table_name):
        return f'DELETE FROM {table_name} WHERE {delete_filter}'
