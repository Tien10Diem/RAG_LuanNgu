import json
import re
from langchain_core.tools import tool

# Load dữ liệu trực tiếp từ JSON
with open(r"data\preprocessed\luanngu.json", "r", encoding="utf-8") as f:
    data = json.load(f)

@tool
def exact_book_tool():
    """Chỉ gọi tool này khi đầu vào yêu cầu 1 bài hoặc thiên không rõ ràng, ví dụ: bài cuối, bài đầu thiên đầu, bài cuối thiên 10,..."""
    lines = []
    for thien_key, thien_val in data.items():
        # Bỏ qua các key không phải thiên
        if not isinstance(thien_val, dict):
            continue
        
        so_bai = sum(1 for k in thien_val if k.startswith("Bài"))
        ten_thien = thien_val.get("Tên thiên", "")
        lines.append(f"{thien_key} - {ten_thien}: {so_bai} bài")

    return "\n".join(lines)