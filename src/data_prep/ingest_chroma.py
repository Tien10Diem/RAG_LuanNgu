from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from langchain_chroma import Chroma
from src.llm_config import embedd
from langchain_text_splitters import RecursiveCharacterTextSplitter
import time
import json
from langchain_core.documents import Document

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

    intro_end= []
    for key, value in data.items():
        
        if key.startswith("Thiên"):
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
        elif key == "Lời mở đầu":
            page_content= f"Lời mở đầu - {value.strip()}"
            metadata= {
                "type": "intro"
            }

            intro_end.append(Document(page_content=page_content, metadata=metadata))
        elif key == "Lời Kết":
            page_content= f"Lời kết - {value.strip()}"
            metadata= {
                "type": "conclusion"
            }
            intro_end.append(Document(page_content=page_content, metadata=metadata))


    print(len(documents))
    batch_size = 25

    for i in range(0, len(documents), batch_size):
        batch = documents[i : i + batch_size]
        db.add_documents(documents=batch)
        print(f"{i + len(batch)}/{len(documents)}")
        if i + batch_size < len(documents):
            time.sleep(25)


    split_docs = text_split.split_documents(intro_end)
    total = len(split_docs)
    print(total)

    for i in range(0, total, batch_size):
        batch = split_docs[i : i + batch_size]

        db.add_documents(batch)
        
        print(f"{i + len(batch)}/{total}")
        
        if i + batch_size < total:
            time.sleep(25)


retriever = db.as_retriever(search_kwargs={"k": 5})