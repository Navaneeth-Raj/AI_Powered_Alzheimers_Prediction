import mysql.connector

def set_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",      
            user="root",  
            password="accessdata",  
            database="task"   
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
def login_details(connection, email, password):
    try:
        cursor = connection.cursor(dictionary=True)
        check_query = "SELECT user_id from users WHERE email_id = %s and password = %s"
        cursor.execute(check_query, (email,password))
        result = cursor.fetchone()
        if result:
            return result['user_id']
        else:
            return False
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Query Failed"
    finally:
        cursor.close()

def cut_connection(connection):
    if connection.is_connected():
        connection.close()

def reg_user(connection, new_user, new_password):
    try:
        cursor = connection.cursor()
        write_query = "INSERT INTO users (email_id, password) VALUES(%s, %s)"
        cursor.execute(write_query, (new_user,new_password))
        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error : {err}")
        return False
    finally:
        cursor.close()
