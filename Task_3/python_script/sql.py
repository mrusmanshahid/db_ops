from configs import Config as config

class SQL:

    def __init__(self):
        pass

    def get_src_select_sql():
        sql =  """
            SELECT * FROM """+config.table_name+""" WHERE id between %s and %s; 
        """
        return sql

    def get_src_delete_sql():
        sql =  """
            DELETE FROM """+config.table_name+"""  WHERE id between %s and %s; 
        """
        return sql

    def get_dest_insert_sql():
        sql =  """
            INSERT INTO """+config.table_name+"""  VALUES %s; 
        """
        return sql
