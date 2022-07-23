import streamlit as st
import mysql.connector 
from mysql.connector import Error
import pandas as pd
import lms_sql_functions as lsf
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import hashlib

# Detail books data formatting
def detail_book_data_formatting(book_data):
    book_data.rename(columns = {
        0 : 'Book ID',
        1 : 'Book Title',
        2 : 'Category',
        3 : 'Status',
        4 : 'Borrowed Date',
        5 : 'Expected Return Date',
        6 : 'Returned Date',
        7 : 'Requested or Borrowed By'
    }, inplace = True)
    return book_data

def book_data_admin_summary_view_formatting(book_data_admin_summary_view):
    book_data_admin_summary_view.rename(columns = {
        0 : 'Book Title',
        1 : 'Book Category',
        2 : 'Available',
        3 : 'Borrowed',
        4 : 'Requested to be Borrowed',
        5 : 'To be Approved for Return'
    }, inplace = True)

    book_data_admin_summary_view = book_data_admin_summary_view.astype({
    'Available': int, 
    'Borrowed': int,
    'Requested to be Borrowed': int,
    'To be Approved for Return': int
    })

    book_data_admin_summary_view['Total Stock'] = book_data_admin_summary_view.iloc[:, 2:6].sum(axis = 1)

    return book_data_admin_summary_view

def book_data_user_summary_view_formatting(book_data_user_summary_view):
    book_data_user_summary_view.rename(columns = {
        0 : 'Book Title',
        1 : 'Book Category',
        2 : 'Available Stock'
    }, inplace = True)

    book_data_user_summary_view = book_data_user_summary_view.astype({
    'Available Stock': int, 
    })

    return book_data_user_summary_view


# Detail users data formatting
def user_data_formatting(user_data):
    user_data.rename(columns = {
        0 : 'User ID',
        1 : 'user Name',
        2 : 'Date of Birth',
        3 : 'Occupation',
        4 : 'Address',
        5 : 'Password'
    }, inplace = True)

    return user_data

# user authentification
def hash_password(password):
    return hashlib.sha3_256(password.encode()).hexdigest()
 
def check_password(user, hashed_password):
    saved_password = lsf.read_query(
        lsf.db_connection, 
        lsf.select_password_from_table())
    return saved_password == hashed_password

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

