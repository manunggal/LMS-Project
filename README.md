# LMS-Project

## Introduction
This is a fourth assignment of Python class from data science course at [Pacmann](https://pacmann.io/). It is arranged to illustrate the functionality of python with MySQL database. LMS stands for Library Management Project, this app is designed to manage the administration of a suppose to be a library at Pacmann. Basic functionality covers adding new books into the collection, searching for books, adding new users and viewing books status, etc.

## Requirements
The required package is listed in ```requirements.txt```. Along with the general best practice of setting up local environment, those packages need to be installed prior to the utilization of this app. The virtual environment or ```venv``` can be set up within your local working directory using  ```python -m venv LMS-Project``` command. The virtual environment will be created and contained within a directory called ```LMS-Project```. Afterwards it can be activated via ```./Scripts/activate```. ```pip install``` command can be used to install the required packages. ```mysql-connector-python``` is used to handle the connection and operation of the MySQL database from python, whereas the creation of the UI aspect is managed using ```streamlit``` a powerful framework to create machine learning and data science app. you can learn more about it at  [Streamlit](https://streamlit.io/). A Streamlit extension called ```streamlit-aggrid``` helps to create an interactive table. in this app, it is used to create a table book where user can select a book to borrow. Finally ```pandas``` is used to handle the tables coming out of the MySQL database.


```
# For UI handling
import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
# Database handling
import mysql.connector 
from mysql.connector import Error
# Table handling
import pandas as pd
# local functions
import lms_sql_functions as lsf
import lms_python_functions as lpf
```

## How it works
The app is divided into three section, which are:
- Admin Section
  As an administrator, user can add new book, add new user, browse collection in a more detailed fashion. an admin also serve to approve book borrowing request and confiriming returning books.
- User Section
  a user or a library member can browse collection, search for a book with a keyword for book title, and editing his/her profile
- Guest Section
  as a guest, one can only browse the collection or search for a book 

### Admin Section
The sidebar is where user log the information in accordance with their respective role, it accepts two inputs which are `username` and `password`.
![Admin Login](https://github.com/manunggal/LMS-Project/blob/master/readme%20pics/admin_login.jpg)
In general the user authentification aspect of this app is not part of the assignment, hence in the current version the authentification of admin is simplified as:
```
if st.sidebar.checkbox("Login"):
            # Admin Section
            if username == "admin":
                # supposed to use admin_table to check login info
                if password == "1234":
                    # supposed to retrieve hashed password from admin_table
                    st.success("Logged as Admin")
                    # Open admin home page
```
if `username` input is 'admin' and `password` input is '1234', the app will present the admin page.
admin picture. The following code delivers the admin page
```
# Open admin home page
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Register New Book", 
    "Books Borrow/Return Request",
    "Books Collection", 
    "Add New user",
    "Users List"])
```
 It consists of five tabs, each tab will open a new page corresponding to the respective tab name.
 
#### Register New Book
In this tab, the admin can add new book to the collection. the following code from `home.py` 
`with tab1: # Register New Book
                        new_book_title = st.text_input("Book Title")
                        new_book_category = st.text_input("Book Category")
                        new_book_stock = st.text_input("Numbers of Books")

                        if st.button("Add Book(s) in Library"):
                            lsf.insert_new_book(new_book_title, new_book_category, new_book_stock, lsf.db_connection)

                            st.success("Book(s) added in Collection")`
will generate the following tab

gambar lagi

The input of `new_book_title`, etc will be executed as MySQL query using code 
`# function to insert new book to database by admin
def insert_new_book(new_book_title, new_book_category, new_book_stock, db_connection):
    sql_string = (
        f'INSERT INTO {books_table} (book_title, book_category, book_status) '
        f'VALUES (\"{new_book_title}\",\"{new_book_category}\", \"available\")'
    )

    for i in range(0, int(new_book_stock)):
        execute_query(db_connection, sql_string)`
        
from` lms_sql_functions.py` when the `st.button("Add Book(s) in Library")` is clicked. Within this block of code, the number of books to be added will be based  on `new_book_stock` input. For each new book, a `book_id` number is generated automatically using auto increment feature that was set-up during MySQL table creation.

#### Book Borrow/Return Request
Both books borrow or return tab will display the following message when there are no such request from library users.
gambar st.info borrow request

`with tab2: # Book Borrow/Return Request
                        tab2_1, tab2_2 = st.tabs([
                            "Request to Borrow",
                            "Request to Return"
                        ])
                        
                        with tab2_1:
                            try:

                                book_requested_to_borrow_admin_view = lpf.detail_book_data_formatting(
                                    lsf.read_query_as_pd(
                                        lsf.db_connection, lsf.presenting_books_to_be_borrowed_for_admin_string
                                    )
                                )
                                book_requested_to_borrow_admin_view_aggrid = lpf.df_to_aggrid(pd.DataFrame(book_requested_to_borrow_admin_view))
                        

                                if st.button("Approve"):
                                    book_approve_to_be_borrowed = lpf.select_book_to_borrow_return(book_requested_to_borrow_admin_view_aggrid, column_name='Book ID')
                                    st.write(book_approve_to_be_borrowed[0])
                                    lsf.execute_query(
                                        lsf.db_connection,
                                        lsf.approve_to_borrow(book_approve_to_be_borrowed[0])
                                    )
                                    st.success("User's request approved")
                            
                            except:
                                st.info("No borrowing request from users")
`

When there are such requests, a function:

`# present borrow book request table
presenting_books_to_be_borrowed_for_admin_string = (
    f'SELECT * FROM {books_table} '
    f'WHERE book_status = \'{books_status[2]}\' '
)`

from `lms_sql_functions.py` will retrieve the table from database and present it to the admin, where function `detail_book_data_formatting` from `lms_python_functions.py` will format the table's column names. Meanwhile function `df_to_aggrid` from `lms_python_functions.py` will convert `pandas` `dataframe` to `Aggrid` `dataframe` in order to create interactive table where the admin can select which request to be approved using a checkbox.
The handling of this request is executed after admin click the `approve` button from `if st.button("Approve"):` code where `book title` is captured from the selected row and used as a query is sent to the database using 
The same process will also happens for the borrow request tab. 




#### Books Collection
#### Add New User
#### Users List
### User Section
#### Browse and Search Collection
#### Borrowed Books
#### Profile Update
### Guest Section
