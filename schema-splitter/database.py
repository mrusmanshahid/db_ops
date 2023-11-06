import pymysql
import logging
from sql import SQL

class Database:

    def __init__(self) -> None:
        pass

    def get_connection(self, host, user, password, port):
        connection = pymysql.connect(host=host, 
                                     user=user,
                                     password=password,
                                     port=port,
                                     db='mysql',
                                     autocommit=1,
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection

    def execute(self, con, sql):
        with con.cursor() as cur:
            cur.execute(sql)

    def execute_and_fetch(self, con, sql):
        with con.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchall()
            return result
