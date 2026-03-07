# Chatbot RAG Luận Ngữ - Khổng Tử

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-🦜️🔗-blueviolet)](https://www.langchain.com/)
[![Gradio](https://img.shields.io/badge/Gradio-🚀-orange)](https://www.gradio.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Dự án này xây dựng một chatbot ứng dụng kỹ thuật **Retrieval-Augmented Generation (RAG)**, cho phép người dùng đặt câu hỏi và nhận câu trả lời thông minh về nội dung cuốn **Luận Ngữ** của Khổng Tử. Chatbot được xây dựng với kiến trúc agentic mạnh mẽ sử dụng LangGraph, tích hợp nhiều công cụ để cung cấp câu trả lời chính xác và đa dạng.

## ✨ Tính Năng Nổi Bật

-   **Giao Diện Trực Quan**: Tương tác thân thiện với người dùng thông qua giao diện web được xây dựng bằng **Gradio**.
-   **Kiến Trúc Agentic**: Sử dụng **LangGraph** để điều phối một agent thông minh, có khả năng lựa chọn và sử dụng công cụ phù hợp với câu hỏi của người dùng.
-   **Hệ Thống Đa Công Cụ (Multi-Tool)**:
    1.  **Truy Vấn Ngữ Cảnh (RAG Retriever)**: Tìm kiếm và truy xuất các đoạn văn bản liên quan nhất từ kho tài liệu Luận Ngữ được vector hóa bằng **ChromaDB**.
    2.  **Tra Cứu Từ Điển Hán-Việt**: Giải thích nghĩa của các từ hoặc cụm từ Hán-Việt có trong tài liệu.
    3.  **Tra Cứu Cấu Trúc Sách**: Cung cấp thông tin về cấu trúc của sách Luận Ngữ (số chương, số bài trong mỗi chương).
-   **Tích Hợp LLM**: Tận dụng sức mạnh của các mô hình ngôn ngữ lớn (LLM) từ **Google Gemini** và **Groq** để tổng hợp và tạo ra câu trả lời cuối cùng.
-   **Quản Lý Trạng Thái Hội Thoại**: Lưu trữ lịch sử cuộc trò chuyện để các câu trả lời sau có ngữ cảnh hơn.
-   **Kiến Trúc Module Hóa**: Mã nguồn được tổ chức rõ ràng, tách biệt các thành phần: chuẩn bị dữ liệu, agent, công cụ, và giao diện.

## ⚙️ Luồng Hoạt Động

Hệ thống hoạt động theo một luồng xử lý thông minh, bắt đầu từ câu hỏi của người dùng và kết thúc bằng câu trả lời do LLM tạo ra.

1.  **Giao Diện Người Dùng**: Người dùng nhập câu hỏi vào giao diện Gradio.
2.  **Agent Điều Phối (LangGraph)**:
    -   Câu hỏi được chuyển đến một agent được xây dựng bằng `LangGraph`.
    -   Agent này đóng vai trò như một "bộ não" trung tâm, phân tích câu hỏi để quyết định xem có cần sử dụng công cụ nào không, hay có thể trả lời trực tiếp.
3.  **Lựa Chọn Công Cụ**: Dựa trên phân tích, agent sẽ lựa chọn một trong các công cụ sau:
    -   **`retriever_tool`**: Nếu là câu hỏi chung về nội dung, triết lý trong Luận Ngữ. Công cụ này sẽ tìm kiếm trong ChromaDB để lấy ra các đoạn văn bản liên quan nhất.
    -   **`dictionary_search_tool`**: Nếu câu hỏi yêu cầu giải thích một từ Hán-Việt. Công cụ này sẽ tra cứu trong file `HanViet.json`.
    -   **`exact_book_tool`**: Nếu câu hỏi liên quan đến cấu trúc sách (ví dụ: "Thiên 10 có bao nhiêu bài?").
4.  **Tạo Ngữ Cảnh (Context)**: Kết quả từ công cụ (nếu được sử dụng) sẽ được dùng làm ngữ cảnh bổ sung.
5.  **Gọi LLM**:
    -   Agent tổng hợp câu hỏi gốc, lịch sử trò chuyện và ngữ cảnh từ công cụ thành một prompt hoàn chỉnh.
    -   Prompt này được gửi đến mô hình LLM (Gemini/Groq).
6.  **Tạo và Hiển Thị Câu Trả Lời**: LLM tạo ra câu trả lời dựa trên thông tin được cung cấp và trả về cho giao diện Gradio để hiển thị cho người dùng.

## 🗂️ Cấu Trúc Dự Án

```
.
├── app.py                # Ứng dụng chính, khởi chạy giao diện Gradio
├── requirements.txt      # Các thư viện Python cần thiết
├── .env.example          # Tệp ví dụ cho các biến môi trường
├── data/
│   ├── raw/              # Dữ liệu thô (PDF, CSV)
│   ├── preprocessed/     # Dữ liệu đã qua xử lý (JSON)
│   └── vectorstore/      # Kho vector ChromaDB
├── pipeline/
│   └── pipeline.ipynb    # Jupyter Notebook cho luồng xử lý và chuẩn bị dữ liệu
└── src/
    ├── llm_config.py     # Cấu hình các mô hình ngôn ngữ (LLMs)
    ├── agent/            # Logic của agent (State, Nodes, Graph) với LangGraph
    ├── data_prep/        # Các script chuẩn bị dữ liệu (ingestion)
    └── tools/            # Các công cụ được agent sử dụng (retriever, dictionary,...)
```

## 🚀 Cài Đặt và Sử Dụng

### 1. Chuẩn Bị Môi Trường

-   Sao chép (clone) repository này về máy:
    ```bash
    git clone https://github.com/your-username/RAG_pdf.git
    cd RAG_pdf
    ```
-   Tạo một môi trường ảo (khuyến khích) và kích hoạt nó:
    ```bash
    python -m venv venv
    # Trên Windows
    venv\Scripts\activate
    # Trên macOS/Linux
    source venv/bin/activate
    ```

### 2. Cài Đặt Thư Viện

Cài đặt tất cả các thư viện cần thiết từ file `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Cấu Hình API Key

Dự án yêu cầu API key từ Google AI Studio để sử dụng mô hình Gemini.

-   Tạo một tệp `.env` ở thư mục gốc của dự án.
-   Sao chép nội dung từ `.env.example` và dán vào tệp `.env`.
-   Thay thế `YOUR_API_KEY` bằng API key của bạn.
    ```
    GEMINI_API_KEY="YOUR_API_KEY"
    ```
    Bạn có thể lấy key tại [Google AI Studio](https://aistudio.google.com/app/apikey).

### 4. Chạy Ứng Dụng

Để khởi động chatbot, chạy lệnh sau:
```bash
python app.py
```

Để tiết kiệm token api tôi khuyến nghị nên hạn chế memories của cuộc hội thoại với tham số -s với tiếp đó là số lượng hội thoại mà bạn muốn lưu trữ. Ví dụ:

```bash
python app.py -s 2
```

Ứng dụng sẽ tự động xử lý dữ liệu và tạo kho vector ChromaDB nếu chưa có. Sau khi khởi tạo xong, một URL Gradio sẽ được cung cấp trong terminal. Mở URL này trên trình duyệt để bắt đầu trò chuyện.

### 5. Ví Dụ Câu Hỏi

Bạn có thể thử các loại câu hỏi sau để trải nghiệm các tính năng của chatbot:

-   **Câu hỏi chung**:
    -   `Khổng Tử nói gì về người quân tử?`
    -   `Thế nào là đạo hiếu?`
-   **Câu hỏi tra từ điển**:
    -   `Giải thích từ "lễ"?`
    -   `"Trung thứ" nghĩa là gì?`
-   **Câu hỏi về cấu trúc sách**:
    -   `Thiên cuối cùng có bao nhiêu bài?`
    -   `Cấu trúc của sách Luận Ngữ như thế nào?`
