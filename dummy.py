import streamlit as st
import mysql.connector 
from mysql.connector import Error
import pandas as pd
import mysql_manager as msm
import user_authentification as ua



# koneksi ke server
server_connection = msm.create_server_connection(msm.host, msm.user, msm.pw)

# membuat koneksi ke database
db_connection = msm.create_db_connection(
    host_name = msm.host, 
   user_name = msm.user, 
    user_password = msm.pw, 
   db_name = msm.db)

def main():
    """
    simple login app
    """
    st.title("simple login app")

    menu = ["home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "home":
        st.subheader('Home')
    elif choice == "Login":
        st.subheader('Login Section')

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type= "password")
        
        if st.sidebar.button("Login"):
            # retrieve hashed password from database
            #saved_password_from_db = msm.select_password_from_table(username)
            saved_password_from_db = msm.read_query_as_pd(db_connection, msm.select_password_from_table(username))
            saved_password_from_db = ua.hash_password(saved_password_from_db.iloc[0][0])
            hashed_password_input = ua.hash_password(password)
            st.success(saved_password_from_db)
            st.success(hashed_password_input)
            # checking if password match
            if hashed_password_input == saved_password_from_db:
                st.success("Logged in as {}".format(username))

                task = st.selectbox("Task",["Add Post", "Analytics", "Profiles"])
                if task == "Add Post":
                    st.subheader("Add your Post")
                elif task == "Analytics":
                    st.subheader("Analytics")
                else:
                    st.subheader("User Profiles")
            else:
                st.warning("Incorrect Username/Password")
    
    else:
        st.subheader('Create New Account')
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            msm.execute_query(db_connection, msm.insert_new_user(new_user, new_password))
            #msm.execute_query(db_connection, msm.creating_users_table)
			#msm.execute_query(db_connection, msm.insert_new_user(new_user, new_password))
            st.success("You have successfully created an account")
            st.info("Go to Login Menu")
        #else:
            #st.warning("Incorrect Username/Password")


if __name__ == '__main__':
    main()