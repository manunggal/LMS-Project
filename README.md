# LMS-Project

## Introduction
This is a fourth assignment of Python class from data science course at [Pacmann](https://pacmann.io/). It is arranged to illustrate the functionality of python with MySQL database. LMS stands for Library Management Project, this app is designed to manage the administration of a suppose to be a library at Pacmann. Basic functionality covers adding new books into the collection, searching for books, adding new users and viewing books status.

## Requirements
The required package is listed in ```requirements.txt```. Along with the general practice of setting up local environemnt, those packages need to be installed prior to the utilization of this app. 


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
### Admin Section
#### Register New Book
#### Book Borrow/Return Request
#### Books Collection
#### Add New User
#### Users List
### User Section
#### Browse and Search Collection
#### Borrowed Books
#### Profile Update
### Guest Section
