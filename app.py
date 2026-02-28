import os
from langchain_core.messages import HumanMessage
from src.agent.graph import rag, config
import gradio as gr



def chatbot_response(message, history):
    # message: Câu hỏi mới nhất từ giao diện gõ vào
    # history: Lịch sử do UI tự lưu (ở đây ta bỏ qua vì LangGraph đã có MemorySaver)
    
    result = rag.invoke(
        {"messages": [HumanMessage(content=message)]},
        config=config
    )
    
    # Trả về đúng chuỗi str để giao diện in ra
    return result['messages'][-1].content

demo = gr.ChatInterface(
    fn=chatbot_response, 
    title="Luận Ngữ",
    description="Khổng Tử"
)

if __name__ == "__main__":
    demo.launch()