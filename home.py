# for UI handling
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Database handling
import mysql.connector
from mysql.connector import Error

# Table handling
import pandas as pd

#local functions
import lms_sql_functions as lsf
import lms_python_functions as lpf

# Create container for notification of database setup
# create connection, create database/table if not exists
placeholder = st.empty()
with placeholder.container():
    #setup database: first setup server connection, create data
    db_connection = lsf.initial_setup(lsf.host, lsf.user, lsf.pw, lsf.db)
placeholder.empty() # clear notification


def main():
    """
    Manung Library
    """
    st.title("Manung Library")

    # create dropdown menu for table selection
    menu = ["Login", "SignUp", "Guest"]
    choice = st.sidebar.selectbox("Menu", menu)

    # if login menu is chosen, one can either login as admin or user
    if choice == "Login":
        st.subheader('Login Section')

        # Catch input variable username and password
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type = 'password')

        if st.sidebar.checkbox("Login"):
            #Admin section
            if username == "admin":
                # use admin table to check login info (for future)
                if password == "1234":
                    # supposed to retrieve hashed password from admin table (currently not implemented)
                    st.success("Login as Admin") # notification, new style
                    # open admin home page, consists of five tabs
                    tab1, tab2, tab3, tab4, tab5 = st.tabs([
                        "Register New Book",
                        "Books Borrow/Return Request",
                        "Books Collection",
                        "Add New User",
                        "Users List"
                    ])

                    # tab1: register new book
                    with tab1:
                        # Catch new variables (book title, category, stocks)
                        new_book_title = st.text_input("Book Title")
                        new_book_category = st.text_input("Book Category")
                        new_book_stocks = st.text_input("Numbers of Books")

                        if st.button("Add Book(s) in Library"):
                            # insert new book to database
                            lsf.insert_new_book(new_book_title, new_book_category, new_book_stocks, db_connection)
                            st.success("Book(s) added in Collection")

                    # tab2: books borrow/return request
                    with tab2:
                        #consists of two tabs: borrow and return
                        tab2_1, tab2_2 = st.tabs(["Request to Borrow", "Request to Return"])

                        # tab2_1: approving request to borrow
                        with tab2_1:
                            # check if books table is empty
                            if lsf.check_table_empty(db_connection, lsf.books_table) == 0:
                                st.info("No books collection yet")
                            else:
                                try:
                                    # retrieve table from books_table, where book_status = 'requested to be borrowed'
                                    book_requested_to_borrow_admin_view = lpf.detail_book_data_formatting(
                                        lsf.read_query_as_pd(
                                        db_connection, lsf.presenting_books_to_be_borrowed_for_admin_string
                                        )
                                    )
                                    # display table: present the result as AgGrid table in order to enable checkbox selection
                                    book_requested_to_borrow_admin_view_aggrid = lpf.df_to_aggrid(
                                        pd.DataFrame(book_requested_to_borrow_admin_view)
                                    )

                                    if st.button("Approve"):
                                        # Catch selected row, take book_id, search in book_table, change book status to 'borrowed'
                                        book_approve_to_be_borrowed = lpf.select_book_to_borrow_return(
                                            book_requested_to_borrow_admin_view_aggrid,
                                            column_name = 'Book ID'
                                        )
                                        lsf.execute_query(
                                            db_connection,
                                            lsf.approve_to_borrow(book_approve_to_be_borrowed[0]),
                                            lsf.success_user_request_approved_string
                                        )

                                except:
                                    st.info("No borrowing request from users")

                        with tab2_2:
                            # check if books table is empty
                            if lsf.check_table_empty(db_connection, lsf.books_table) == 0:
                                st.info("No books collection yet")

                            else:
                                try:
                                    # retrieve table from books_table, where book_status = 'to be approved for return'
                                    book_requested_to_return_admin_view = lpf.detail_book_data_formatting(
                                        lsf.read_query_as_pd(
                                        db_connection, lsf.presenting_books_to_be_returned_for_admin_string
                                        )
                                    )
                                    # display table: present the result as AgGrid table in order to enable checkbox selection
                                    book_requested_to_return_admin_view_aggrid = lpf.df_to_aggrid(
                                        pd.DataFrame(book_requested_to_return_admin_view)
                                    )

                                    if st.button("Approve"):
                                        # Catch selected row, take book_id, search in book_table, change book status to 'returned'
                                        book_approve_to_be_returned = lpf.select_book_to_borrow_return(
                                            book_requested_to_return_admin_view_aggrid,
                                            column_name = 'Book ID'
                                            )
                                        lsf.execute_query(
                                            db_connection,
                                            lsf.approve_to_return(book_approve_to_be_returned[0]),
                                            lsf.success_user_request_approved_string
                                        )

                                except:
                                    st.info("No returning request from users")

                    # tab3: books collection
                    with tab3:
                           
                        tab3_1, tab3_2 = st.tabs(["Collection Summary", "Books Details Table"])

                        # tab3_1: collection summary
                        with tab3_1:
                            # check if books table is empty
                            if lsf.check_table_empty(db_connection, lsf.books_table) == 0:
                                st.info("No books collection yet")

                            else:
                                # debug_book_data_summary_view = lsf.read_query_as_pd(db_connection, lsf.presenting_books_table_for_admin_summary_string)
                                # st.info(debug_book_data_summary_view)
                                
                                # present book table using SUM MySQL function to count numbers of available books, borrowed books, and total books
                                book_data_summary_view = lpf.book_data_admin_summary_view_formatting(
                                    lsf.read_query_as_pd(db_connection, lsf.presenting_books_table_for_admin_summary_string)
                                )
                                # display table: present the result
                                st.dataframe(book_data_summary_view)
                        
                        # tab3_2: books details table
                        with tab3_2:
                            # check if books table is empty
                            if lsf.check_table_empty(db_connection, lsf.books_table) == 0:
                                st.info("No books collection yet")

                            else:
                                # create search keyword variable
                                admin_search_keyword = st.text_input("Search Book")

                                if st.button("Search Book"):
                                    # catch search_keyword, retrieve book_table where book_title like %search_keyword%
                                    detail_book_data = lpf.detail_book_data_formatting(
                                        lsf.read_query_as_pd(
                                            db_connection,
                                            lsf.search_book_admin(admin_search_keyword)
                                        )
                                    )
                                    # display table: present the result
                                    st.dataframe(detail_book_data)

                                else:
                                    # present detail book_table
                                    detail_book_data = lpf.detail_book_data_formatting(
                                        lsf.read_query_as_pd(
                                            db_connection,
                                            lsf.presenting_detail_books_table_string
                                        )
                                    )
                                    # display table: present the result
                                    st.dataframe(detail_book_data)

                    # tab4: add new user
                    with tab4:
                        new_user_by_admin = st.text_input("username")
                        new_password_by_admin = st.text_input("New Password by Admin", type='password')
                        new_user_dob_by_admin = st.text_input("Date of Birth (YYYY-MM-DD)")
                        new_user_occupation_by_admin = st.text_input("Occupation")
                        new_user_address_by_admin = st.text_input("Address")

                        if st.button("Add New User"):
                            # check if username already exists in user table
                            check_user_name_from_users_table = lsf.read_query_as_pd(
                                db_connection,
                                lsf.check_user_name(new_user_by_admin)
                            )
                            print(check_user_name_from_users_table)
                            st.info(check_user_name_from_users_table)

                            # if username does not exist, insert new user to user table
                            if check_user_name_from_users_table.empty or new_user_by_admin != "admin":

                                # if password and date_of_birth are not empty
                                if len(new_password_by_admin) and len(new_user_dob_by_admin) >0:
                                    # update users_table with new user
                                    lsf.execute_query(
                                        db_connection,
                                        lsf.inserting_new_user_string(
                                            new_user_by_admin,
                                            new_user_dob_by_admin,
                                            new_user_occupation_by_admin,
                                            new_user_address_by_admin,
                                            new_password_by_admin
                                        ),
                                        lsf.success_new_user_added_byadmin_string 
                                    )


                                else:
                                    st.error("Password and Date of Birth cannot be empty")

                            else:
                                st.error("Username already exists or not permitted")

                    # Shows library users list
                    with tab5:
                        if lsf.check_table_empty(db_connection, lsf.users_table) == 0:
                            st.info("No library users yet")
                        
                        else:
                            search_user_keyword = st.text_input("Search User")

                            if st.button('Search User'):
                                st.info("Search user based on username")

                                detail_user_data = lpf.user_data_formatting(
                                    lsf.read_query_as_pd(
                                        db_connection,
                                        lsf.search_for_user_admin(search_user_keyword)
                                    )
                                )   
                                st.dataframe(detail_user_data)
                            else:
                                # present user table
                                detail_user_data = lpf.user_data_formatting(
                                    lsf.read_query_as_pd(
                                        db_connection,
                                        lsf.presenting_detail_users_table_string
                                    )
                                )
                                st.dataframe(detail_user_data)

                else:
                    st.warning("Incorrect username/password")

            # User section
            # Use users table
            else:
                # check if username exists in users table
                check_user_name_from_users_table = lsf.read_query_as_pd(
                    db_connection,
                    lsf.check_user_name(username)
                )

                # if query return empty, check password
                if not check_user_name_from_users_table.empty:

                    # retrieve hashed password from users table
                    saved_password_from_db = lsf.read_query_as_pd(
                        db_connection,
                        lsf.select_password_from_table(username)
                    )
                    hashed_password_input = lpf.hash_password(password)

                    # if hashed password from input == hashed password from database, login success
                    if saved_password_from_db.iloc[0][0] == hashed_password_input:
                        st.success(f'Login as {username}')
                        # user section tabs:
                        tab1, tab2, tab3 = st.tabs([
                            "Library Books Collection",
                            "Borrowed Book",
                            "Profile"
                        ])

                        with tab1:

                            # check if books table is empty
                            if lsf.check_table_empty(db_connection, lsf.books_table) == 0:
                                st.info("No books collection yet")
                            else:
                                # create search keyword variable
                                user_search_keyword = st.text_input("Search Book")

                                # create search_state to prevent table resetting when clicked
                                if 'search_state' not in st.session_state:
                                    st.session_state.search_state = False

                                if st.button("Search Book") or st.session_state.search_state:
                                    st.session_state.search_state = True

                                    st.info('Search book based on book title')
                                    # retrieve table based on user search keyword
                                    book_data_user_search_view = lpf.book_data_user_summary_view_formatting(
                                        lsf.read_query_as_pd(
                                            db_connection,
                                            lsf.search_book_user(user_search_keyword)
                                        )
                                    )

                                    # Present table as AgGrid table to allow book selection using checkbox
                                    book_userview_aggrid = lpf.df_to_aggrid(
                                        pd.DataFrame(book_data_user_search_view)
                                    )

                                else:
                                    # Present table with book title, category and numbers of available stock
                                    book_data_user_view = lpf.book_data_user_summary_view_formatting(
                                        lsf.read_query_as_pd(
                                            db_connection,
                                            lsf.presenting_books_table_for_user_summary_string
                                        )
                                    )

                                    book_userview_aggrid = lpf.df_to_aggrid(
                                        pd.DataFrame(book_data_user_view)
                                    )

                                if st.button("Request to borrow"):
                                    # Catch selected row, take book_id, search in book_table, change book status to 'requested to be borrowed'
                                    book_request_to_borrow_stock = lpf.select_book_to_borrow_return(
                                        book_userview_aggrid,
                                        column_name = 'Available Stock'
                                    )
                                    book_request_to_borrow = lpf.select_book_to_borrow_return(
                                        book_userview_aggrid,
                                        column_name = 'Book Title'
                                    )
                                    
                                    # Request to borrow is processed if available stock >= 1
                                    if book_request_to_borrow_stock.iloc[0] >= 1:
                                        lsf.execute_query(
                                            db_connection,
                                            lsf.request_to_borrow(book_request_to_borrow[0], username),
                                            lsf.success_request_to_borrow_string
                                        )
                                    else:
                                        st.warning("The selected book is not available")

                        with tab2:
                            try:
                                # select from books_table where borrowed by user, status borrowed
                                borrowed_book_data_user_view  = lpf.detail_book_data_formatting(
                                    lsf.read_query_as_pd(
                                        db_connection,
                                        lsf.presenting_borrowed_book_table_for_user_string(username)
                                    )
                                )
                                # display table: present the result
                                borrowed_book_data_user_view_aggrid = lpf.df_to_aggrid(
                                    pd.DataFrame(borrowed_book_data_user_view)
                                )

                                # submit book return request
                                if st.button("Return book(s)"):
                                    # select book to be returned, change the book_status to be 'to be approved for return'
                                    book_request_to_return = lpf.select_book_to_borrow_return(
                                        borrowed_book_data_user_view_aggrid,
                                        column_name = 'Book ID'
                                    )
                                    lsf.execute_query(
                                        db_connection,
                                        lsf.request_to_return(book_request_to_return[0], username),
                                        lsf.success_request_to_return_string
                                    )
                            except:
                                st.info("No borrowed book")

                        with tab3:
                            # user profile setting: changing password and address
                            loggedin_password = st.text_input("New Password by user", type='password')
                            loggedin_user_address = st.text_input("New Address by User")

                            if st.button("Update Profile"):
                                # update users_table with new user data
                                lsf.execute_query(
                                    db_connection,
                                    lsf.updating_user_profile_string(
                                        username,
                                        loggedin_password,
                                        loggedin_user_address
                                    ),
                                    lsf.success_updated_profile_string 
                                )

                                profile_data = lpf.user_data_formatting(
                                    lsf.read_query_as_pd(
                                        db_connection,
                                        lsf.retrieve_user_data(username)
                                    )
                                )

                                st.dataframe(profile_data)

                    else:
                        st.warning("Incorrect username/password")

                else:
                    st.error('username does not exist')

    elif choice == "SignUp":
        st.subheader("Create New Account")
        # similiar process with new user addition from admin above
        new_user = st.text_input("username")
        new_password = st.text_input("Password", type='password')
        new_user_dob = st.text_input("tanggal Lahir")
        new_user_occupation = st.text_input("Occupation")
        new_user_address = st.text_input("address")

        if st.button("Signup"):
            if new_user != "admin":
                # Compare if username already exists in the table
                check_user_name_from_users_table = lsf.read_query_as_pd(
                    db_connection,
                    lsf.check_user_name(new_user)
                )

                # if username does not exist, insert new user to user table
                if check_user_name_from_users_table.empty and new_user != 'admin':
                    st.info("Username available")
                    # if password and date_of_birth are not empty
                    if len(new_password) and len(new_user_dob) > 0:
                        # update users_table with new user
                        lsf.execute_query(
                            db_connection,
                            lsf.inserting_new_user_string(
                                new_user,
                                new_user_dob,
                                new_user_occupation,
                                new_user_address,
                                new_password
                            ),
                            lsf.success_signup_string 
                        )

                    else:
                        st.error("Password and Date of Birth cannot be empty")

                else:
                    st.error("Username already exists or not permitted")

            else:
                st.warning("Username admin cannot be used")

    else:
        st.subheader("Browse as a Guest")
        st.success("You can browse our collection as a Guest")

        # check if books table is empty
        if lsf.check_table_empty(db_connection, lsf.books_table) == 0:
            st.info("No books collection yet")

        else:
            # similiar process with user browse collection functions above, without the book selection checkbox
            guest_search_keyword = st.text_input('Search Books')
                            
            if st.button('Search Book'):
                
                st.info('search book based on title')
                book_data_guest_search_view = lpf.book_data_user_summary_view_formatting(
                    lsf.read_query_as_pd(
                        db_connection, lsf.search_book_user(guest_search_keyword)
                        )
                ) 
                st.dataframe(book_data_guest_search_view)
                

            else:
                
                book_data_guest_search_view = lpf.book_data_user_summary_view_formatting(
                    lsf.read_query_as_pd(
                        db_connection, lsf.presenting_books_table_for_user_summary_string
                        )
                )

                st.dataframe(book_data_guest_search_view)

    with st.sidebar:
        # Check if database connection is active
        if db_connection.is_connected():
            st.success("Database connected")
        else:
            st.warning("Database not connected")

        

if __name__ == '__main__':
    main()
