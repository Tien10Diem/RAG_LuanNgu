from langchain_chroma import Chroma
from llm_config import embedd
from langchain_text_splitters import RecursiveCharacterTextSplitter

db= Chroma(
    embedding_function=embedd,
    collection_name= "vectorDB",
    persist_directory= r"data\vectorstore"
)

text_split= RecursiveCharacterTextSplitter(
    chunk_size= 1000,
    chunk_overlap= 200
)
