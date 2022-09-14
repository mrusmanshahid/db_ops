import datetime
import pymysql
import logging
from configs import Config as conf
from sql import SQL as sql

class MigrateData:
    def __init__(self):
        pass

    def get_connection(self, host, user, password, database):
        conn = pymysql.connect(host=host, user=user, password=password,
                               database=database, port=3306, connect_timeout=5)
        return conn

    def get_all_batches(self, statement):
        logging.info(f'Loading Batches')
        start = conf.batch_start
        end = conf.batch_end
        temp_end = start + conf.batch_size
        sql_statements = self.prepare_sql_statements(statement, start, end, temp_end)
        logging.info(f'Total Statements Created: {str(len(sql_statements))}')
        return sql_statements

    def prepare_sql_statements(self, statement, start, end, temp_end):
        prepared_sql_statements = []
        while temp_end < end:
            stmt = statement % (start_date, temp_end)
            prepared_sql_statements.append(stmt)
            start_date = temp_date
            temp_date = start_date + conf.batch_size
        stmt = statement % (start, end)
        prepared_sql_statements.append(stmt)
        return prepared_sql_statements

    def get_data_from_src(self, statement):
        logging.info(f'Fetching data for statement: {statement}')
        con = self.get_connection(conf.src_db_url, conf.src_db_username, conf.src_db_password, conf.src_schema)
        with con.cursor() as cursor:
            return cursor.execute(statement)
    
    def delete_batch_at_src(self, statement):
        logging.info(f'Deleting data for statement: {statement}')
        con = self.get_connection(conf.src_db_url, conf.src_db_username, conf.src_db_password, conf.src_schema)
        with con.cursor() as cursor:
            return cursor.execute(statement)

    def insert_into_target(self, data):
        logging.info(f'Migrating {len(data)} records to the destination database')
        statement = sql.get_dest_insert_sql()
        con = self.get_connection(conf.dest_db_url, conf.dest_db_username, conf.dest_db_password, conf.dest_schema)
        with con.cursor() as cursor:
            cursor.executemany(statement, data)
            cursor.close()
    
    def migrate_to_destination(self):
        statement = sql.get_src_select_sql()
        batches = self.get_all_batches(statement)
        for batch_statement in batches:
            data = self.get_data_from_src(batch_statement)
            self.insert_into_target(data)
    
    def delete_from_source(self):
        statement = sql.get_src_delete_sql()
        batches = self.get_all_batches(statement)
        for batch_statement in batches:
            self.delete_batch_at_src(batch_statement)