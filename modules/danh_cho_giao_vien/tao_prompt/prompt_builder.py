# =====================================================================
# FILE: modules/danh_cho_giao_vien/tao_prompt/prompt_builder.py
# =====================================================================
import streamlit as st
import os
import sys

# Đảm bảo hệ thống tìm thấy thư mục export
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

def get_word_engine():
    try:
        from export.export_word import WordExportEngine
        return WordExportEngine
    except Exception as e:
        return None

def render_prompt_module():
    st.markdown("""
        <style>
        .header-blue {color: #0000FF; font-weight: bold; font-size: 15px; text-align: left; margin-bottom: 2px;}
        .box-prompt {background-color: #D0E8F2; padding: 15px; border-radius: 8px; border-left: 5px solid #5C9EAD; margin-bottom: 15px;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="box-prompt">💡 <b>Kỹ sư Prompt:</b> Công cụ giúp Giáo viên cấu trúc hóa các ý tưởng thành "Siêu câu lệnh" chuẩn mực, tối ưu hóa sức mạnh của AI trong công việc.</div>', unsafe_allow_html=True)

    # 1. KHUNG NHẬP LIỆU Ý TƯỞNG
    st.markdown('<p class="header-blue">Thầy/Cô muốn AI làm gì? (Nhập ý tưởng thô):</p>', unsafe_allow_html=True)
    y_tuong_tho = st.text_area(
        "Ý tưởng", 
        placeholder="Ví dụ: Tôi muốn AI viết một bài giới thiệu về ngày hội STEM của trường cấp 2, nghe thật hào hứng để đăng lên Fanpage...", 
        height=100, label_visibility="collapsed"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="header-blue">Đóng vai (Role):</p>', unsafe_allow_html=True)
        vai_tro = st.selectbox("Vai trò", ["Chuyên gia Giáo dục", "Nhà sáng tạo nội dung", "Giáo viên Tâm lý", "Kỹ sư Công nghệ", "Tùy chọn khác"], label_visibility="collapsed")
    with col2:
        st.markdown('<p class="header-blue">Định dạng đầu ra (Format):</p>', unsafe_allow_html=True)
        dinh_dang = st.selectbox("Định dạng", ["Bài viết mạng xã hội", "Văn bản trang trọng (Word)", "Bảng biểu (Markdown)", "Kịch bản (Script)"], label_visibility="collapsed")

    # 2. XỬ LÝ AI - TỐI ƯU PROMPT
    if st.button("🚀 TỐI ƯU HÓA SIÊU CÂU LỆNH (PROMPT)", type="primary", use_container_width=True):
        if not y_tuong_tho.strip():
            st.warning("⚠️ Thầy/Cô vui lòng nhập ý tưởng thô trước khi tối ưu hóa.")
            return

        user_raw_key = st.session_state.get("user_gemini_key", "").strip()
        if not user_raw_key:
            if "GEMINI_API_KEY" in st.secrets: user_raw_key = st.secrets["GEMINI_API_KEY"].strip()
        if not user_raw_key:
            st.error("⚠️ Lỗi cấu hình: Vui lòng nhập Gemini API Key ở thanh bên (Sidebar) trước!")
            return

        with st.spinner("🤖 Hệ thống đang phân tích và tái cấu trúc câu lệnh..."):
            from google import genai
            try:
                client = genai.Client(api_key=str(user_raw_key))
                
                prompt_he_thong = f"""
Bạn là một Chuyên gia Kỹ sư Prompt (Prompt Engineer) hàng đầu. Nhiệm vụ của bạn là nâng cấp ý tưởng thô của người dùng thành một "Siêu câu lệnh" (Meta-prompt) cực kỳ chi tiết, chuyên nghiệp và hiệu quả để họ có thể copy và dùng cho các AI khác (như ChatGPT, Gemini, Claude).

Thông tin đầu vào từ người dùng:
- Ý tưởng cốt lõi: {y_tuong_tho}
- Vai trò AI cần đóng vai: {vai_tro}
- Định dạng mong muốn: {dinh_dang}

Hãy xuất ra cấu trúc như sau (Sử dụng Markdown rõ ràng):
1. **Đánh giá ý tưởng:** Nhận xét ngắn gọn 2 dòng về mục tiêu của người dùng.
2. **SIÊU CÂU LỆNH ĐÃ TỐI ƯU:** Cung cấp câu lệnh hoàn chỉnh. Hãy đóng khung câu lệnh này trong một khối code (code block) để người dùng dễ dàng bấm nút COPY. Câu lệnh này phải bao gồm các yếu tố: 
   - [Vai trò]
   - [Bối cảnh cụ thể]
   - [Nhiệm vụ chi tiết]
   - [Giọng văn/Phong cách]
   - [Cấu trúc đầu ra mong muốn].
3. **Mẹo sử dụng:** Đưa ra 1-2 mẹo nhỏ để người dùng điền thêm biến số nếu cần.
                """
                
                response = client.models.generate_content(
                    model="models/gemini-2.5-flash",
                    contents=prompt_he_thong
                )
                
                if response and response.text:
                    st.session_state['current_prompt_data'] = {
                        "is_khbd": True, # Giữ cờ này để xuất Word ổn định
                        "title": "Công cụ Tối ưu Prompt",
                        "subject": "Kỹ năng AI",
                        "grade": "Giáo viên",
                        "ten_bai_save": "Sieu_Cau_Lenh_AI",
                        "ai_generated_content": response.text
                    }
                    st.success("✅ Đã chế tạo thành công Siêu câu lệnh!")
            except Exception as api_err:
                st.error(f"❌ Lỗi máy chủ AI: {api_err}")

    # 3. KẾT XUẤT WORD
    st.markdown("---")
    prompt_cache = st.session_state.get('current_prompt_data')
    if prompt_cache:
        with st.expander("🔍 Xem trước Siêu câu lệnh", expanded=True):
            st.markdown(prompt_cache["ai_generated_content"])
            
        WordEngine = get_word_engine()
        word_file = None
        if WordEngine:
            try:
                word_file = WordEngine.export_to_word(prompt_cache)
            except Exception as e:
                st.error(f"⚠️ Lỗi xuất Word: {e}")

        col_dl, col_del = st.columns(2)
        with col_dl:
            if word_file:
                st.download_button(
                    label="📄 Tải Prompt (Word)", 
                    data=word_file, 
                    file_name="Sieu_Cau_Lenh_AI.docx", 
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            else:
                st.button("📄 Tải Prompt (Đang xử lý)", disabled=True, use_container_width=True)
                
        with col_del:
            if st.button("❌ Xóa bản nháp", use_container_width=True):
                del st.session_state['current_prompt_data']
                st.rerun()
