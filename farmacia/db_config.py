import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',        # Coloque seu usuário MySQL
        password='',      # Coloque sua senha MySQL
        database='farmacia_db'
    )
    return connection
