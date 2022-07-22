import streamlit as st
import mysql.connector 
from mysql.connector import Error
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

import lms_sql_functions as lsf
import lms_python_functions as lpf




# from streamlit import caching

# koneksi ke server
server_connection = lsf.create_server_connection(lsf.host, lsf.user, lsf.pw)

# create database
lsf.execute_query(server_connection, lsf.creating_database_string) # create database if not exists

# create database and table if not exist

lsf.execute_query(lsf.db_connection, lsf.creating_admin_table_string) # create admin table  if not exists
lsf.execute_query(lsf.db_connection, lsf.creating_users_table_string) # create user table if not exists
lsf.execute_query(lsf.db_connection, lsf.creating_books_table_string) # create book table if not exists

st.set_page_config(page_title = "Home")

def main():
    """
    Pacmann Library
    """
    st.title("Pacmann Library")

    menu = ["Login", "SignUp", "Guest"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader('Login Section')

        username = st.sidebar.text_input("user Name")
        password = st.sidebar.text_input("Password", type= "password")

        if st.sidebar.checkbox("Login"):
            # Admin Section
            if username == "admin":
                # Use admin table to check login info
                if password == "1234":
                    # retrieve hashed password from admin table
                    st.success("Logged as Admin")
                    # Open admin home page
                    tab1, tab2, tab3, tab4, tab5 = st.tabs([
                        "Register New Book", 
                        "Books Borrow/Return Request",
                        "Books Collection", 
                        "Add New user",
                        "Users List"])

                    with tab1: # Register New Book
                        new_book_title = st.text_input("Book Title")
                        new_book_category = st.text_input("Book Category")
                        new_book_stock = st.text_input("Numbers of Books")

                        if st.button("Add Book(s) in Library"):
                            lsf.insert_new_book(new_book_title, new_book_category, new_book_stock, lsf.db_connection)

                            st.success("Book(s) added in Collection")
                        

                    with tab2: # Book Borrow/Return Request
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
                                st.write(book_requested_to_borrow_admin_view)
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

                        with tab2_2:
                            try:
                            
                                book_requested_to_return_admin_view = lpf.detail_book_data_formatting(
                                    lsf.read_query_as_pd(
                                        lsf.db_connection, lsf.presenting_books_to_be_returned_for_admin_string
                                    )
                                )
                                st.write(book_requested_to_return_admin_view)
                                book_requested_to_return_admin_view_aggrid = lpf.df_to_aggrid(pd.DataFrame(book_requested_to_return_admin_view))


                                if st.button("Approve"):
                                    book_approve_to_be_returned = lpf.select_book_to_borrow_return(book_requested_to_return_admin_view_aggrid, column_name='Book ID')
                                    st.write(book_approve_to_be_returned[0])
                                    lsf.execute_query(
                                        lsf.db_connection,
                                        lsf.approve_to_return(book_approve_to_be_returned[0])
                                    )
                                    st.success("User's request approved")

                            except:
                                st.info("No returning request from users")


                    with tab3: # Shows Books Collection

                        tab3_1, tab3_2 = st.tabs([
                            "Collection Summary",
                            "Books Details Table"
                        ])

                        with tab3_1:
                            book_data_summary_view = lpf.book_data_admin_summary_view_formatting(
                            lsf.read_query_as_pd(
                                lsf.db_connection, lsf.presenting_books_table_for_admin_summary_string
                            )
                        )
                            st.dataframe(book_data_summary_view)
                        
                        with tab3_2:
                            
                            admin_search_keyword = st.text_input("Search Book")

                            if st.button('Search Book'):
                                 
                                detail_book_data = lpf.detail_book_data_formatting(
                                    lsf.read_query_as_pd(
                                        lsf.db_connection, lsf.search_book_admin(admin_search_keyword)
                                    )
                                )
                                
                                st.dataframe(detail_book_data)
                            
                            else:
                                detail_book_data = lpf.detail_book_data_formatting(
                                    lsf.read_query_as_pd(
                                        lsf.db_connection, lsf.presenting_detail_books_table_string
                                    )
                                )
                                
                                st.dataframe(detail_book_data)
                    
                    with tab4: # Add new user 

                        new_user_by_admin = st.text_input("username")
                        new_password_by_admin = st.text_input("New Password by Admin", type='password')
                        new_user_dob_by_admin = st.text_input("Date of Birth")
                        new_user_occupation_by_admin = st.text_input("Occupation")
                        new_user_address_by_admin = st.text_input("Address")
                        
                        if st.button("Add new user"):
                            lsf.execute_query(
                               lsf.db_connection,
                               lsf.inserting_new_user_string(
                                new_user_by_admin,
                                new_user_dob_by_admin,
                                new_user_occupation_by_admin,
                                new_user_address_by_admin,
                                new_password_by_admin
                               ) 
                            )
                            st.success("new user added")


                        

                    with tab5: # Shows Library user List
                        search_user_keyword = st.text_input("Search User")
                        
                        if st.button('Search User'):
                            st.info('search user based on username')
                        
                            detail_user_data = lpf.user_data_formatting(
                                lsf.read_query_as_pd(
                                    lsf.db_connection, lsf.search_for_user_admin(search_user_keyword)
                                )
                            )
                            st.dataframe(detail_user_data) 

                        else:

                            detail_user_data = lpf.user_data_formatting(
                                lsf.read_query_as_pd(
                                    lsf.db_connection, lsf.presenting_detail_users_table_string
                                )
                            )

                            st.dataframe(detail_user_data) 
                        

                else:
                    st.warning("Incorrect username/Password")

            # user/user Section
            else: # use user table
                # retrieve hashed password from user table
                saved_password_from_db = lsf.read_query_as_pd(lsf.db_connection, lsf.select_password_from_table(username))
                hashed_password_input = lpf.hash_password(password)
                                
                if saved_password_from_db.iloc[0][0] == hashed_password_input:
                    st.success(f'Logged as {username}')

                    tab1, tab2, tab3 = st.tabs([
                        "Library Books Collection", 
                        "Borrowed Books",
                        "Profile"
                    ])

                    with tab1:
                        
                        user_search_keyword = st.text_input('Search Books')
                        
                        if 'search_state' not in st.session_state:
                            st.session_state.search_state = False

                        if st.button('Search Book') or st.session_state.search_state:
                            st.session_state.search_state = True

                            st.info('search book based on title')
                            book_data_user_search_view = lpf.book_data_user_summary_view_formatting(
                                lsf.read_query_as_pd(
                                    lsf.db_connection, lsf.search_book_user(user_search_keyword)
                                    )
                            ) 

                            book_userview_aggrid = lpf.df_to_aggrid(pd.DataFrame(book_data_user_search_view))

                        else:
                            
                            book_data_user_view = lpf.book_data_user_summary_view_formatting(
                                lsf.read_query_as_pd(
                                    lsf.db_connection, lsf.presenting_books_table_for_user_summary_user_string
                                    )
                            )

                            book_userview_aggrid = lpf.df_to_aggrid(pd.DataFrame(book_data_user_view))
                                                                
                        if st.button("Request to borrow"):
                            book_request_to_borrow = lpf.select_book_to_borrow_return(book_userview_aggrid, column_name = 'Book Title') 
                            lsf.execute_query(
                                lsf.db_connection,
                                lsf.request_to_borrow(
                                    book_request_to_borrow[0], 
                                    username)
                                )

                            st.write(book_request_to_borrow[0])
                            st.write(lsf.request_to_borrow(book_request_to_borrow[0], username))
                            st.success("Request submitted, awaiting for admin approval")

                    with tab2:
                        try:
                            # display book select user, status borrowed
                            borrowed_book_data_user_view = lpf.detail_book_data_formatting(
                                lsf.read_query_as_pd(
                                    lsf.db_connection, lsf.presenting_borrowed_book_table_for_user_string(username)
                                )
                            )


                            borrowed_book_data_user_view_aggrid = lpf.df_to_aggrid(pd.DataFrame(borrowed_book_data_user_view))
                            
                            
                            # submit book return request
                            if st.button("Return book(s)"):

                                book_request_to_return = lpf.select_book_to_borrow_return(borrowed_book_data_user_view_aggrid, column_name='Book ID') 
                                lsf.execute_query(
                                    lsf.db_connection,
                                    lsf.request_to_return(
                                        book_request_to_return[0], 
                                        username)
                                )

                                st.write(book_request_to_return)
                                # st.write(lsf.request_to_return(book_request_to_return[0], username))
                                # st.success("Request submitted, awaiting for admin approval")

                                # st.success("Request submitted, awaiting for admin confirmation")

                        except:
                            st.info("You haven't borrowed any yet")

                       
                        

                       
                        

                    with tab3:
                        # if st.button("Refresh Profile Data"):
                        #     st.success("Updated profile saved, ")  

                        loggedin_password = st.text_input("New Password by user", type='password')
                        loggedin_user_address = st.text_input("New Address by user")
                        
                        if st.button("Update profile"):

                            lsf.execute_query(
                               lsf.db_connection,
                               lsf.updating_user_profile_string(
                                username, 
                                loggedin_password, 
                                loggedin_user_address
                               ) 
                            )
                            st.write(lsf.updating_user_profile_string(
                                username, 
                                loggedin_password, 
                                loggedin_user_address
                               ) )
                            st.success("Updated profile saved")

                        profile_data = lpf.user_data_formatting(
                            lsf.read_query_as_pd(
                                lsf.db_connection, lsf.retrieve_user_data(username)
                            )
                        )
                        
                        st.dataframe(profile_data)     

                else:
                    st.warning("Incorrect username/Password")

    elif choice == "SignUp":
        st.subheader('Create New Account')
        new_user = st.text_input("username")
        new_password = st.text_input("Password", type='password')
        new_user_dob = st.text_input("tanggal Lahir")
        new_user_occupation = st.text_input("Occupation")
        new_user_address = st.text_input("address")
        
        if st.button("Signup"):
            if new_user != "admin":
                lsf.execute_query(             
                    lsf.db_connection,
                    lsf.inserting_new_user_string(
                        new_user,
                        new_user_dob,
                        new_user_occupation,
                        new_user_address,
                        new_password
                    ) 
                )
                st.success("Registration successful, use login")

            else:
                st.warning("username admin cannot be used")

    else:
        st.subheader('Browse as a Guest')
        st.success("You can browse our collection as a guest")

        guest_search_keyword = st.text_input('Search Books')
                        
        if st.button('Search Book'):
            # st.session_state.search_state = True

            st.info('search book based on title')
            book_data_guest_search_view = lpf.book_data_user_summary_view_formatting(
                lsf.read_query_as_pd(
                    lsf.db_connection, lsf.search_book_user(guest_search_keyword)
                    )
            ) 
            st.dataframe(book_data_guest_search_view)
            # book_userview_aggrid = lpf.df_to_aggrid(pd.DataFrame(book_data_user_search_view))

        else:
            
            book_data_guest_search_view = lpf.book_data_user_summary_view_formatting(
                lsf.read_query_as_pd(
                    lsf.db_connection, lsf.presenting_books_table_for_user_summary_user_string
                    )
            )

            st.dataframe(book_data_guest_search_view)
            # book_userview_aggrid = lpf.df_to_aggrid(pd.DataFrame(book_data_user_view))

        
        

if __name__ == '__main__':
    main()




