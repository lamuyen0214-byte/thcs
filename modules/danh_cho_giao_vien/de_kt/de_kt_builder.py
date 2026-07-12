import streamlit as st
from ai_engine.layer_1_model.gemini import gemini_instance
from ai_engine.layer_3_reasoning.prompt_manager import PromptManager
from ai_engine.layer_5_output.word_export import WordExportEngine

def render_de_kt_module():
    # 1. CẤU HÌNH CSS ĐỂ KHÓA BỐ CỤC
    st.markdown("""
        <style>
        .header-blue {color: #0000FF; font-weight: bold; font-size: 16px; text-align: center;}
        .text-red-italic {color: #FF0000; font-style: italic; font-weight: bold; font-size: 14px;}
        .box-trac-nghiem {background-color: #FFF2CC; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
        .box-tu-luan {background-color: #D5E8D4; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
        .header-red-title {color: #FF0000; font-weight: bold; font-size: 16px; margin-bottom: 5px;}
        </style>
    """, unsafe_allow_html=True)

    # 2. HÀNG 1: MENU ĐIỀU HƯỚNG CƠ BẢN
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<p class="header-blue">MENU MÔN HỌC</p>', unsafe_allow_html=True)
        mon_hoc = st.selectbox("Môn", ["Khoa học Tự nhiên", "Toán học", "Vật lý", "Hóa học"], label_visibility="collapsed", index=0)
    with col2:
        st.markdown('<p class="header-blue">MENU LỚP</p>', unsafe_allow_html=True)
        lop = st.selectbox("Lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], label_visibility="collapsed", index=3)
    with col3:
        st.markdown('<p class="header-blue">HÌNH THỨC KT</p>', unsafe_allow_html=True)
        hinh_thuc = st.selectbox("Hình thức", ["Giữa kì", "Cuối kì", "Thường xuyên"], label_visibility="collapsed")
    with col4:
        st.markdown('<p class="header-blue">THỜI GIAN</p>', unsafe_allow_html=True)
        thoi_gian = st.selectbox("Thời gian", ["45 phút", "60 phút", "90 phút", "120 phút"], label_visibility="collapsed", index=1)

    st.write("")

    # 3. HÀNG 2: TỶ LỆ MỨC ĐỘ NHẬN THỨC
    st.markdown('<p class="header-red-title">Tỷ lệ mức độ nhận thức (%):</p>', unsafe_allow_html=True)
    col_tl1, col_tl2, col_tl3, col_tl4 = st.columns(4)
    with col_tl1:
        nhan_biet = st.number_input("**Nhận biết:**", value=40, step=5, format="%d")
    with col_tl2:
        thong_hieu = st.number_input("**Thông hiểu:**", value=30, step=5, format="%d")
    with col_tl3:
        van_dung = st.number_input("**Vận dụng:**", value=20, step=5, format="%d")
    with col_tl4:
        van_dung_cao = st.number_input("**Vận dụng cao:**", value=10, step=5, format="%d")

    st.write("")

    # 4. HÀNG 3: TÊN BÀI VÀ TẢI FILE DỮ LIỆU
    col_ten, col_file1, col_file2 = st.columns([2, 1, 1])
    with col_ten:
        st.markdown('<p class="header-red-title">Tên bài kiểm tra / Đề số:</p>', unsafe_allow_html=True)
        ten_bai = st.text_input("Tên bài", placeholder="Ví dụ: Kiểm tra đánh giá giữa kì I", label_visibility="collapsed")
    with col_file1:
        st.markdown('<p class="text-red-italic">Tải Đề Cương (.docx, .pdf):</p>', unsafe_allow_html=True)
        de_cuong_file = st.file_uploader("Đề cương", type=['docx', 'pdf'], label_visibility="collapsed")
    with col_file2:
        st.markdown('<p class="text-red-italic">Tải Đề mẫu ma trận (.docx, .pdf):</p>', unsafe_allow_html=True)
        ma_tran_file = st.file_uploader("Ma trận", type=['docx', 'pdf'], label_visibility="collapsed")

    st.write("")

    # 5. HÀNG 4: CẤU TRÚC MA TRẬN ĐỘNG (TRẮC NGHIỆM & TỰ LUẬN)
    col_tn, spacer, col_tl = st.columns([12, 1, 12])

    # --- CỘT TRÁI: TRẮC NGHIỆM ĐỘNG ---
    with col_tn:
        # Đặt chỗ trống (placeholder) để hiển thị tiêu đề sau khi đã tính tổng điểm
        tn_header = st.empty()
        st.write("")
        
        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu nhiều lựa chọn:")
        with c2: sl1 = st.number_input("SL1", value=12, key="sl1", label_visibility="collapsed")
        with c3: d1 = st.number_input("D1", value=3.0, step=0.25, format="%.2f", key="d1", label_visibility="collapsed")
        with c4: st.write("*điểm*")

        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu đúng/sai:")
        with c2: sl2 = st.number_input("SL2", value=1, key="sl2", label_visibility="collapsed")
        with c3: d2 = st.number_input("D2", value=0.25, step=0.25, format="%.2f", key="d2", label_visibility="collapsed")
        with c4: st.write("*điểm*")

        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu điền khuyết:")
        with c2: sl3 = st.number_input("SL3", value=1, key="sl3", label_visibility="collapsed")
        with c3: d3 = st.number_input("D3", value=0.25, step=0.25, format="%.2f", key="d3", label_visibility="collapsed")
        with c4: st.write("*điểm*")

        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu trả lời ngắn:")
        with c2: sl4 = st.number_input("SL4", value=2, key="sl4", label_visibility="collapsed")
        with c3: d4 = st.number_input("D4", value=0.5, step=0.25, format="%.2f", key="d4", label_visibility="collapsed")
        with c4: st.write("*điểm*")

        # Tính tổng điểm trắc nghiệm tự động và cập nhật lên Header
        tong_diem_tn = d1 + d2 + d3 + d4
        tong_so_cau_tn = sl1 + sl2 + sl3 + sl4
        tn_header.markdown(f'<div class="box-trac-nghiem">TRẮC NGHIỆM &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {tong_diem_tn:.2f} &nbsp;&nbsp;&nbsp; Điểm</div>', unsafe_allow_html=True)

    # --- CỘT PHẢI: TỰ LUẬN ĐỘNG ---
    with col_tl:
        # Ô nhập số lượng câu tự luận (mở khóa để giáo viên nhập)
        c_tl1, c_tl2 = st.columns([2, 1])
        with c_tl1: st.write("**Nhập số lượng câu Tự luận:**")
        with c_tl2: so_cau_tl = st.number_input("Số câu TL", min_value=1, max_value=10, value=4, key="so_cau_tl", label_visibility="collapsed")
        
        # Đặt chỗ trống (placeholder) cho tiêu đề tự luận
        tl_header = st.empty()
        st.write("")
        
        diem_tl_list = []
        # Vòng lặp sinh số dòng tương ứng với số câu tự luận được nhập
        for i in range(1, int(so_cau_tl) + 1):
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1: 
                st.write(f"**Câu {i}.**")
            with c2: 
                # Khởi tạo điểm mặc định là 1.0 cho mỗi câu để tránh lỗi
                diem = st.number_input("Điểm", value=1.0, step=0.25, format="%.2f", key=f"diem_tl_{i}", label_visibility="collapsed")
                diem_tl_list.append(diem)
            with c3: 
                st.write("*điểm*")

        # Tính tổng điểm tự luận tự động và cập nhật lên Header
        tong_diem_tl = sum(diem_tl_list)
        tl_header.markdown(f'<div class="box-tu-luan">TỰ LUẬN &nbsp;&nbsp;&nbsp; <span style="color:red;">{int(so_cau_tl)}</span> &nbsp;&nbsp;&nbsp; <span style="color:red;">{tong_diem_tl:.2f}</span> &nbsp;&nbsp;&nbsp; Điểm</div>', unsafe_allow_html=True)

    # 6. HÀNG 6: YÊU CẦU KHÁC & THỰC THI (KHÔI PHỤC KẾT NỐI AI)
    st.write("---")
    col_chk, col_req = st.columns([1, 2])
    with col_chk:
        st.markdown('<p class="text-red-italic">Yêu cầu khác:</p>', unsafe_allow_html=True)
    with col_req:
        bam_sat = st.checkbox("Bám sát nội dung đề cương/ma trận tải lên", value=True)
        yeu_cau_khac = st.text_area("Yêu cầu chi tiết", placeholder="Ví dụ: Chú trọng các câu hỏi liên hệ thực tế...", label_visibility="collapsed")
    
    st.write("")
    
    # Nút bấm kích hoạt AI
    if st.button("🚀 Khởi tạo Đề Kiểm Tra", type="primary", use_container_width=True):
        if not ten_bai.strip():
            st.warning("⚠️ Vui lòng nhập 'Tên bài kiểm tra / Đề số' trước khi khởi tạo.")
        else:
            with st.spinner("AI đang phân tích ma trận và soạn câu hỏi..."):
                # Đóng gói thông tin ma trận để gửi cho AI
                chu_de_ai = f"{ten_bai} ({hinh_thuc}, {thoi_gian}). Tỷ lệ: NB {nhan_biet}%, TH {thong_hieu}%, VD {van_dung}%, VDC {van_dung_cao}%."
                if yeu_cau_khac:
                    chu_de_ai += f" Yêu cầu bổ sung: {yeu_cau_khac}"

                sys_inst, prompt = PromptManager.get_de_kt_prompt(mon_hoc, lop, chu_de_ai, tong_so_cau_tn, int(so_cau_tl))
                result = gemini_instance.generate_content(prompt, sys_inst)
                
                if result:
                    st.success("✅ Đã tạo xong đề kiểm tra theo đúng ma trận!")
                    with st.expander("👀 Xem trước Đề và Đáp án", expanded=True):
                        st.markdown(result)
                    st.session_state['current_de_kt'] = result

    # 7. XUẤT FILE WORD
    if 'current_de_kt' in st.session_state:
        st.write("")
        col_down1, col_down2, col_down3 = st.columns([1, 2, 1])
        with col_down2:
            word_file = WordExportEngine.export_to_word(st.session_state['current_de_kt'], title=f"De_Kiem_Tra_{mon_hoc}")
            st.download_button(
                label="📄 Tải xuống Đề Kiểm Tra (.docx)",
                data=word_file,
                file_name="De_Kiem_Tra.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
