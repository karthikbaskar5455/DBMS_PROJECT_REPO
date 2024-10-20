import streamlit as st
import os
import csv
import sys

sys.path.append('<PATH TO FILE : sql_methods')
from sql_methods import *


import re

# Function to check if an email is valid
def is_valid_email(email: str) -> bool:
    # Regular expression for validating an email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Check if the email matches the pattern
    if re.match(pattern, email):
        return True  # Email is valid
    else:
        return False  # Email is not valid

#checking if the entered date is of DD-MM-YYYY format
def is_valid_date_format(date_str: str) -> bool:
    # Regular expression for DD-MM-YYYY format
    pattern = r'^\d{1,2}-\d{1,2}-\d{4}$'
    
    # Check if the string matches the pattern
    if re.match(pattern, date_str):
        return True
    return False


#Checking if username exists
def check_username(username):
    query1=" SELECT Username FROM USER_ ;"
    usernames=execute_query(query1)
    if (username) in usernames:
        return True
    return False


#our Main function
def signup():
    st.title("Signup Page")

    username = st.text_input("Choose a Username",placeholder="Username")

    name = st.text_input("Name",value="",placeholder="Name")
    age = st.text_input("Age",value="",placeholder="Age")
    dob=st.text_input("Date of Birth",value="",placeholder="DD-MM-YYYY")
    Email=st.text_input("Enter Email",value="",placeholder="Email")

    #converting age to int
    flag=0
    if age.isdigit():
        age=int(age)
    else:
        flag=1


    password = st.text_input("Choose a Password", type="password",placeholder="password")
    confirm_password = st.text_input("Confirm Password", type="password",placeholder="password")

    if st.button("Signup"):

        if password == confirm_password:

            #checking age
            if (flag==1 or age>116 or age<=0):
                st.error("enter a valid age")

            #checking date
            if (is_valid_date_format(dob)==False):
                st.error("Date should be of DD-MM-YYYY format")

            #checking email
            if (is_valid_email(Email)==False):
                st.error("Enter a valid email")
            
            #if email,dob,age,pwd=confirmed pwd then...
            else:
                if username and password and name and dob and Email and age:

                    if check_username(username):
                        st.warning('Username already exists. Please choose another username.')
                    else:
                        # rows = [[username, password]]
                        # write_csv(filename, rows)
                        st.success('Account created successfully! Please log in.')

                        #Adding the password to the USER_AUTH table the hash function called within the below function takes care of hashing
                        insert_User_Auth(sanitize_input(password))
                        #Adding the user Data including name,age,dob,Email
                        insert_User_(sanitize_input(username),sanitize_input(name),age,dob,Email)

                        st.balloons()  # Optional: Add some fun visuals



                else:
                    st.error('Please fill all the input fields')


            
        else:
            st.error("Passwords do not match. Please try again.")

    if st.button("Go to Login"):
        st.switch_page("login.py")

if __name__ == "__main__":
    signup()
