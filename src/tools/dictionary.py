from langchain_core.tools import tool
import json

with open(r"data\preprocessed\HanViet.json", "r", encoding="utf-8") as f:
    dic = json.load(f)
    
@tool
def search(query: str):
    """Chỉ sử dụng search tool nếu câu hỏi liên quan đến giải thích nghĩa của từ, câu trong tài liệu.
    Hãy sử dụng kết quả trả về để trả lời câu hỏi. 
    Khi trả lời thì hãy kèm thêm thông tin lấy từ đâu trong tài liệu HanViet.json.
    """
    
    query = query.strip().lower()

    
    if query in dic:
        return json.dumps({query: dic[query]}, ensure_ascii=False)
    else:
        query_set= set(query.split())
        list_key={}
        for k in dic:
            key_set = set(k.split())
            
            if len(key_set) > 1 and key_set.issubset(query_set):
                list_key[k] = dic[k]
        
        for word in query_set:
            if word in dic and word not in list_key:
                list_key[word] = dic[word]
        
        if len(list_key) > 0:
            return json.dumps(list_key, ensure_ascii=False, indent=2)
        else:
            return "Not found!!!"
    
            