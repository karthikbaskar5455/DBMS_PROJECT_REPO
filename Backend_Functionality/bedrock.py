import os
import boto3
from langchain.chains import ConversationChain
from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
def bedrock_chain():
    # Set the AWS profile to be used by Boto3.
    # Replace "default" with the name of your AWS profile if it's different.
    profile = os.environ["AWS_PROFILE"]="default"    


    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        aws_access_key_id="xxxxxxxxxxxxxxxxxxxx",    #substitute with your aws access key id

        aws_secret_access_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  #substitute with your aws secret access key
        region_name="ap-south-1"    #you can change to your preffered region
    )

    titan_llm = Bedrock(
        model_id="amazon.titan-text-express-v1", client=bedrock_runtime, credentials_profile_name=profile
    )
    titan_llm.model_kwargs = {"temperature": 0.5, "maxTokenCount": 700}

    prompt_template = """System: The following is a friendly conversation between a knowledgeable helpful assistant and a customer.
    The assistant is talkative and provides lots of specific details from it's context.

    Current conversation:
    {history}

    User: {input}
    Bot:"""
    PROMPT = PromptTemplate(
        input_variables=["history", "input"], template=prompt_template
    )

    memory = ConversationBufferMemory(human_prefix="User", ai_prefix="Bot")
    conversation = ConversationChain(
        prompt=PROMPT,
        llm=titan_llm,
        verbose=False,
        memory=memory,
    )

    return conversation
def remove_user_text(input_text):
    # Find the index of "User:"
    user_index = input_text.find("User:")
    
    # Remove everything starting from "User:"
    if user_index != -1:
        output_text = input_text[:user_index].strip()
    else:
        output_text = input_text
    
    return output_text

def remove_repetitions(input_string):
    words = input_string.split()
    seen = set()
    result = []

    for word in words:
        if word not in seen:
            seen.add(word)
            result.append(word)

    # Join the unique words back into a string
    return ' '.join(result)

def remove_bot_prefix(input_string):
    # Split the string into lines
    lines = input_string.split('\n')
    
    # Remove "Bot:" from each line
    cleaned_lines = [line.replace("Bot:", "").strip() for line in lines]
    
    # Join the cleaned lines back into a single string
    return '\n'.join(cleaned_lines)

"""def run_chain(chain, prompt):
    num_tokens = chain.llm.get_num_tokens(prompt)
    return chain({"input": prompt}), num_tokens"""
def run_chain(chain, prompt):
    num_tokens = chain.llm.get_num_tokens(prompt)
    
    # Get AI response and remove user content
    ai_response = chain({"input": prompt})
    ai_response_without_user = ai_response.get("response", "")

    return {"response": remove_bot_prefix(remove_repetitions(remove_user_text(ai_response_without_user)))}, num_tokens


def clear_memory(chain):
    return chain.memory.clear()

        
