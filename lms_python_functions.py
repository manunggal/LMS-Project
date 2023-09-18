import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
import lms_sql_functions as lsf
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import hashlib

# Details book data formatting
def detail_book_data_formatting(book_data):
    book_data.rename(columns={
        0: 'Book ID', 
        1: 'Book Title', 
        2: 'Category', 
        3: 'Status', 
        4: 'Borrowed Date', 
        5: 'Expected Return Date',
        6: 'Returned Date',
        7: 'Requested or Borrowed By'}, 
        inplace=True)
    return book_data

# Present stock summary table for admin view
def book_data_admin_summary_view_formatting(book_data_admin_summary_view):
    book_data_admin_summary_view.rename(columns={
        0: 'Book Title',
        1: 'Book Category',
        2: 'Available',
        3: 'Borrowed',
        4: 'Requested to be Borrowed',
        5: 'To be Approved for Return'},
        inplace=True)
    
    book_data_admin_summary_view = book_data_admin_summary_view.astype({
        'Available': 'int',
        'Borrowed': 'int',
        'Requested to be Borrowed': 'int',
        'To be Approved for Return': 'int'
    })

    book_data_admin_summary_view['Total Stock'] = book_data_admin_summary_view.iloc[:, 2:6].sum(axis=1)
    return book_data_admin_summary_view

# Present available stock summary table for user and guest view
def book_data_user_summary_view_formatting(book_data_user_summary_view):
    book_data_user_summary_view.rename(columns={
        0: 'Book Title',
        1: 'Book Category',
        2: 'Available Stock'},
        inplace=True)
    
    book_data_user_summary_view = book_data_user_summary_view.astype({
        'Available Stock': 'int'
    })

    return book_data_user_summary_view

# Detail users data formatting
def user_data_formatting(user_data):
    user_data.rename(columns={
        0: 'User ID', 
        1: 'User Name', 
        2: 'Date of Birth', 
        3: 'Occupation', 
        4: 'Address', 
        5: 'Password'}, 
        inplace=True)
    return user_data

# User Authentication
def hash_password(password):
    return hashlib.sha3_256(password.encode()).hexdigest()

def check_password(user, hashed_password):
    saved_password = lsf.read_query(
        lsf.db_connection,
        lsf.select_password_from_table()
    )
    return saved_password == hashed_password

# check date of birth format (YYYY-MM-DD)
def check_dob_format(new_dob):
    if len(new_dob) != 10:
        raise Exception('Date of birth format is incorrect. Please enter in YYYY-MM-DD format.')
    
    try:
        # check year within mysql accepted year range (1000 - 9999)
        year_check = 1000 <= int(new_dob[0:4]) <= 9999
        # check month within mysql accepted month range (01 - 12)
        month_check = 1 <= int(new_dob[5:7]) <= 12
        # check day within mysql accepted day range (01 - 31)
        day_check = 1 <= int(new_dob[8:10]) <= 31
        # dash check
        dash_check = (new_dob[4] == '-' and new_dob[7] == '-')

        return year_check and month_check and day_check and dash_check
    except:
        raise Exception('Date of birth format is incorrect. Please enter in YYYY-MM-DD format.')

# convert pd.dataframe to aggrid    
def df_to_aggrid(df):
    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_selection(selection_mode='single',use_checkbox=True)
    grid_table = AgGrid(df, gridOptions=gd.build(),update_mode=GridUpdateMode.SELECTION_CHANGED)
    return grid_table

# save selected book
def select_book_to_borrow_return(grid_table, column_name):
    selected_book = pd.DataFrame(grid_table['selected_rows'])[column_name]
    return selected_book
