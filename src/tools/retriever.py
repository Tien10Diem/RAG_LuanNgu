from langchain_core.tools import tool
from src.data_prep.ingest_chroma import db

retriever = db.as_retriever(search_kwargs={"k": 3})

@tool
def retrieval_tool(query: str):
    """Sử dụng retriever_tool nếu câu hỏi liên quan đến nội dung tài liệu. 
    Nếu câu hỏi nằm ngoài phạm vi tài liệu hoặc là lời chào hỏi xã giao, hãy trả lời trực tiếp rằng bạn không có thông tin."""
    
    docs= retriever.invoke(query)
    
    if docs is None:
        return "Not found!!!"
    
    list_docs=[]
    for i, doc in enumerate(docs):
        list_docs.append(f"Docs {i+1}: \n{doc.page_content}")
    
    return "\n\n".join(list_docs)

@tool
def search(query: str):
    """Chỉ sử dụng search tool nếu câu hỏi liên quan đến giải thích nghĩa của từ, câu trong tài liệu."""
    
    """
    Hướng làm:
    Chia làm 3 tầng:
    Khớp chính xác
    Tìm trên tập con -> Câu hỏi đặt ra: Nhiều tập con? (liệu có tối ưu?)
    split để tìm từng từ
    """
    pass