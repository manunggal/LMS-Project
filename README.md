# LMS-Project

## Introduction
This is a fourth assignment of Python class from data science course at [Pacmann](https://pacmann.io/). It is arranged to illustrate the functionality of python with MySQL database. LMS stands for Library Management Project, this app is designed to manage the administration of a suppose to be a library at Pacmann. Basic functionality covers adding new books into the collection, searching for books, adding new users and viewing books status, etc.

## Requirements
The required package is listed in ```requirements.txt```. Along with the general best practice of setting up local environment, those packages need to be installed prior to the utilization of this app. The virtual environment or ```venv``` can be set up within your local working directory using  ```python -m venv LMS-Project``` command. The virtual environment will be created and contained within a directory called ```LMS-Project```. Afterwards it can be activated via ```./Scripts/activate```. ```pip install``` command can be used to install the required packages. ```mysql-connector-python``` is used to handle the connection and operation of the MySQL database from python, whereas the creation of the UI aspect is managed using ```streamlit``` a powerful framework to create machine learning and data science app. you can learn more about it at  [Streamlit](https://streamlit.io/). A Streamlit extension called ```streamlit-aggrid``` helps to create an interactive table. in this app, it is used to create a table book where user can select a book to borrow. Finally ```pandas``` is used to handle the tables coming out of the MySQL database. The python functions that were created for this project are saved in two separate files. `lms_python_functions.py` (imported as `lpf` in the app) contains functions related to data wrangling in python while `lms_sql_functions.py` (imported as `lsf` in the app) has functions that send queries to MySQL database.




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
When `username` input is 'admin' and `password` input is '1234', the app will present the admin page.

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
![register new book](https://github.com/manunggal/LMS-Project/blob/1daccf9b0a8e18dc77ca9f445621ab599ec3f6c9/readme%20pics/register_new_book_admin.jpg)

The input of `new_book_title`, etc will be executed as MySQL query using `lsf.insert_new_book` function when the `st.button("Add Book(s) in Library")` is clicked. Within this block of code, the number of books to be added will be based  on `new_book_stock` input. For each new book, a `book_id` number is generated automatically using auto increment feature that was set-up during MySQL table creation.

#### Book Borrow/Return Request
Both books borrow or return tab will display the following message when there are no such request from library users.
gambar st.info borrow request


When there are such requests, a function:



from `lms_sql_functions.py` will retrieve the table from database and present it to the admin, where function `detail_book_data_formatting` from `lms_python_functions.py` will format the table's column names. Meanwhile function `df_to_aggrid` from `lms_python_functions.py` will convert `pandas` `dataframe` to `Aggrid` `dataframe` in order to create interactive table where the admin can select which request to be approved using a checkbox.
The handling of this request is executed after admin click the `approve` button from `if st.button("Approve"):` code where `book title` is captured from the selected row using `lpf.select_book_to_borrow_return` and used as a query to be sent to the database using `lsf.approve_to_borrow` function. 
The same process will also happens for the borrow request tab. 


#### Books Collection
There are two tabs within `Book Collection` tab, which are:
- Collection Summary
  
    The collection summary provides admin with available stock information for each book title. `lsf.presenting_books_to_be_returned_for_admin_string` function is used to send the query and retrieve the result. 
    The example: 
    The table shows numbers of available book, numbers of borrow, total stock, etc

- Books Details Table
  This tab presents the raw table from database, it covers the status of the book, if it is borrowed, who borrow it, and when it needs to be return. 
  Within this tab admin can also search book title by clicking the `Search Book` button after providing the search keyword. `lsf.search_book_admin` function provide the requred MySQL query.





#### Add New User
Similiar with adding new book, admin can add new user via `Add New User` tab. the provided information will be assembled as MySQL query string using `lsf.inserting_new_user_string` after clicking `Add new user` button. As general practice of not saving user password as a plain text, the newly created password is hashed using `lpf.hash_password` function. This function use `hashlib.sha3_256()` function from `hashlib`.

#### Users List
This tab will provide a table of detail users information.

### User Section
Library user need to provide his/her username and corresponding password  to login. This information is used to check the saved username and password in the database using `lsf.select_password_from_table(username)` function.

#### Browse and Search Collection
Once the user is logged-in, one the user can browse for collection. The table presented in this section is a simplified version, it only provides book title, book category, and how many books are available. `lsf.presenting_books_table_for_user_summary_user_string` function handle the reading query from the database. The user can also searches books title using book title keyword.  `lsf.search_book_user` handle the search.
When the user decide to borrow a book, the user can select it via a checkbox at the left side of the table. This table is built using `lpf.df_to_aggrid` that convert pandas dataframe to aggrid dataframe, in order to facilitate book selection. After clicking `Request to Borrow`, 
```
 book_request_to_borrow = lpf.select_book_to_borrow_return(book_userview_aggrid, column_name = 'Book Title') 
                            lsf.execute_query(
                                lsf.db_connection,
                                lsf.request_to_borrow(
                                    book_request_to_borrow[0], 
                                    username)
                                )
``` 
this block of codes handle the request. `lsf.request_to_borrow` convert the `available` status of the book to become `requested to be borrwed`. Books with this status will be presented in admin's `borrow request` tab. As explained above, after the admin approves the request, the book status will be converted to `borrowed` and username of the borrower will be added in the `requested or borrowed by` column of `books_table`.


#### Borrowed Books
Once the user's borrow request approved by the admin, the list of borrowed book will be shown here. `lsf.presenting_borrowed_book_table_for_user_string` filter `books_table` where `book_status` is `borrowed` and `borrowed_by` equal to username.


#### Profile Update
User can make simple update of its password and address. ` lsf.updating_user_profile_string` handles the update of `users_table` in the database and `lsf.retrieve_user_data` presents the result by filtering `user_name` from the `users_table`. 

### SignUp Section
Besides the admin, new user can signup itself using signup section. The functions are similiar with the ones used above.


### Guest Section
Guest section can be used for those who doesn't intend to register as user. By browsing as a guest, one can search and view the library collection. The functions for this section are similiar with the ones in browse and search tab of the user section, only without the checkbox for borrowing request.
