# =====================================================================
# FILE: modules/teaching/rag_engine.py
# =====================================================================
import streamlit as st
import tempfile
import os

def process_rag_engine(uploaded_file, hinh_thuc_url=None):
    st.markdown("---")
    st.markdown("#### 💬 Bước 2: Tương tác và truy vấn với AI")
    
    # 1. KIỂM TRA API KEY
    user_raw_key = st.session_state.get("user_gemini_key", "").strip()
    if not user_raw_key:
        if "GEMINI_API_KEY" in st.secrets: user_raw_key = st.secrets["GEMINI_API_KEY"].strip()
    if not user_raw_key:
        st.error("⚠️ Lỗi cấu hình: Vui lòng nhập Gemini API Key ở thanh bên (Sidebar) trước!")
        return

    # 2. XỬ LÝ TÀI LIỆU TẢI LÊN
    if "rag_chat_history" not in st.session_state:
        st.session_state.rag_chat_history = []
        st.session_state.current_file_id = None

    if uploaded_file is not None:
        file_details = {"Tên file": uploaded_file.name, "Định dạng": uploaded_file.type, "Kích thước": f"{uploaded_file.size / 1024:.2f} KB"}
        st.success(f"✅ Đã nạp tài liệu: {file_details['Tên file']}")
        
        # Lưu file tạm thời để truyền cho Google GenAI
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        # Nếu là file mới thì làm sạch lịch sử chat
        if st.session_state.current_file_id != uploaded_file.name:
            st.session_state.rag_chat_history = []
            st.session_state.current_file_id = uploaded_file.name
    elif hinh_thuc_url:
        st.success(f"✅ Đã ghi nhận đường dẫn URL: {hinh_thuc_url}")
        tmp_file_path = None
    else:
        st.info("💡 Vui lòng hoàn thành Bước 1 (Tải tài liệu hoặc nhập Link) để kích hoạt Trợ lý RAG.")
        return

    # 3. GIAO DIỆN CHAT TRUY VẤN TÀI LIỆU
    chat_container = st.container(height=400)
    with chat_container:
        if not st.session_state.rag_chat_history:
            st.markdown("*AI: Chào thầy/cô! Tôi đã đọc tài liệu. Thầy/Cô muốn bóc tách hoặc tóm tắt thông tin gì từ tài liệu này?*")
        for message in st.session_state.rag_chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Khung nhập câu hỏi
    if prompt := st.chat_input("Nhập câu hỏi về tài liệu (VD: Tóm tắt nguyên lý hoạt động của ESP8266 trong file này...)"):
        # Hiển thị câu hỏi của người dùng
        st.session_state.rag_chat_history.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        # Gửi yêu cầu lên Gemini
        with chat_container:
            with st.chat_message("assistant"):
                with st.spinner("Đang trích xuất dữ liệu từ tài liệu..."):
                    from google import genai
                    try:
                        client = genai.Client(api_key=str(user_raw_key))
                        
                        # Upload file lên Gemini nếu có file
                        if tmp_file_path and uploaded_file is not None:
                            # Tải file lên bộ nhớ của Gemini
                            gemini_file = client.files.upload(file=tmp_file_path)
                            
                            system_instruction = "Bạn là Trợ lý AI Phân tích tài liệu. Hãy trả lời câu hỏi của người dùng dựa TRÊN tài liệu được cung cấp. Nếu thông tin không có trong tài liệu, hãy nói rõ. Trả lời bằng Tiếng Việt."
                            
                            response = client.models.generate_content(
                                model='models/gemini-2.5-flash',
                                contents=[gemini_file, system_instruction, prompt]
                            )
                        else:
                            # Xử lý trường hợp URL (chỉ duyệt văn bản thuần)
                            response = client.models.generate_content(
                                model='models/gemini-2.5-flash',
                                contents=[f"Dựa vào nội dung từ đường dẫn sau (nếu có thể truy cập): {hinh_thuc_url}. Hãy trả lời câu hỏi: {prompt}"]
                            )

                        if response and response.text:
                            st.markdown(response.text)
                            st.session_state.rag_chat_history.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error(f"❌ Lỗi truy xuất tài liệu: {e}")
