from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
from langchain_core.messages import SystemMessage, ToolMessage, HumanMessage
from src.agent.state import stateAgent
from langgraph.graph import END
from src.tools.dictionary import search
from src.tools.retriever import retrieval_tool
from src.llm_config import model
from langgraph.prebuilt import ToolNode

tools = [search, retrieval_tool]
llm_with_tools= model.bind_tools(tools)

system_prompt = """
Bạn là một trợ lý ảo CHỈ được phép sử dụng thông tin từ tài liệu Luận Ngữ thông qua retrieval_tool.
    QUY TẮC NGHIÊM NGẶT:
    1. Nếu thông tin KHÔNG có trong kết quả trả về của retrieval_tool hoặc search, bạn phải trả lời: 
    "Rất tiếc, tôi không được cung cấp về thông tin này."
    2. TUYỆT ĐỐI KHÔNG sử dụng kiến thức cá nhân hoặc tri thức bên ngoài tài liệu để giải thích. 
    3. TUYỆT ĐỐI Không tự ý bịa đặt hoặc đưa ra các con số nếu tài liệu không ghi rõ hoặc không có.
    4. Luôn trích dẫn rõ Thiên/Bài nếu tìm thấy thông tin.
    5. Câu hỏi của người dùng có thể không rõ ràng nên có thể hỏi lại để đảm bảo hơn.
Tài liệu, sách, nội dung, ... là các từ mà người ta thường mô tả về nội dung của pdf.
"""
def call_llm(state: stateAgent):
    messages = list(state['messages'])
    messages = [SystemMessage(content=system_prompt)] + messages
    
    rs= llm_with_tools.invoke(messages)
    
    return {'messages': [rs]}

action_node = ToolNode(tools)
        
def should_cont(state: stateAgent):
    result = state['messages'][-1]
    
    if hasattr(result, 'tool_calls') and len(result.tool_calls) > 0:
        return "action" 
    
    return END