# Chatbot RAG Luận Ngữ

Dự án này cài đặt một chatbot có thể trả lời các câu hỏi về Luận Ngữ của Khổng Tử bằng cách sử dụng pipeline RAG (Retrieval-Augmented Generation). Chatbot sử dụng giao diện Gradio để tương tác với người dùng.

## Tính năng

-   **Giao diện Chatbot**: Giao diện web thân thiện với người dùng được xây dựng bằng Gradio.
-   **Pipeline RAG**: Sử dụng pipeline RAG để truy xuất các đoạn văn bản có liên quan từ Luận Ngữ và tạo ra câu trả lời.
-   **Vector Store**: Sử dụng ChromaDB làm kho lưu trữ vector để truy xuất các đoạn văn bản hiệu quả.
-   **Tích hợp LLM**: Tích hợp với các mô hình ngôn ngữ từ Google Gemini và Groq bằng LangChain.
-   **Kiến trúc Mô-đun**: Dự án được cấu trúc với các mô-đun riêng biệt cho việc chuẩn bị dữ liệu, logic của agent và ứng dụng chính.

## Chi tiết về Luồng hoạt động

Dự án hoạt động dựa trên một pipeline RAG (Retrieval-Augmented Generation) được xây dựng bằng LangChain và LangGraph. Luồng hoạt động chi tiết như sau:

1.  **Chuẩn bị dữ liệu (`src/data_prep`)**:
    *   Dữ liệu gốc từ file `LuanNgu.pdf` được xử lý và chuyển đổi thành file `luanngu.json` với các tên thiên, bài, nội dung.
    *   Script `ingest_chroma.py` đọc file JSON này, tạo các đối tượng `Document` của LangChain.
    *   Các văn bản lớn được chia thành các đoạn nhỏ hơn (chunks) bằng `RecursiveCharacterTextSplitter` để tối ưu hóa việc truy xuất.

2.  **Vector Store và Embedding**:
    *   Các chunks văn bản sau đó được "vector hóa" (embedding) bằng mô hình embedding của Google (thông qua `langchain_google_genai`).
    *   Các vector này cùng với nội dung text gốc được lưu trữ trong một cơ sở dữ liệu vector là **ChromaDB** (`data/vectorstore`). Quá trình này được gọi là "ingestion" và chỉ cần thực hiện một lần.

3.  **Xử lý yêu cầu người dùng (`app.py` và `src/agent`)**:
    *   Khi người dùng gửi một câu hỏi thông qua giao diện Gradio, câu hỏi này sẽ được chuyển đến agent của LangGraph.
    *   **Retrieval**: Agent sử dụng một công cụ retriever (`src/tools/retriever.py`) để tìm kiếm trong ChromaDB. Nó sẽ tìm và trả về 3 đoạn văn bản (chunks) có liên quan nhất đến câu hỏi của người dùng dựa trên sự tương đồng về mặt ngữ nghĩa của vector.
    *   **Generation**: Các đoạn văn bản được truy xuất này, cùng với câu hỏi gốc và lịch sử cuộc trò chuyện (được quản lý bởi `MemorySaver` của LangGraph), được đóng gói thành một "prompt" hoàn chỉnh.
    *   Prompt này được gửi đến một mô hình ngôn ngữ lớn (LLM) như Google Gemini hoặc Groq để tạo ra câu trả lời cuối cùng.
    *   **Agent Graph**: Logic của agent được định nghĩa trong `src/agent/graph.py` sử dụng `StateGraph`. Graph này có các node chính là `call_llm` (gọi LLM) và `action` (thực hiện một công cụ, ví dụ như retriever). Cạnh điều kiện `should_cont` quyết định luồng tiếp theo: liệu agent cần tiếp tục sử dụng công cụ hay đã có đủ thông tin để trả lời.

4.  **Hiển thị kết quả**:
    *   Câu trả lời do LLM tạo ra được trả về cho `app.py` và hiển thị trên giao diện Gradio cho người dùng.

Toàn bộ quá trình này giúp chatbot có khả năng trả lời các câu hỏi một cách chính xác bằng cách dựa trên ngữ cảnh được cung cấp từ kho tài liệu "Luận Ngữ", thay vì chỉ dựa vào kiến thức đã được huấn luyện trước của LLM.

## Cấu trúc Dự án

```
.
├── app.py                # Tệp ứng dụng chính với giao diện Gradio
├── requirements.txt      # Các thư viện Python cần thiết
├── data/
│   ├── preprocessed/     # Các tệp dữ liệu đã được tiền xử lý
│   ├── raw/              # Các tệp dữ liệu thô (PDF, CSV)
│   └── vectorstore/      # Kho lưu trữ vector ChromaDB
├── pipeline/
│   └── pipeline.ipynb    # Jupyter notebook cho pipeline xử lý dữ liệu
└── src/
    ├── agent/            # Logic của agent với LangGraph
    ├── data_prep/        # Các script để chuẩn bị và nhập dữ liệu
    ├── llm_config.py     # Cấu hình cho các mô hình ngôn ngữ
    └── tools/            # Các công cụ truy xuất và khác
```

## Cài đặt

1.  Sao chép repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  Tạo và kích hoạt môi trường ảo (tùy chọn nhưng được khuyến nghị):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Trên Windows, sử dụng `venv\Scripts\activate`
    ```

3.  Cài đặt các thư viện cần thiết:
    ```bash
    pip install -r requirements.txt
    ```

## Sử dụng

1.  **Nhập dữ liệu (Data Ingestion)**:
    Trước khi chạy ứng dụng lần đầu tiên, bạn cần nhập dữ liệu vào kho lưu trữ vector Chroma. Chạy lệnh sau từ thư mục gốc:
    ```bash
    python -m src.data_prep.ingest_chroma
    ```
    Script này sẽ xử lý dữ liệu từ `data/preprocessed/luanngu.json` và lưu trữ nó trong thư mục `data/vectorstore`.

2.  **Chạy Chatbot**:
    Để khởi động chatbot, hãy chạy tệp `app.py`:
    ```bash
    python app.py
    ```
    Lệnh này sẽ khởi chạy một giao diện web Gradio. Mở URL được cung cấp trong trình duyệt của bạn để tương tác với chatbot.
