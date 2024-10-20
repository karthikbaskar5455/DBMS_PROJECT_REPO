import streamlit as st
import uuid
import sys
sys.path.append('<PATH TO sql_methods FILE')
from sql_methods import *

sys.path.append('<PATH TO BEDROCK FILE>')
import bedrock

from datetime import datetime
# A function that gives current DATETIME
def get_current_timestamp():
    # Get the current date and time
    now = datetime.now()
    # Format it to MySQL DATETIME format
    mysql_timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    return mysql_timestamp

# A Function that calculates duration based on startTime and EndTime
def calculate_duration(start_time, end_time):
    # Convert string timestamps back to datetime objects
    dt1 = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    dt2 = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    # Calculate the duration
    duration = dt2 - dt1
    
    # Return total seconds and total minutes
    total_seconds = int(duration.total_seconds())
    total_minutes = total_seconds // 60
    
    return total_minutes

def merge_lists(list1, list2):
    list3 = list1 + list2
    return list3
# Rest of your Streamlit code...


# Streamlit app
def main():

    
    st.title("Your Streamlit App")

    # Fetch data from the database
    data = list() #fetch_data()

    # Display data in Streamlit
    st.write("User Prompts and AI Responses:")
    for row in data:
        st.write(f"User Prompt: {row[0]}")
        st.write(f"AI Response: {row[1]}")
        st.write("---")


# Initialize session state variables
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "llm_app" not in st.session_state:
    st.session_state.llm_app = bedrock

if "llm_chain" not in st.session_state:
    st.session_state.llm_chain = bedrock.bedrock_chain()

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "input" not in st.session_state:
    st.session_state.input = ""

def write_top_bar():
    col1, col2, col3 = st.columns([2, 10, 3])
    with col1:
        logout = st.button("LogOut")
    with col2:
        st.write("                               ")
        st.write("                               ")
        st.write("                               ")
        st.write("                               ")
        header = "     AWS Cloud Services Help Chatbot"
        st.write(f"<h3 class='main-header'>{header}</h3>", unsafe_allow_html=True)
    with col3:
        clear = st.button("Clear Chat")
        
    if clear:
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.input = ""
        bedrock.clear_memory(st.session_state.llm_chain)

    if logout:
        End_Time=get_current_timestamp()
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.input = ""
        bedrock.clear_memory(st.session_state.llm_chain)
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #Inserting a record into Session_ table
        insert_Session_( SharedValue.get_value2() , get_current_timestamp()  , calculate_duration(SharedValue.get_value2(), get_current_timestamp()) , SharedValue.get_value() ) 

        #Inserting to user_prompt and Responses Tables
        Alternating_Prompt_Response_Pairs = list( set(merge_lists(SharedValue.get_list(), SharedValue.get_list2()) ))
        print(Alternating_Prompt_Response_Pairs)
        for prompt_or_Response in Alternating_Prompt_Response_Pairs:

            if prompt_or_Response.startswith("USER_PROMPT : "):
                insert_User_Prompt(prompt_or_Response , get_current_timestamp() , SharedValue.get_value())
            else:
                insert_Responses(get_current_timestamp() , prompt_or_Response , get_Session_ID() )
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        st.switch_page("login.py")
    return clear

clear = write_top_bar()

if clear:
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.input = ""
    bedrock.clear_memory(st.session_state.llm_chain)

def handle_input():
    input_text = st.session_state.input

    llm_chain = st.session_state.llm_chain
    chain = st.session_state.llm_app
    result, amount_of_tokens = chain.run_chain(llm_chain, input_text)
    question_with_id = {
        "question": input_text,
        "id": len(st.session_state.questions),
        "tokens": amount_of_tokens,
    }
    st.session_state.questions.append(question_with_id)

    st.session_state.answers.append(
        {"answer": result, "id": len(st.session_state.questions)}
    )
    st.session_state.input = ""

    #Adding a prompt to the SharedValue Class
    SharedValue.add_to_list("USER_PROMPT : " + sanitize_input(input_text))
    #----------------------------------------

def write_user_message(md):
    col1, col2 = st.columns([1, 12])

    with col1:
        var=8
        #st.image(USER_ICON, use_column_width="always")
    with col2:
        st.container()
        st.warning(md["question"])
        st.write(f"Tokens used: {md['tokens']}")

def render_answer(answer):
    col1, col2 = st.columns([1, 12])
    with col1:
        var=9
        #st.image(AI_ICON, use_column_width="always")
    with col2:
        st.container()
        response=answer["response"]
        st.info(response)
        #Adding the response from AI to sharedValue Class variable list
        SharedValue.add_to_list2( "AI : " + sanitize_input(response) )
        #--------------------------------------------------------------

def write_chat_message(md):
    chat = st.container()
    with chat:
        render_answer(md["answer"])

with st.container():
    for i in range(min(len(st.session_state.get("questions", [])), len(st.session_state.get("answers", [])))):
        q = st.session_state.questions[i]
        a = st.session_state.answers[i]
        write_user_message(q)
        write_chat_message(a)

st.markdown("---")
input_text = st.text_input(
    "You are talking to an AI, ask any question.", key="input", on_change=handle_input
)
