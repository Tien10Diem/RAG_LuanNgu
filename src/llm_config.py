from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()

api_embedd = os.getenv("api")
api_chat = os.getenv("api_proq")

embedd = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    api_key=api_embedd
)

model= ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0,
    api_key= api_chat
)
