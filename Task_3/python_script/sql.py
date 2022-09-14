class SQL:

    def __init__(self):
        pass

    def get_src_select_sql(self):
        sql =  """
            SELECT * FROM %s WHERE id between %s and %s; 
        """
        return sql

    def get_src_delete_sql(self):
        sql =  """
            DELETE FROM %s WHERE id between %s and %s; 
        """
        return sql

    def get_dest_insert_sql(self):
        sql =  """
            INSERT INTO %s VALUES %s; 
        """
        return sql
