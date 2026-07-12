import streamlit as st
# Sử dụng Google GenAI SDK chính thống
from google import genai 

def process_rag_engine(uploaded_file, user_query):
    if not uploaded_file:
        return "Vui lòng tải tài liệu lên trước."
    
    # Giả lập xử lý RAG: Đọc nội dung file (Thầy sẽ tích hợp langchain/vector store ở đây sau)
    file_content = uploaded_file.read().decode("utf-8", errors="ignore")
    
    # Gọi AI để trả lời dựa trên file
    client = st.session_state.get("gemini_client")
    if not client:
        return "Chưa cấu hình Gemini API Key."
        
    prompt = f"Dựa vào tài liệu sau: {file_content[:5000]}... \n\n Hãy trả lời câu hỏi: {user_query}"
    
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    return response.text
