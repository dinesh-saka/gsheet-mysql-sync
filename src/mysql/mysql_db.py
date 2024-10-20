from sqlalchemy import create_engine
import pymysql

def connect_to_mysql():
    engine = create_engine('mysql+pymysql://<yourusername>:<yourpassword>@localhost/<dbname>')
    connection = engine.connect()
    return connection

def execute_query(query, data=None):
    connection = connect_to_mysql()
    if data:
        connection.execute(query, data)
    else:
        connection.execute(query)
    connection.close()
