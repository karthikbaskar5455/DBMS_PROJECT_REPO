import mysql.connector
from mysql.connector import Error
import sys
from datetime import datetime

sys.path.append('<PATH-TO-DIRECTORY-WHERE-pwdHashing-IS-STORED>')
from pwdHashing import *

sys.path.append('<PATH-TO-DIRECTORY-WHERE-deviceInfo-IS-STORED>')
from deviceInfo import *


#Replace ' with _ to prevent SQL INJECTION
def sanitize_input(input_string):
    """
    Replace single quotes with underscores in the input string.
    """
    return input_string.replace("'", "_")


#Class with Class variables to be used across different programs
class SharedValue:
    # Class variables shared by all instances
    _shared_value = None
    _shared_value2 = None
    _shared_list = []  # New list to store UserPrompts
    _shared_list2= []  # New list to store AI Responses
    @classmethod
    def set_value(cls, value):
        cls._shared_value = value

    @classmethod
    def set_value2(cls, value):
        cls._shared_value2 = value

    @classmethod
    def get_value(cls):
        return cls._shared_value

    @classmethod
    def get_value2(cls):
        return cls._shared_value2

    @classmethod
    def add_to_list(cls, value):
        cls._shared_list.append(value)

    @classmethod
    def get_list(cls):
        return cls._shared_list

    @classmethod
    def set_list(cls, new_list):
        cls._shared_list = new_list


    @classmethod
    def add_to_list2(cls, value):
        cls._shared_list2.append(value)

    @classmethod
    def get_list2(cls):
        return cls._shared_list2

    @classmethod
    def set_list2(cls, new_list):
        cls._shared_list2 = new_list


#convert date into proper format
def convert_date_format(date_str: str) -> str:
    # Parse the input date string
    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
    
    # Format the date object to the desired format
    return date_obj.strftime('%Y-%m-%d')

#Execute query - returns records for SELECT but returns 0 for correct commit
def execute_query(query):
    try:
        # Establish the connection
        connection = mysql.connector.connect(
            host='localhost',       # Adjust if necessary
            database='AWS_HELP_CHATBOT_BACKEND',
            user='xxxxxxx',   # Replace with your MySQL username
            password='xxxxxxx' # Replace with your MySQL password
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            
            # Commit changes for INSERT/UPDATE/DELETE queries
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                connection.commit()
                return 0
            else:
                # Fetch and print results for SELECT queries
                results = cursor.fetchall()
                return results

    except Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        if connection.is_connected():
            cursor.close()
            connection.close()


#Insert into DEVICE_INFO Table
def insert_DeviceInfo():
    di=Get_List_DeviceInfo()
    query=f"INSERT INTO DEVICE_INFO VALUES(NULL,'{di[0]}' , '{di[1]}' , '{di[2]}' , '{di[3]}' , '{di[4]}' , '{di[5]}')"
    execute_query(query)

#Insert into  LOCATION_INFO table
def insert_LocationInfo():
    li=Get_List_LocationInfo()
    query=f"INSERT INTO LOCATION_INFO VALUES(null,'{li[0]}' , '{li[1]}' , '{li[2]}' , '{li[3]}')"
    execute_query(query)

#Insert into User_ Table
def insert_User_(username,name,age,dob,Email):
    dob=convert_date_format(dob)
    query="SELECT COUNT(*) FROM USER_AUTH;"
    pwd_ID=int(execute_query(query)[0][0])
    query=f"INSERT INTO USER_ VALUES(null, '{username}' , '{name}' , '{age}' , '{dob}' , '{Email}',null,'{pwd_ID}');"
    execute_query(query)   

#Insert a password after hashing it along with the hashing algorithm used
def insert_User_Auth(password):
    list1=hash_password(password)
    query=f"INSERT INTO USER_AUTH VALUES(NULL,'{list1[0]}','{list1[1]}','{list1[2]}');"
    # query="INSERT INTO USER_AUTH VALUES(NULL," + list1[0] + "," + list1[1] +"," + list1[2] + ");"
    execute_query(query)

#Insert into LOGIN_ATTEMPTS table when User_ID is mentioned
def insert_Login_Attempts(state, User_ID):
    Location_ID = int(execute_query("SELECT COUNT(*) FROM LOCATION_INFO")[0][0])
    Device_ID = int(execute_query("SELECT COUNT(*) FROM DEVICE_INFO")[0][0])

    # Check if User_ID is None and set the query accordingly
    query = f"INSERT INTO LOGIN_ATTEMPTS(Status, User_ID, Location_ID, device_Info_ID) VALUES('{state}', '{User_ID}' , '{Location_ID}', '{Device_ID}');"
    execute_query(query)

#Insert into LOGIN_ATTEMPTS table when User_ID is NOT mentioned
def insert_Login_Attempts2(state):
    Location_ID = int(execute_query("SELECT COUNT(*) FROM LOCATION_INFO")[0][0])
    Device_ID = int(execute_query("SELECT COUNT(*) FROM DEVICE_INFO")[0][0])

    # Check if User_ID is None and set the query accordingly
    query = f"INSERT INTO LOGIN_ATTEMPTS(Status, User_ID, Location_ID, device_Info_ID) VALUES('{state}', NULL , '{Location_ID}', '{Device_ID}');"
    execute_query(query)

#Checking if username exists
def check_username(username):
    query1=" SELECT Username FROM USER_ ;"
    usernames=execute_query(query1)
    if (username,) in usernames:
        return True
    return False

# Retrieve User ID based on username
def get_UserID(username):
    query1=f"SELECT User_ID FROM USER_ WHERE Username='{username}';"
    return(execute_query(query1)[0][0])

#Insert into Session_ Table
def insert_Session_(Start_Time,End_Time,Duration,User_ID):
    Model_ID=1
    Location_ID = int(execute_query("SELECT COUNT(*) FROM LOCATION_INFO")[0][0])
    Device_ID = int(execute_query("SELECT COUNT(*) FROM DEVICE_INFO")[0][0])
    query=f"INSERT INTO SESSION_ VALUES ( NULL , '{Start_Time}' ,  '{End_Time}' , '{Duration}', '{User_ID}' , '{Location_ID}' , '{Device_ID}', '{Model_ID}'); "
    execute_query(query)

#Insert into USER_PROMPT table
def insert_User_Prompt(Prompt,Timestamp,User_ID):
    Session_ID=int(execute_query("SELECT COUNT(*) FROM SESSION_")[0][0])
    query=f"INSERT INTO USER_PROMPT VALUES( NULL , '{Prompt}' , '{Timestamp}' , '{User_ID}' , '{Session_ID}' )"
    execute_query(query)

#Insert into Responses Table
def insert_Responses(Timestamp , Response , Session_ID ):
    Model_ID=1
    Prompt_ID=int(execute_query("SELECT COUNT(*) FROM USER_PROMPT")[0][0])
    query=f"INSERT INTO RESPONSES VALUES( NULL , '{Timestamp}' , '{Response}' , '{Model_ID}' , '{Session_ID}' , '{Prompt_ID}' )"
    execute_query(query)

#Retrieve Latest Session ID
def get_Session_ID():
    Session_ID=execute_query("SELECT COUNT(*) FROM SESSION_")[0][0]
    return Session_ID




