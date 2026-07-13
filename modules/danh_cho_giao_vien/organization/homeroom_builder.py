import streamlit as st
import os
import sys

# =====================================================================
# 1. ĐỊNH VỊ ĐƯỜNG DẪN GỐC TỰ ĐỘNG TÌM AI_ENGINE (ƯU TIÊN TUYỆT ĐỐI)
# =====================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = current_dir
# Quét ngược lên các thư mục cha cho đến khi thấy lõi 'ai_engine'
while not os.path.exists(os.path.join(root_dir, 'ai_engine')) and root_dir != os.path.dirname(root_dir):
    root_dir = os.path.dirname(root_dir)

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Đảm bảo hệ thống tìm thấy thư mục export
export_path = os.path.abspath(os.path.join(root_dir, 'export'))
if export_path not in sys.path:
    sys.path.append(export_path)

# =====================================================================
# 2. NẠP ĐỘNG CƠ TỪ KIẾN TRÚC MỚI
# =====================================================================
from ai_engine.ai_config import get_api_key
from ai_engine.ai_runner import run_ai_with_fallback

def get_word_engine():
    try:
        from export.export_word import WordExportEngine
        return WordExportEngine
    except Exception as e:
        print(f"Lỗi nạp module Word: {e}")
        return None

def render_homeroom_module():
    st.markdown("""
        <style>
        .header-blue {color: #0000FF; font-weight: bold; font-size: 15px; text-align: left; margin-bottom: 2px;}
        .box-homeroom {background-color: #FFF2CC; padding: 15px; border-radius: 8px; border-left: 5px solid #D6B656; margin-bottom: 15px;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="box-homeroom">📋 <b>Trợ lý Chủ nhiệm:</b> Tự động hóa công tác viết nhận xét học bạ, thiết kế kịch bản họp phụ huynh và gợi ý hướng giải quyết các tình huống sư phạm chuyên nghiệp.</div>', unsafe_allow_html=True)

    # 1. CHỌN NGHIỆP VỤ
    nghiep_vu = st.radio(
        "Chọn nghiệp vụ cần hỗ trợ:",
        ["📝 Nhận xét học bạ", "👥 Kịch bản họp phụ huynh", "🧩 Xử lý tình huống sư phạm", "🤝 Hỗ trợ HS khuyết tật"],
        horizontal=True
    )
    
    st.write("---")

    # 2. GIAO DIỆN ĐỘNG THEO TỪNG NGHIỆP VỤ
    noi_dung_input = ""
    prompt_he_thong = ""
    tieu_de_luu = "Cong_Tac_Chu_Nhiem"

    if nghiep_vu == "📝 Nhận xét học bạ":
        st.markdown('<p class="header-blue">Thông tin / Đặc điểm của học sinh:</p>', unsafe_allow_html=True)
        noi_dung_input = st.text_area(
            "Đặc điểm học sinh", 
            placeholder="Ví dụ: Lực học KHTN tốt, tích cực tham gia các dự án khoa học. Tuy nhiên còn trầm tính, cần chủ động hơn khi làm việc nhóm...", 
            height=100, label_visibility="collapsed"
        )
        prompt_he_thong = f"""
Bạn là một Giáo viên Chủ nhiệm Lớp 9 dày dặn kinh nghiệm, giàu lòng nhân ái và thấu hiểu tâm lý học sinh. 
Dựa vào các thông tin sau: {noi_dung_input}
Hãy viết 3 mẫu nhận xét học bạ (hoặc sổ liên lạc) khác nhau cho học sinh này:
1. Mẫu 1: Ngắn gọn, súc tích (dành cho học bạ chính thức).
2. Mẫu 2: Động viên, khích lệ (tập trung vào sự tiến bộ và kỹ năng mềm).
3. Mẫu 3: Góp ý chân thành, mang tính định hướng phát triển trong tương lai.
Yêu cầu: Dùng từ ngữ sư phạm, tích cực, không gây tổn thương học sinh. Trình bày dưới dạng Markdown rõ ràng.
"""
        tieu_de_luu = "Nhan_Xet_Hoc_Ba"

    elif nghiep_vu == "👥 Kịch bản họp phụ huynh":
        st.markdown('<p class="header-blue">Mục đích / Trọng tâm cuộc họp:</p>', unsafe_allow_html=True)
        noi_dung_input = st.text_area(
            "Trọng tâm cuộc họp", 
            placeholder="Ví dụ: Họp phụ huynh đầu năm Lớp 9, phổ biến kế hoạch học tập, định hướng phân luồng ôn thi vào lớp 10...", 
            height=100, label_visibility="collapsed"
        )
        prompt_he_thong = f"""
Bạn là một Giáo viên Chủ nhiệm xuất sắc. Hãy thiết kế một Kịch bản Họp phụ huynh học sinh chi tiết với trọng tâm sau: {noi_dung_input}
Cấu trúc kịch bản cần có:
1. Tuyên bố lý do, giới thiệu đại biểu.
2. Báo cáo tình hình chung của lớp.
3. Nội dung trọng tâm (Triển khai chi tiết các ý giáo viên yêu cầu ở trên).
4. Thảo luận, giải đáp thắc mắc (Gợi ý sẵn 3 câu hỏi phụ huynh thường hỏi và cách giáo viên trả lời khéo léo).
5. Kết luận và lời cảm ơn.
Yêu cầu: Lời văn trang trọng, gắn kết, thể hiện sự chuyên nghiệp. Trình bày bằng Markdown.
"""
        tieu_de_luu = "Kich_Ban_Hop_PHHS"

    elif nghiep_vu == "🧩 Xử lý tình huống sư phạm":
        st.markdown('<p class="header-blue">Mô tả tình huống sư phạm cần giải quyết:</p>', unsafe_allow_html=True)
        noi_dung_input = st.text_area(
            "Tình huống", 
            placeholder="Ví dụ: Trong lớp có một nhóm học sinh quá mải mê làm dự án mà lơ là các môn khác...", 
            height=100, label_visibility="collapsed"
        )
        prompt_he_thong = f"""
Bạn là Chuyên gia Tư vấn Tâm lý Học đường và Cố vấn Sư phạm. Hãy giúp Giáo viên Chủ nhiệm đưa ra hướng giải quyết thấu tình đạt lý cho tình huống sau: {noi_dung_input}
Vui lòng phân tích và đưa ra:
1. Nhận định nguyên nhân cốt lõi của vấn đề tâm lý/hành vi này.
2. Cách xử lý tình huống ngay lập tức (Ngắn hạn).
3. Biện pháp giáo dục và hỗ trợ bền vững (Dài hạn) đảm bảo môi trường lớp học an toàn.
4. Gợi ý mẫu lời thoại giáo viên dùng để nói chuyện trực tiếp với học sinh/phụ huynh.
Yêu cầu: Giải pháp phải mang tính nhân văn, tuân thủ nguyên tắc sư phạm. Trình bày bằng Markdown.
"""
        tieu_de_luu = "Xu_Ly_Tinh_Huong"
        
    else: # Mục mới: Hỗ trợ HS khuyết tật
        st.markdown('<p class="header-blue">Dạng khuyết tật và nhu cầu đặc biệt của học sinh:</p>', unsafe_allow_html=True)
        noi_dung_input = st.text_area(
            "Đặc điểm học sinh khuyết tật", 
            placeholder="Ví dụ: Học sinh khiếm thị nhẹ (cần tài liệu chữ to), hoặc khuyết tật vận động (cần hỗ trợ di chuyển, thao tác trong giờ thực hành thí nghiệm)...", 
            height=100, label_visibility="collapsed"
        )
        prompt_he_thong = f"""
Bạn là Chuyên gia Giáo dục Đặc biệt và là một Giáo viên Chủ nhiệm đầy tâm huyết. Hãy lập một Kế hoạch hỗ trợ giáo dục cá nhân (IEP) khả thi, tập trung vào việc tạo điều kiện hòa nhập cho học sinh có đặc điểm sau: {noi_dung_input}

Bối cảnh: Học sinh đang học lớp 9. Cần chú trọng đặc biệt vào các giải pháp hỗ trợ học sinh tham gia an toàn và hiệu quả vào các giờ học đòi hỏi quan sát, thực hành hoặc làm thí nghiệm (như môn Khoa học Tự nhiên).

Cấu trúc Kế hoạch cần có:
1. Đánh giá tóm tắt khả năng và rào cản của học sinh.
2. Mục tiêu hỗ trợ giáo dục.
3. Biện pháp can thiệp cụ thể trên lớp (Bố trí không gian, điều chỉnh tài liệu học tập, điều chỉnh phương pháp kiểm tra đánh giá, và hỗ trợ thiết bị thực hành).
4. Phân công phối hợp (Giáo viên chủ nhiệm - Giáo viên bộ môn - Phụ huynh - Học sinh hỗ trợ).
Yêu cầu: Văn phong chuyên nghiệp, nhân văn, bám sát các nguyên tắc giáo dục hòa nhập. Trình bày bằng Markdown.
"""
        tieu_de_luu = "Ho_Tro_HS_Khuyet_Tat"

    # 3. NÚT XỬ LÝ
    # Cắt bỏ icon ở đầu, giữ nguyên tên nghiệp vụ và viết hoa
    ten_hien_thi = " ".join(nghiep_vu.split()[1:]).upper()
    
    if st.button(f"🚀 THỰC THI: {ten_hien_thi}", type="primary", use_container_width=True):
        if not noi_dung_input.strip():
            st.warning("⚠️ Thầy/Cô vui lòng nhập thông tin vào khung trống trước khi thực thi.")
            st.stop()

        # =====================================================================
        # BỘ ĐIỀU KHIỂN TRUNG TÂM (AI ENGINE)
        # =====================================================================
        api_key = get_api_key()
        
        if not api_key:
            st.error("⚠️ Lỗi cấu hình: Vui lòng nhập Gemini API Key ở thanh bên (Sidebar) trước!")
            st.stop()

        with st.spinner("🤖 Trợ lý Chủ nhiệm đang soạn thảo nội dung..."):
            # Gọi API thông qua kiến trúc chuẩn
            result = run_ai_with_fallback(
                prompt=prompt_he_thong,
                api_key=api_key,
                model_mode="flash"
            )
            
            if result.get("success"):
                st.session_state['current_homeroom_data'] = {
                    "is_khbd": True, # Dùng cờ này để xuất Word đẹp nhất
                    "title": nghiep_vu,
                    "subject": "Công tác Chủ nhiệm",
                    "grade": "Khối THCS",
                    "ten_bai_save": tieu_de_luu,
                    "ai_generated_content": result.get("text")
                }
                st.success(f"✅ Đã hoàn tất soạn thảo trong {result.get('time'):.2f} giây!")
                st.rerun()
            else:
                st.error("❌ Máy chủ AI đang bận hoặc lỗi.")
                with st.expander("🔍 Chi tiết lỗi kỹ thuật ngầm", expanded=True):
                    st.code(result.get("error"))

    # 4. KẾT XUẤT WORD
    st.markdown("---")
    homeroom_cache = st.session_state.get('current_homeroom_data')
    if homeroom_cache:
        with st.expander("🔍 Xem trước Nội dung biên soạn", expanded=True):
            st.markdown(homeroom_cache["ai_generated_content"])
            
        WordEngine = get_word_engine()
        word_file = None
        if WordEngine:
            try:
                word_file = WordEngine.export_to_word(homeroom_cache)
            except Exception as e:
                st.error(f"⚠️ Lỗi xuất Word: {e}")

        col_dl, col_del = st.columns(2)
        with col_dl:
            if word_file:
                st.download_button(
                    label="📄 Tải Hồ sơ (Word)", 
                    data=word_file, 
                    file_name=f"{homeroom_cache['ten_bai_save']}.docx", 
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            else:
                st.button("📄 Tải Hồ sơ (Đang xử lý)", disabled=True, use_container_width=True)
                
        with col_del:
            if st.button("❌ Xóa bản nháp", use_container_width=True):
                del st.session_state['current_homeroom_data']
                st.rerun()
