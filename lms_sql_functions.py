import mysql.connector 
from mysql.connector import Error
import pandas as pd

import lms_python_functions as lpf


# database parameters
user = 'root'
pw = "150617"
host = "localhost"
db = "lms_project"

# table name
admin_table = "admin_table"
users_table = 'users_table'
books_table = 'books_table'


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


# membuat koneksi ke database


db_connection = create_db_connection(
    host_name = host, 
    user_name = user, 
    user_password = pw, 
    db_name = db)


# strings to create sql database and tables
# creating database
creating_database_string = f'CREATE DATABASE IF NOT EXISTS {db}'

creating_admin_table_string = (
    f'CREATE TABLE IF NOT EXISTS '
    f'{admin_table}'
    f'(admin_name VARCHAR(50), admin_password VARCHAR(64))'
)

creating_users_table_string = (
    f'CREATE TABLE IF NOT EXISTS '
    f'{users_table}'
    f'(user_id INT AUTO_INCREMENT PRIMARY KEY,'
    f'user_name VARCHAR(50),'
    f'date_of_birth DATE,'
    f'occupation VARCHAR(50),'
    f'address VARCHAR(50),'
    f'password VARCHAR(64))'

)

creating_books_table_string = (
    f'CREATE TABLE IF NOT EXISTS '
    f'{books_table}'
    f'(book_id INT AUTO_INCREMENT PRIMARY KEY,'
    f'book_title TEXT,'
    f'book_category VARCHAR(50),'
    f'book_status VARCHAR(50),'
    f'borrowed_date DATE,'
    f'expected_return_date DATE,'
    f'actual_returned_date DATE,'
    f'borrowed_by VARCHAR(50))'
)


# function to insert new book to database by admin
def insert_new_book(new_book_title, new_book_category, new_book_stock, db_connection):
    sql_string = (
        f'INSERT INTO {books_table} (book_title, book_category, book_status) '
        f'VALUES (\"{new_book_title}\",\"{new_book_category}\", \"available\")'
    )

    for i in range(0, int(new_book_stock)):
        execute_query(db_connection, sql_string)

    

# books status options for further data handling (if any)
books_status = ('available', 'borrowed', 'requested to be borrowed', 'to be approved for return')

#present books record summary for admin
presenting_books_table_for_admin_summary_string = (
    f'SELECT book_title, book_category, '
    f'SUM(CASE WHEN book_status = \'{books_status[0]}\' THEN 1 ELSE 0 END) AS {books_status[0]}, '
    f'SUM(CASE WHEN book_status = \'{books_status[1]}\' THEN 1 ELSE 0 END) AS {books_status[1]}, '
    f'SUM(CASE WHEN book_status = \'{books_status[2]}\' THEN 1 ELSE 0 END) AS \'{books_status[2]}\', '
    f'SUM(CASE WHEN book_status = \'{books_status[3]}\' THEN 1 ELSE 0 END) AS \'{books_status[3]}\' '
    f'FROM {books_table} GROUP BY book_title, book_category'
)

# present book table
presenting_detail_books_table_string = f'SELECT * FROM {books_table}'

# present borrow book request table
presenting_books_to_be_borrowed_for_admin_string = (
    f'SELECT * FROM {books_table} '
    f'WHERE book_status = \'{books_status[2]}\' '
)

# present return book request table
presenting_books_to_be_returned_for_admin_string = (
    f'SELECT * FROM {books_table} '
    f'WHERE book_status = \'{books_status[3]}\' '
)

# present user table
presenting_detail_users_table_string = f'SELECT * FROM {users_table}'



#present books record summary for user
presenting_books_table_for_user_summary_user_string = (
    f'SELECT book_title, book_category, '
    f'SUM(CASE WHEN book_status = \'{books_status[0]}\' THEN 1 ELSE 0 END) AS {books_status[0]} '
    f'FROM {books_table} GROUP BY book_title, book_category'
)

#present books record summary for guest

# presents borrowed book for use
def presenting_borrowed_book_table_for_user_string(username): 
    return (
        f'SELECT * FROM {books_table} '
        f'WHERE borrowed_by = \'{username}\' '
        f' AND (book_status = \'{books_status[1]}\' '
        f' OR book_status = \'{books_status[3]}\')' 
    )



# add new user
def inserting_new_user_string(new_user, new_user_dob, new_user_occupation, new_user_address, new_user_password):
   return (
    f'INSERT INTO {users_table} (user_name, date_of_birth, occupation, address, password) '
    f'VALUES(\"{new_user}\",'
    f'\"{new_user_dob}\",'
    f'\"{new_user_occupation}\",'
    f'\"{new_user_address}\",'
    f'\"{lpf.hash_password(new_user_password)}\")'
   ) 

# password checking
def select_password_from_table(user):
    return f'SELECT password FROM users_table WHERE user_name = \"{user}\"'


# update table for borrowing request
def request_to_borrow(book_title, username):
    return (
        f'WITH book_to_borrow AS( '
        f'SELECT book_id FROM {books_table} '
        f'WHERE book_title = \"{book_title}\" '
        f'LIMIT 1) '
        f'UPDATE books_table '
        f'INNER JOIN book_to_borrow '
        f'USING(book_id) '
        f'SET '
        f'book_status = \"{books_status[2]}\", '
        f'borrowed_by = \"{username}\"'
    ) 

# update table for return request by user
def request_to_return(book_id, username):
    return (
        f'UPDATE books_table '
        f'SET book_status = \"{books_status[3]}\", '
        f'actual_returned_date = current_date() '
        f'WHERE book_id = \"{book_id}\"'
    )


# update table for approving borrowing request by admin
def approve_to_borrow(book_id):
    return (
        f'UPDATE books_table '
        f'SET book_status = \"{books_status[1]}\", '
        f'borrowed_date = current_date(), '
        f'expected_return_date = DATE_ADD(current_date(), INTERVAL 14 DAY) '
        f'WHERE book_id = \"{book_id}\"'
    )


def approve_to_return(book_id):
    return (
        f'UPDATE books_table '
        f'SET book_status = \"{books_status[0]}\", '
        f'borrowed_date = NULL, '
        f'expected_return_date = NULL, '
        f'actual_returned_date = NULL, '
        f'borrowed_by = NULL '
        f'WHERE book_id = \"{book_id}\"'
    )

# user update his/profile
def retrieve_user_data(username):
    return(
        f'SELECT * FROM users_table '
        f'WHERE user_name = \'{username}\''
    )

def updating_user_profile_string(username, loggedin_password, loggedin_user_address):
    return (
        f'UPDATE users_table '
        f'SET password = \"{lpf.hash_password(loggedin_password)}\", '
        f'address = \"{loggedin_user_address}\" '
        f'WHERE user_name = \"{username}\"'
    )

# search function
# admin search
def search_book_admin(search_keywords):
    return (
        f'{presenting_detail_books_table_string} '
        f'WHERE book_title LIKE \'%{search_keywords}%\''
    )

# admin search user
# presenting_detail_users_table_string    
def search_for_user_admin(search_user_keywords):
    return (
        f'{presenting_detail_users_table_string} '
        f'WHERE user_name LIKE \'%{search_user_keywords}%\''
    )


# user or guess search
def search_book_user(search_keywords):
    return(
        f'SELECT book_title, book_category, '
        f'SUM(CASE WHEN book_status = \'available\' THEN 1 ELSE 0 END) AS available_stock '
        f'FROM books_table WHERE book_title LIKE \'%{search_keywords}%\' '
        f'GROUP BY book_title, book_category'
    )
