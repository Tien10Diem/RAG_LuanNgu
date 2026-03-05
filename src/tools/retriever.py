from langchain_core.tools import tool
from src.data_prep.ingest_chroma import retriever
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]

@tool
def retrieval_tool(query: str):
    """Sử dụng retriever_tool nếu câu hỏi liên quan đến việc trích xuất nội dung từ tài liệu (sách, file, pdf).
    QUAN TRỌNG: Hãy chắt lọc từ khóa chính xác từ câu hỏi của người dùng (ví dụ: "Lời mở đầu", "Quân tử", "Thiên Học nhi") để làm 'query' truyền vào. KHÔNG truyền vào những câu hỏi chung chung như "cái gì đây".
    Sử dụng retriever_tool để tìm nội dung từ sách.
    MẸO TÌM KIẾM QUAN TRỌNG ĐỂ KHÔNG BỊ LỖI: 
    - Hệ thống tìm kiếm theo độ tương đồng, KHÔNG giỏi tìm số chính xác. 
    - TUYỆT ĐỐI KHÔNG truyền các câu hỏi như "bài cuối cùng là gì", "có bao nhiêu bài" vào tool, hãy truyền từ khóa là tên Thiên để đếm từ kết quả.
    """
    
    
    docs= retriever.invoke(query)
    
    if docs is None:
        return "Not found!!!"
    
    list_docs = ["<CONTEXT>"]
    for i, doc in enumerate(docs):
        list_docs.append(f"Docs {i+1}: \n{doc.page_content}")
    list_docs.append("</CONTEXT>\nCHÚ Ý TỐI THƯỢNG: CHỈ ĐƯỢC PHÉP TRẢ LỜI DỰA TRÊN THÔNG TIN TRONG CẶP THẺ <CONTEXT> NÀY. KHÔNG BỊA ĐẶT THÊM.")
    
    return "\n\n".join(list_docs)

