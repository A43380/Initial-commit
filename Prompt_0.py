from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv(override=True)

api_key = os.getenv("AZURE_OPEN_AI_KEY")
api_version = os.getenv("AZURE_OPEN_AI_VERSION")
azure_endpoint = os.getenv("AZURE_OPEN_AI_ENDPOINT")
deployment = os.getenv("AZURE_OPEN_AI_DEPLOYMENT")

model = AzureChatOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=azure_endpoint,
        azure_deployment=deployment,
        temperature=0
)

st.header("Coding Assist")

user_input = st.text_input("Coding Question")

language_input = st.selectbox("Select the coding Language", ["Select...", "Python", "C++", "Java", "C"])

code_type = st.selectbox("Select the type of code", ["Select...", "Beginner Friendly", "Simple Code", "Complex Code"])

template = PromptTemplate(
    template="""
        Please solve the {user_input} asked in website with the following specifications:
        Coding Language: {language_input}
        Code Type: {code_type}
        1. Approach Details
        - Include the proper explanation took to solve the problem in each step.
        - Explain the time complexity and space complexity of each line.
        - Include any other approach if exists
    If not able to solve the {user_input}, respond with: "Unable to guess the solution" instead of guessing.
""",
input_variables = ["user_input", "language_input", "code_type"]
)

prompt = template.invoke({
    "user_input": user_input,
    "language_input" : language_input,
    "code_type": code_type
})

if st.button("Solve"):
    result = model.invoke(prompt)
    st.write(result.content)