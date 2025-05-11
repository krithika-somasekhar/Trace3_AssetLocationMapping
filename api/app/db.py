import pymysql
from flask import current_app, g
from pymysql.cursors import DictCursor

def get_db_connection():
    if 'db_conn' not in g:
        host = current_app.config['DB_HOST']
        user = current_app.config['DB_USER']
        password = current_app.config['DB_PASSWORD']
        database = current_app.config['DB_NAME']
        g.db_conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=DictCursor,
            autocommit=True
        )
    return g.db_conn

def close_db_connection(e=None):
    db_conn = g.pop('db_conn', None)
    if db_conn is not None and not db_conn._closed:
        db_conn.close()
