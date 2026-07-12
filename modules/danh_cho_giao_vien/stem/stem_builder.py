# =====================================================================
# FILE: modules/danh_cho_giao_vien/stem/stem_builder.py
# =====================================================================
import streamlit as st
import os
import sys

# Đảm bảo hệ thống tìm thấy thư mục export ở gốc dự án
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

def get_word_engine():
    try:
        from export.export_word import WordExportEngine
        return WordExportEngine
    except Exception as e:
        st.error(f"Lỗi nạp module kết xuất Word: {e}")
        return None

def render_stem_module():
    # 1. CẤU HÌNH CSS ĐỒNG BỘ GIAO DIỆN
    st.markdown("""
        <style>
        .header-blue {color: #0000FF; font-weight: bold; font-size: 15px; text-align: left; margin-bottom: 2px;}
        .header-red-title {color: #FF0000; font-weight: bold; font-size: 16px; margin-bottom: 5px;}
        .box-stem {background-color: #E1D5E7; padding: 15px; border-radius: 8px; border-left: 5px solid #9673A6; margin-bottom: 15px;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="box-stem">🛠️ <b>Chế độ Kỹ sư Giáo dục:</b> Trợ lý AI sẽ thiết kế Kế hoạch bài dạy STEM tuân thủ nghiêm ngặt quy trình EDP, tích hợp Rubric đánh giá và cá nhân hóa lộ trình học tập.</div>', unsafe_allow_html=True)

    # 2. KHUNG NHẬP LIỆU THÔNG TIN DỰ ÁN STEM
    st.markdown('<p class="header-red-title">Chủ đề / Tên dự án STEM:</p>', unsafe_allow_html=True)
    chu_de = st.text_input("Chủ đề STEM", placeholder="Ví dụ: Thiết kế hệ thống chiếu sáng thông minh tiết kiệm năng lượng...", label_visibility="collapsed")

    col1, col2, col3 = st.columns([1.5, 1.5, 2])
    with col1:
        st.markdown('<p class="header-blue">Môn học chủ đạo:</p>', unsafe_allow_html=True)
        mon_hoc = st.selectbox("Môn học STEM", ["Khoa học tự nhiên", "Vật lý", "Hóa học", "Sinh học", "Toán", "Tin học", "Công nghệ"], label_visibility="collapsed", index=0)
    
    with col2:
        st.markdown('<p class="header-blue">Đối tượng (Lớp):</p>', unsafe_allow_html=True)
        lop = st.selectbox("Lớp STEM", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], label_visibility="collapsed", index=3)
    
    with col3:
        st.markdown('<p class="header-blue">Mô hình AI xử lý:</p>', unsafe_allow_html=True)
        model_display_name = st.selectbox("Mô hình AI STEM", ["3.1 Flash-Lite", "3.5 Flash", "3.1 Pro", "Tư duy mở rộng"], label_visibility="collapsed", index=0)

    st.markdown('<p class="header-blue">Yêu cầu bổ sung / Điều kiện cơ sở vật chất:</p>', unsafe_allow_html=True)
    yeu_cau_dac_biet = st.text_area(
        "Yêu cầu khác", 
        placeholder="Ví dụ: Ứng dụng vi điều khiển ESP8266, tận dụng vật liệu tái chế, thiết kế hoạt động riêng hỗ trợ học sinh có nhu cầu giáo dục đặc biệt...", 
        height=80, 
        label_visibility="collapsed"
    )

    st.write("")

    # 3. NÚT KHỞI TẠO VÀ XỬ LÝ LOGIC AI
    if st.button("🚀 KHỞI TẠO TIẾN TRÌNH BÀI DẠY STEM", type="primary", use_container_width=True):
        if not chu_de.strip():
            st.warning("⚠️ Thầy/Cô vui lòng nhập 'Chủ đề / Tên dự án STEM' trước khi khởi tạo.")
            return

        # Lấy trực tiếp chuỗi API Key thô từ bộ nhớ hoặc Secrets
        user_raw_key = st.session_state.get("user_gemini_key", "").strip()
        if not user_raw_key:
            if "GEMINI_API_KEY" in st.secrets: user_raw_key = st.secrets["GEMINI_API_KEY"].strip()
            elif "GOOGLE_API_KEY" in st.secrets: user_raw_key = st.secrets["GOOGLE_API_KEY"].strip()

        if not user_raw_key:
            st.error("⚠️ Lỗi cấu hình: Vui lòng nhập Gemini API Key ở thanh bên (Sidebar) trước!")
            return
            
        from google import genai
        try:
            # Tự động khởi tạo lại Client an toàn
            client = genai.Client(api_key=str(user_raw_key))
        except Exception as api_err:
            st.error(f"❌ Trục trặc khởi tạo máy chủ AI: {api_err}")
            return

        with st.spinner("🤖 Trợ lý AI đang áp dụng quy trình EDP để thiết kế giáo án STEM..."):
            
            # Ánh xạ model
            model_mapping = {
                "3.1 Flash-Lite": "models/gemini-2.5-flash",
                "3.5 Flash": "models/gemini-2.5-flash",
                "3.1 Pro": "models/gemini-1.5-pro",
                "Tư duy mở rộng": "models/gemini-2.5-pro"
            }
            primary_model = model_mapping.get(model_display_name, "models/gemini-2.5-flash")
            fallback_queue = list(dict.fromkeys([primary_model, "models/gemini-2.5-flash", "models/gemini-1.5-pro"]))

            # SIÊU CÂU LỆNH TỪ HUB CỦA THẦY
            system_instruction = f"""
Bạn là chuyên gia giáo dục STEM, có kinh nghiệm triển khai các dự án học tập theo quy trình Kỹ thuật (Engineering Design Process - EDP).

# NHIỆM VỤ
Soạn Kế hoạch bài dạy (KHBD) STEM theo cấu trúc bài học tích hợp.

# CẤU TRÚC BÀI DẠY STEM BẮT BUỘC
1. MỤC TIÊU:
   - Kiến thức (Liên môn: Toán, Khoa học, Công nghệ).
   - Năng lực (Tập trung: Giải quyết vấn đề, Tư duy thiết kế, làm việc nhóm).
   - Phẩm chất (Trách nhiệm, Sáng tạo).
2. THIẾT BỊ & HỌC LIỆU:
   - Liệt kê vật liệu STEM (ưu tiên vật liệu tái chế, chi phí thấp, dễ tìm).
3. TIẾN TRÌNH DẠY HỌC (EDP):
   - Hoạt động 1: Xác định vấn đề (Context & Challenge).
   - Hoạt động 2: Nghiên cứu kiến thức nền (Concept).
   - Hoạt động 3: Lên ý tưởng & Thiết kế giải pháp (Brainstorming).
   - Hoạt động 4: Chế tạo và Thử nghiệm (Build & Test).
   - Hoạt động 5: Trình bày, đánh giá & Cải tiến (Conclusion).

# YÊU CẦU ĐỐI VỚI HOẠT ĐỘNG STEM
- TIẾN TRÌNH: Phải bám sát mô hình CCCC (Context - Challenge - Concept - Conclusion).
- HỖ TRỢ AI: Gợi ý các công cụ AI (ví dụ: dùng AI để thiết kế bản vẽ hoặc tính toán thông số).
- SẢN PHẨM CỤ THỂ: Phải có bảng tiêu chí đánh giá sản phẩm (Rubric) chi tiết.
- PHÂN HÓA:
  - Hỗ trợ: Các bước chế tạo mẫu cụ thể.
  - Mở rộng: Yêu cầu tối ưu hóa sản phẩm (vd: tăng độ bền, giảm chi phí).

# ĐỊNH DẠNG
- Markdown.
- Sử dụng cấu trúc Markdown mạch lạc, bôi đậm các từ khóa quan trọng. Các công thức tính toán thông số kỹ thuật phải được bọc trong ký tự chuẩn LaTeX để hiển thị công thức trực quan.
- Bảng biểu trình bày quy trình chế tạo.

[THÔNG SỐ DỰ ÁN STEM THỰC TẾ]:
- Chủ đề/Tên dự án: {chu_de}
- Môn học chủ đạo: {mon_hoc}
- Đối tượng giảng dạy: Học sinh {lop}
- Các yêu cầu bổ sung/Điều kiện cơ sở vật chất: {yeu_cau_dac_biet if yeu_cau_dac_biet else 'Không có yêu cầu đặc biệt. Ưu tiên tính khả thi trong môi trường lớp học tiêu chuẩn.'}
"""
            response_text = None
            activated_model = ""

            for current_model in fallback_queue:
                try:
                    response = client.models.generate_content(
                        model=current_model,
                        contents=system_instruction
                    )
                    if response and response.text:
                        response_text = response.text
                        activated_model = current_model
                        break
                except Exception as e:
                    if "503" in str(e) or "429" in str(e):
                        continue
                    else:
                        break

            if response_text:
                st.session_state['current_stem_data'] = {
                    "is_khbd": True, # Sử dụng chung cờ is_khbd để mượn cấu trúc xuất Word của Giáo án
                    "subject": f"STEM - {mon_hoc}",
                    "grade": lop,
                    "title": chu_de,
                    "ten_bai_save": chu_de,
                    "ai_generated_content": response_text
                }
                st.success(f"✅ Đã biên soạn thành công dự án STEM bằng mô hình {activated_model}!")
            else:
                st.error("❌ Trục trặc kết nối máy chủ AI. Thầy/Cô vui lòng thử lại sau.")

    # 4. KẾT XUẤT VÀ TẢI FILE WORD
    st.markdown("---")
    st.markdown("##### 📥 Kết Xuất Hồ Sơ Dự Án STEM")
    
    if st.session_state.get('stem_delete_trigger'):
        if 'current_stem_data' in st.session_state:
            del st.session_state['current_stem_data']
        st.session_state['stem_delete_trigger'] = False
        st.rerun()

    stem_cache = st.session_state.get('current_stem_data')
    word_file = None

    if stem_cache:
        with st.expander("🔍 Xem trước Kế hoạch bài dạy STEM", expanded=True):
            st.markdown(stem_cache["ai_generated_content"])
            
        WordEngine = get_word_engine()
        if WordEngine:
            try:
                word_file = WordEngine.export_to_word(stem_cache)
            except Exception as e:
                st.error(f"💡 Trình dịch Word đang đồng bộ cấu trúc: {e}")

    col_save, col_download, col_delete = st.columns(3)
    with col_save:
        if st.button("💾 Lưu file tạm thời", use_container_width=True, disabled=(stem_cache is None), key="btn_save_stem"):
            st.toast("💾 Đã lưu cấu hình dự án STEM vào RAM an toàn!")
    
    with col_download:
        if word_file is not None and stem_cache is not None:
            saved_title = stem_cache.get("ten_bai_save", "Du_An").replace(" ", "_")
            st.download_button(
                label="📄 Tải file về máy",
                data=word_file,
                file_name=f"Giao_An_STEM_{saved_title}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                key="btn_dl_word_stem"
            )
        else:
            st.button("📄 Tải file về máy", disabled=True, use_container_width=True, key="btn_dl_word_stem_disabled")
            
    with col_delete:
        if st.button("❌ Xóa file", use_container_width=True, disabled=(stem_cache is None), key="btn_del_stem"):
            st.session_state['stem_delete_trigger'] = True
            st.rerun()
