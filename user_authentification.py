import hashlib
import mysql_manager

# user authentification
def hash_password(password):
    return hashlib.sha3_256(password.encode()).hexdigest()
 
def check_password(user, hashed_password):
    saved_password = mysql_manager.read_query(
        db_connection, 
        msm.select_password_from_table())
    return saved_password == hashed_password
