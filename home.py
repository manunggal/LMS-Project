# For UI handling
import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
# Database handling
import mysql.connector 
from mysql.connector.errors import Error
# Table handling
import pandas as pd
# local functions
import lms_sql_functions as lsf
import lms_python_functions as lpf




# create container for notification of database setup (create connection, create database/table if not exists)
placeholder = st.empty()
with placeholder.container():
    # setup database: first setup server connection, create database, create database connection, create users and books table if not exists 
    db_connection = lsf.initial_setup(lsf.host, lsf.user, lsf.pw, lsf.db)
placeholder.empty() #clear notification




def main():
    """
    Pacmann Library
    """
    st.title("Pacmann Library")

    # create dropdown menu
    menu = ["Login", "SignUp", "Guest"]
    choice = st.sidebar.selectbox("Menu", menu)

    # if login menu is chosen, one can either login as admin or user
    if choice == "Login":
        st.subheader('Login Section')

        # catch input variable username and password
        username = st.sidebar.text_input("user Name")
        password = st.sidebar.text_input("Password", type= "password")

        if st.sidebar.checkbox("Login"):
            # Admin Section
            if username == "admin":
                # Use admin table to check login info (for future)
                if password == "1234":
                    # supposed to retrieve hashed password from admin table (currently not)
                    st.success("Login as Admin")
                    # Open admin home page, consists of five tabs
                    tab1, tab2, tab3, tab4, tab5 = st.tabs([
                        "Register New Book", 
                        "Books Borrow/Return Request",
                        "Books Collection", 
                        "Add New user",
                        "Users List"])

                    with tab1: # Register New Book
                        # Catch new variables (book title, category, and stocks)
                        new_book_title = st.text_input("Book Title")
                        new_book_category = st.text_input("Book Category")
                        new_book_stock = st.text_input("Numbers of Books")

                        if st.button("Add Book(s) in Library"): # update books_table with new book
                            lsf.insert_new_book(new_book_title, new_book_category, new_book_stock, db_connection)
                            st.success("Book(s) added in Collection")
                        

                    with tab2: # Book Borrow/Return Request
                        # consist of two sub-tabs:
                        tab2_1, tab2_2 = st.tabs([
                            "Request to Borrow",
                            "Request to Return"
                        ])
                        
                        with tab2_1: # for approving books borrowing request
                            
                            # check if books table is empty 
                            if lsf.check_table_empty(db_connection, lsf.books_table) == 0:
                                st.info('No books collection yet')

                            else:

                                try:
                                    # retrieve table from books_table, where book_status = 'requested to be borrowed'
                                    book_requested_to_borrow_admin_view = lpf.detail_book_data_formatting(
                                        lsf.read_query_as_pd(
                                            db_connection, lsf.presenting_books_to_be_borrowed_for_admin_string
                                        )
                                    )
                                    # presents the result as AgGrid table in order to enable checkbox selection 
                                    book_requested_to_borrow_admin_view_aggrid = lpf.df_to_aggrid(pd.DataFrame(book_requested_to_borrow_admin_view))
                            

                                    if st.button("Approve"):
                                        # catch selected row, take book_id, search in book_table, change book_status to 'borrowed'
                                        book_approve_to_be_borrowed = lpf.select_book_to_borrow_return(book_requested_to_borrow_admin_view_aggrid, column_name='Book ID')
                                        lsf.execute_query(
                                            db_connection,
                                            lsf.approve_to_borrow(book_approve_to_be_borrowed[0]),
                                            lsf.success_user_request_approved_string
                                        )
                                                                
                                except:
                                    st.info("No borrowing request from users")

                        with tab2_2: # for confirming book return request

                            # check if books table is empty 
                            if lsf.check_table_empty(db_connection, lsf.books_table) == 0:
                                st.info('No books collection yet')

                            else:

                                try:
                                    # retrieve table from books_table, where book_status = 'to be approved for return'
                                    book_requested_to_return_admin_view = lpf.detail_book_data_formatting(
                                        lsf.read_query_as_pd(
                                            db_connection, lsf.presenting_books_to_be_returned_for_admin_string
                                        )
                                    )
                                    # presents the result as AgGrid table in order to enable checkbox selection 
                                    book_requested_to_return_admin_view_aggrid = lpf.df_to_aggrid(pd.DataFrame(book_requested_to_return_admin_view))


                                    if st.button("Approve"):
                                        # catch selected row, take book_id, search in book_table, change book_status to 'available'
                                        book_approve_to_be_returned = lpf.select_book_to_borrow_return(book_requested_to_return_admin_view_aggrid, column_name='Book ID')
                                        lsf.execute_query(
                                            db_connection,
                                            lsf.approve_to_return(book_approve_to_be_returned[0]),
                                            lsf.success_user_request_approved_string
                                        )

                                except:
                                    st.info("No returning request from users")


                    with tab3: # Shows Books Collection
                        # create sub tabs
                        tab3_1, tab3_2 = st.tabs([
                            "Collection Summary",
                            "Books Details Table"
                        ])

                        with tab3_1:  
                            # check if books table is empty 
                            if lsf.check_table_empty(db_connection, lsf.books_table) == 0:
                                st.info('No books collection yet')

                            else: 
                                                         
                                # present book_table using SUM MySQL function to count numbers of available book, borrowed, etc.
                                book_data_summary_view = lpf.book_data_admin_summary_view_formatting(
                                    lsf.read_query_as_pd(
                                        db_connection, lsf.presenting_books_table_for_admin_summary_string
                                    )
                                )
                                st.dataframe(book_data_summary_view)
                        
                        with tab3_2:
                            # check if books table is empty
                            if lsf.check_table_empty(db_connection, lsf.books_table) == 0:
                                st.info('No books collection yet')
                            
                            else:                          
                                # create search_keyword variable 
                                admin_search_keyword = st.text_input("Search Book")

                                if st.button('Search Book'):
                                    # catch search_keyword, retrieve book_table where book_title like %search_keyword%  
                                    detail_book_data = lpf.detail_book_data_formatting(
                                        lsf.read_query_as_pd(
                                            db_connection, lsf.search_book_admin(admin_search_keyword)
                                        )
                                    )
                                    
                                    st.dataframe(detail_book_data)
                                
                                else:
                                    # present detail book_table
                                    detail_book_data = lpf.detail_book_data_formatting(
                                        lsf.read_query_as_pd(
                                            db_connection, lsf.presenting_detail_books_table_string
                                        )
                                    )
                                    
                                    st.dataframe(detail_book_data)
                    
                    with tab4: # Add new user 
                        # create new user variables
                        new_user_by_admin = st.text_input("username")
                        new_password_by_admin = st.text_input("New Password by Admin", type='password')
                        new_user_dob_by_admin = st.text_input("Date of Birth (YYYY-MM-DD)")
                        new_user_occupation_by_admin = st.text_input("Occupation")
                        new_user_address_by_admin = st.text_input("Address")
                        
                        if st.button("Add new user"):
                            # compare if username already exists in the table
                            check_user_name_from_users_table = lsf.read_query_as_pd(
                                db_connection, lsf.check_user_name(new_user_by_admin)    
                            )
                            # if username does not exists
                            if check_user_name_from_users_table.empty and new_user_by_admin != 'admin':
                                
                                # if password and date of birth not empty
                                if len(new_password_by_admin) and len(new_user_dob_by_admin) > 0:
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
                                    st.error('Password and Date of Birth cannot be empty')

                            else:
                                st.error("Username already exists or not permitted")

                        
                    with tab5: # Shows Library user List

                        # check if books table is empty 
                        if lsf.check_table_empty(db_connection, lsf.users_table) == 0:
                            st.info('No library users yet')
                            
                        else:

                            search_user_keyword = st.text_input("Search User")
                            
                            if st.button('Search User'): # catch user keyword, search users_table where user_name like keyword 
                                st.info('search user based on username')
                            
                                detail_user_data = lpf.user_data_formatting(
                                    lsf.read_query_as_pd(
                                        db_connection, lsf.search_for_user_admin(search_user_keyword)
                                    )
                                )
                                st.dataframe(detail_user_data) 

                            else:
                                # present user table
                                detail_user_data = lpf.user_data_formatting(
                                    lsf.read_query_as_pd(
                                        db_connection, lsf.presenting_detail_users_table_string
                                    )
                                )

                                st.dataframe(detail_user_data) 
                        

                else:
                    st.warning("Incorrect username/Password")

            # user/user Section
            else: # use user table
                # check if username exist
                check_user_name_from_users_table = lsf.read_query_as_pd(
                    db_connection, lsf.check_user_name(username)    
                )
                
                if not check_user_name_from_users_table.empty: # if query return empty, check password

                    # retrieve hashed password from user table
                    saved_password_from_db = lsf.read_query_as_pd(db_connection, lsf.select_password_from_table(username))
                    hashed_password_input = lpf.hash_password(password)
                                    
                    if saved_password_from_db.iloc[0][0] == hashed_password_input:  # check if input password for user = password in table
                        st.success(f'Login as {username}')
                        # user section tabs:
                        tab1, tab2, tab3 = st.tabs([
                            "Library Books Collection", 
                            "Borrowed Books",
                            "Profile"
                        ])

                        with tab1:

                            # check if books table is empty 
                            if lsf.check_table_empty(db_connection, lsf.books_table) == 0:
                                st.info('No books collection yet')

                            else:

                                # catch search keyword
                                user_search_keyword = st.text_input('Search Books')
                                
                                # create search_state to prevent table resetting when clicked
                                if 'search_state' not in st.session_state:
                                    st.session_state.search_state = False

                                if st.button('Search Book') or st.session_state.search_state: 
                                    st.session_state.search_state = True

                                    st.info('search book based on title')
                                    # retrieve table based on user search word
                                    book_data_user_search_view = lpf.book_data_user_summary_view_formatting(
                                        lsf.read_query_as_pd(
                                            db_connection, lsf.search_book_user(user_search_keyword)
                                            )
                                    ) 
                                    # present table as AgGrid table to allow book selection using checkbox
                                    book_userview_aggrid = lpf.df_to_aggrid(pd.DataFrame(book_data_user_search_view))

                                else:
                                    # present table with book title, category and numbers of available stock
                                    book_data_user_view = lpf.book_data_user_summary_view_formatting(
                                        lsf.read_query_as_pd(
                                            db_connection, lsf.presenting_books_table_for_user_summary_user_string
                                            )
                                    )

                                    book_userview_aggrid = lpf.df_to_aggrid(pd.DataFrame(book_data_user_view))
                                                                        
                                if st.button("Request to borrow"):
                                    # select 1 book of the selected book_title, change the book_status to be 'requested to be borrowed'
                                    book_request_to_borrow_stock = lpf.select_book_to_borrow_return(book_userview_aggrid, column_name = 'Available Stock') 
                                    book_request_to_borrow = lpf.select_book_to_borrow_return(book_userview_aggrid, column_name = 'Book Title') 
                                    
                                    # request to borrow is processed if available stock >= 1
                                    if book_request_to_borrow_stock.iloc[0] >= 1:
                                    
                                        lsf.execute_query(
                                            db_connection,
                                            lsf.request_to_borrow(
                                                book_request_to_borrow[0], 
                                                username),
                                            lsf.success_request_to_borrow_string
                                            )
                                    
                                    else:
                                        st.warning('The selected book is not available')

                        with tab2:
                            try:
                                # select from books_table where borrowed by user, status borrowed
                                borrowed_book_data_user_view = lpf.detail_book_data_formatting(
                                    lsf.read_query_as_pd(
                                        db_connection, lsf.presenting_borrowed_book_table_for_user_string(username)
                                    )
                                )


                                borrowed_book_data_user_view_aggrid = lpf.df_to_aggrid(pd.DataFrame(borrowed_book_data_user_view))
                                
                                
                                # submit book return request
                                if st.button("Return book(s)"):
                                    # select book to be return, change the book_status to be 'to be approved for return'
                                    book_request_to_return = lpf.select_book_to_borrow_return(borrowed_book_data_user_view_aggrid, column_name='Book ID') 
                                    lsf.execute_query(
                                        db_connection,
                                        lsf.request_to_return(
                                            book_request_to_return[0], 
                                            username),
                                        lsf.success_request_to_return_string
                                    )

                            except:
                                st.info("You haven't borrowed any yet")                    
                            

                        with tab3:
                            # catch password and address to be updated
                            loggedin_password = st.text_input("New Password by user", type='password')
                            loggedin_user_address = st.text_input("New Address by user")
                            
                            if st.button("Update profile"):
                                # update column password and or address from users_table where user_name = username
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
                                    db_connection, lsf.retrieve_user_data(username)
                                )
                            )
                            
                            st.dataframe(profile_data)     

                    else:
                        st.warning("Incorrect username/Password")
                
                else:
                    st.error('username does not exist')

    elif choice == "SignUp":
        st.subheader('Create New Account')
        # similiar process with new user addition from admin above
        new_user = st.text_input("username")
        new_password = st.text_input("Password", type='password')
        new_user_dob = st.text_input("tanggal Lahir")
        new_user_occupation = st.text_input("Occupation")
        new_user_address = st.text_input("address")
        
        if st.button("Signup"):
            if new_user != "admin":
                # compare if username already exists in the table
                check_user_name_from_users_table = lsf.read_query_as_pd(
                                db_connection, lsf.check_user_name(new_user)    
                            )
                # if username does not exists
                if check_user_name_from_users_table.empty and new_user_by_admin != 'admin':

                    # if password and date of birth not empty
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
                        st.error('Password and Date of Birth cannot be empty')

                else:
                    st.error("Username already exists or not permitted")

            else:
                st.warning("username admin cannot be used")

    else:
        st.subheader('Browse as a Guest')
        st.success("You can browse our collection as a guest")

        # check if books table is empty 
        if lsf.check_table_empty(db_connection, lsf.books_table) == 0:
            st.info('No books collection yet')

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
                        db_connection, lsf.presenting_books_table_for_user_summary_user_string
                        )
                )

                st.dataframe(book_data_guest_search_view)
                

    with st.sidebar:
        # Check if database connection is active
        if db_connection.is_connected():
            st.info('Connected to Database')
        else:
            st.warning('No Database connection')
        
        

if __name__ == '__main__':
    main()




