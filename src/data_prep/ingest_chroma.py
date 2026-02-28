from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
from langchain_chroma import Chroma
from src.llm_config import embedd
from langchain_text_splitters import RecursiveCharacterTextSplitter
import time
import json
from langchain_core.documents import Document
import os

db= Chroma(
    embedding_function=embedd,
    collection_name= "vectorDB",
    persist_directory= r"data\vectorstore"
)

text_split= RecursiveCharacterTextSplitter(
    chunk_size= 1000,
    chunk_overlap= 200
)
if db._collection.count() == 0:
    with open(r"data\preprocessed\luanngu.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []

    for key, value in data.items():
        if key == "Lời mở đầu":
        
            doc = Document(
                page_content=f"Lời mở đầu:\n{value.strip()}",
                metadata={"source": "Lời mở đầu", "type": "intro"}
            )
            documents.append(doc)

        elif key=="Lời Kết":
            doc = Document(
                page_content=f"Lời kết:\n{value.strip()}",
                metadata={"source": "Lời kết", "type": "conclusion"}
            )
            documents.append(doc)
        
        elif key.startswith("Thiên"):
            ten_thien = value.get("Tên thiên", "")
            chu_Han = value.get("Chữ Hán", "") 
            
            for sub_key, sub_content in value.items():
                if sub_key.startswith("Bài"):
                    
                    page_content = f"{key} - {ten_thien} ({chu_Han})\n{sub_key}:\n{sub_content.strip()}"
                    
                    # Lưu thêm chu_Han vào metadata
                    metadata = {
                        "thien": key,
                        "ten_thien": ten_thien,
                        "chu_Han_thien": chu_Han,
                        "bai": sub_key,
                        "type": "content"
                    }
                    
                    doc = Document(page_content=page_content, metadata=metadata)
                    documents.append(doc)
                
    split_docs = text_split.split_documents(documents)
    # db.add_documents(documents=split_docs)

    batch_size = 25
    total = len(split_docs)

    for i in range(0, total, batch_size):
        batch = split_docs[i : i + batch_size]
    
        db.add_documents(batch)
        
        print(f"{i + len(batch)}/{total}")
        
        if i + batch_size < total:
            time.sleep(25)

retriever = db.as_retriever(search_kwargs={"k": 3})