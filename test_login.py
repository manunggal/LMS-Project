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
	"""Simple Login App"""

	st.title("Simple Login App")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			
			msm.execute_query(db_connection, create_users_table)
            # check user password
            # result_password_check = ua.check_password(username, password)
			
			# if result_password_check.iloc[0][0]:

			st.success("Logged In as {}".format(username))

			task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
			if task == "Add Post":
				st.subheader("Add Your Post")

			elif task == "Analytics":
				st.subheader("Analytics")
			else:
				st.subheader("User Profiles")
				user_result = view_all_users()
				clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
				st.dataframe(clean_db)
		else:
			st.warning("Incorrect Username/Password")





	else:
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			msm.execute_query(db_connection, msm.creating_users_table)
			msm.execute_query(db_connection, msm.inserting_new_user())
            st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")
        else:
            


if __name__ == '__main__':
	main()