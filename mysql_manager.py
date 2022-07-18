import mysql.connector 
from mysql.connector import Error
import pandas as pd
import user_authentification as ua
#import test_login


# database parameters
user = 'root'
pw = "150617"
host = "localhost"
db = "lms_dummy"

# Fungsi Koneksi ke Server
def create_server_connection(host_name, user_name, user_password):
    connection = None
    
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password
        )
        print("MySQL server connection is established")
    except Error as error:
        print(f"Error: {error}")
    return connection

# Fungsi membuat database
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created")
    except Error as error:
        print(f"Error: {error}")


# Fungsi Koneksi ke database
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name)
        print("MySQL database connection is established")
    except Error as error:
        print(f"Error: {error}")
    return connection

# Fungsi untuk Eksekusi Query, Create, Update, Delete, Insert table and data
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed")
    except Error as error:
        print(f"Error: {error}")

# FUngsi Read Query
def read_query_as_pd(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return pd.DataFrame(result)
    except Error as error:
        print(f"Error: {error}")


def read_query_as_object(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as error:
        print(f"Error: {error}")

# variable untuk execute atau read queries
# creating database
creating_database = f"CREATE DATABASE IF NOT EXISTS {db}"

creating_users_table = """
CREATE TABLE IF NOT EXISTS users_table(
username TEXT,
password TEXT)
"""

# inserting new user
def insert_new_user(new_user, new_user_password):
   return f"INSERT INTO users_table (username, password) VALUES(\"{new_user}\",\"{ua.hash_password(new_user_password)}\")"

# password checking
def select_password_from_table(user):
    return f'SELECT password FROM users_table WHERE username = \"{user}\"'

# Membuat database lms_project
#create_database(
#    create_server_connection(host, user, pw), 
#    creating_database)