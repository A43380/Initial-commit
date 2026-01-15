import gradio as gr
import os
from PyPDF2 import PdfReader
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.getenv("AZURE_OPEN_AI_KEY")
api_version = os.getenv("AZURE_OPEN_AI_VERSION")
api_endpoint = os.getenv("AZURE_OPEN_AI_ENDPOINT")
deployment = os.getenv("AZURE_OPEN_AI_DEPLOYMENT")
print(deployment)
llm = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=api_endpoint,
)

reader = PdfReader("me/linkedin.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text

with open("me/summary.txt", "r", encoding ="utf-8") as f:
    summary = f.read()

name = "Poorti Maheshwari"

system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potentail client or future employer who came across the website. \
If you don't know the answer, say so."

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Proflie:\n{linkedin}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."

def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    response = llm.chat.completions.create(
        model = deployment,
        messages = messages
    )
    return response.choices[0].message.content

gr.ChatInterface(chat, type="messages").launch()

