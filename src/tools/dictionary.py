from langchain_core.tools import tool

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