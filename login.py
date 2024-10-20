import streamlit as st
import os
import csv
import sys
import devicInfo 

sys.path.append('<PATH TO sql_methods FILE')
from sql_methods import *


# A function that gives current DATETIME
def get_current_timestamp():
    # Get the current date and time
    now = datetime.now()
    # Format it to MySQL DATETIME format
    mysql_timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    return mysql_timestamp



#Checking credentials to validate login
def check_credentials(username,password):
    query1=" SELECT u.Username , ua.pwd FROM USER_ u JOIN USER_AUTH ua ON u.pwd_ID =ua.pwd_ID;"
    usernamePwds=execute_query(query1)
    if (username,password) in usernamePwds:
        return True
    return False

#Checking if username exists
def check_username(username):
    query1=" SELECT Username FROM USER_ ;"
    usernames=execute_query(query1)
    if (username,) in usernames:
        return True
    return False


def login():
    st.title("Login Page")

    username = st.text_input("Username",key="username_input",placeholder="username")
    password = st.text_input("Password", type="password", key="password_input",placeholder="password")

    insert_DeviceInfo()
    insert_LocationInfo()

    #if Login button is pressed
    if st.button("Login"):
        
        #if username and password are both entered
        if username and password:
            

            #If username does NOT exist
            if check_username(username)==False:
                st.error('Account does not exist.')
                st.session_state.logged_in = False 

                #Database updation...
                insert_Login_Attempts2('Failure' )

            #If username exists
            else:
                flag=check_credentials(sanitize_input(username), password)
                #if password matched then row number is returned 
                if flag==True:

                    st.success('Logged in successfully!')
                    st.session_state.logged_in = True  # Update login state
                    st.balloons()  #some fun visuals

                    #Database function handling
                    SharedValue.set_value(get_UserID(  sanitize_input(username) ))   #User_ID being stored in _shared_value
                    SharedValue.set_value2(get_current_timestamp()) #setting _shared_value2 to a current time stamp to mark the begininning of the session 
                    insert_Login_Attempts( 'Success' , get_UserID( sanitize_input(username) )) #LOGIN_ATTEMPTS Table being updated
                    #--
                    st.switch_page("pages/app2.py")
                    return

                #if password not matched then incorrect password
                else:
                    st.error('Incorrect password.')
                    st.session_state.logged_in = False 
                    insert_Login_Attempts2('Failure' , get_UserID( sanitize_input( username ) ) )

        else:
            st.error('Please enter both username and password.')
            st.session_state.logged_in = False 


    #if signup button is pressed 
    if st.button("Go to Signup"):
        st.switch_page("pages/signup.py")
        st.session_state.logged_in = False 
    
if __name__ == "__main__":
    login()

