import streamlit as st

def render_de_kt_module():
    # 1. CẤU HÌNH CSS ĐỂ KHÓA BỐ CỤC VÀ TÔ MÀU THEO BẢN MẪU
    st.markdown("""
        <style>
        .header-red {color: #FF0000; font-weight: bold; font-size: 18px; margin-bottom: 0px;}
        .header-blue {color: #0000FF; font-weight: bold; font-size: 16px; text-align: center;}
        .text-red-italic {color: #FF0000; font-style: italic; font-weight: bold; font-size: 14px;}
        .box-trac-nghiem {background-color: #FFF2CC; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center;}
        .box-tu-luan {background-color: #D5E8D4; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center;}
        div[data-testid="stNumberInput"] label {display: none !important;}
        div[data-testid="stFileUploader"] label {display: none !important;}
        </style>
    """, unsafe_allow_html=True)

    # 2. HÀNG 1: TIÊU ĐỀ CHÍNH
    col_title1, col_title2 = st.columns(2)
    with col_title1:
        st.markdown('<p class="header-red">CHỨC NĂNG TẠO ĐỀ KIỂM TRA</p>', unsafe_allow_html=True)
    with col_title2:
        st.markdown('<p class="header-red">THƯ MỤC LƯU ĐỀ ĐÃ XD</p>', unsafe_allow_html=True)
    
    st.write("") # Tạo khoảng trắng

    # 3. HÀNG 2: MENU ĐIỀU HƯỚNG CƠ BẢN
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

    # 4. HÀNG 3: TỶ LỆ MỨC ĐỘ NHẬN THỨC
    st.markdown('<p class="header-red">Tỷ lệ mức độ nhận thức (%):</p>', unsafe_allow_html=True)
    col_tl1, col_tl2, col_tl3, col_tl4 = st.columns(4)
    with col_tl1:
        st.write("**Nhận biết:**")
        nhan_biet = st.number_input("NB", value=40, step=5, format="%d")
    with col_tl2:
        st.write("**Thông hiểu:**")
        thong_hieu = st.number_input("TH", value=30, step=5, format="%d")
    with col_tl3:
        st.write("**Vận dụng:**")
        van_dung = st.number_input("VD", value=20, step=5, format="%d")
    with col_tl4:
        st.write("**Vận dụng cao:**")
        van_dung_cao = st.number_input("VDC", value=10, step=5, format="%d")

    st.write("")

    # 5. HÀNG 4: TÊN BÀI VÀ TẢI FILE DỮ LIỆU
    col_ten, col_file1, col_file2 = st.columns([2, 1, 1])
    with col_ten:
        st.markdown('<p class="header-red">Tên bài kiểm tra / Đề số:</p>', unsafe_allow_html=True)
        ten_bai = st.text_input("Tên bài", placeholder="Ví dụ: Kiểm tra đánh giá giữa kì I", label_visibility="collapsed")
    with col_file1:
        st.markdown('<p class="text-red-italic">Tải Đề Cương (.docx, .pdf):</p>', unsafe_allow_html=True)
        de_cuong_file = st.file_uploader("Đề cương", type=['docx', 'pdf'])
    with col_file2:
        st.markdown('<p class="text-red-italic">Tải Đề mẫu ma trận (.docx, .pdf):</p>', unsafe_allow_html=True)
        ma_tran_file = st.file_uploader("Ma trận", type=['docx', 'pdf'])

    st.write("")

    # 6. HÀNG 5: CẤU TRÚC MA TRẬN (TRẮC NGHIỆM & TỰ LUẬN)
    col_tn, spacer, col_tl = st.columns([12, 1, 12])

    # --- CỘT TRÁI: TRẮC NGHIỆM ---
    with col_tn:
        st.markdown('<div class="box-trac-nghiem">TRẮC NGHIỆM &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 4.0 &nbsp;&nbsp;&nbsp; Điểm</div>', unsafe_allow_html=True)
        st.write("")
        
        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu nhiều lựa chọn:")
        with c2: st.number_input("SL1", value=12)
        with c3: st.number_input("D1", value=3.0, step=0.25, format="%.2f")
        with c4: st.write("*điểm*")

        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu đúng/sai:")
        with c2: st.number_input("SL2", value=1)
        with c3: st.number_input("D2", value=0.25, step=0.25, format="%.2f")
        with c4: st.write("*điểm*")

        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu điền khuyết:")
        with c2: st.number_input("SL3", value=1)
        with c3: st.number_input("D3", value=0.25, step=0.25, format="%.2f")
        with c4: st.write("*điểm*")

        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu trả lời ngắn:")
        with c2: st.number_input("SL4", value=2)
        with c3: st.number_input("D4", value=0.5, step=0.25, format="%.2f")
        with c4: st.write("*điểm*")

    # --- CỘT PHẢI: TỰ LUẬN ---
    with col_tl:
        st.markdown('<div class="box-tu-luan">TỰ LUẬN &nbsp;&nbsp;&nbsp; <span style="color:red;">4</span> &nbsp;&nbsp;&nbsp; <span style="color:red;">6.0</span> &nbsp;&nbsp;&nbsp; Điểm</div>', unsafe_allow_html=True)
        st.write("")
        
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1: st.write("**Câu 1.**")
        with c2: st.number_input("TL1", value=2.5, step=0.25, format="%.2f")
        with c3: st.write("*điểm*")

        c1, c2, c3 = st.columns([2, 2, 1])
        with c1: st.write("**Câu 2.**")
        with c2: st.number_input("TL2", value=1.5, step=0.25, format="%.2f")
        with c3: st.write("*điểm*")

        c1, c2, c3 = st.columns([2, 2, 1])
        with c1: st.write("**Câu 3.**")
        with c2: st.number_input("TL3", value=1.0, step=0.25, format="%.2f")
        with c3: st.write("*điểm*")

        c1, c2, c3 = st.columns([2, 2, 1])
        with c1: st.write("**Câu 4.**")
        with c2: st.number_input("TL4", value=1.0, step=0.25, format="%.2f")
        with c3: st.write("*điểm*")

    # 7. HÀNG 6: YÊU CẦU KHÁC & NÚT THỰC THI
    st.write("")
    col_chk, col_req = st.columns([1, 2])
    with col_chk:
        st.markdown('<p class="text-red-italic">Yêu cầu khác:</p>', unsafe_allow_html=True)
    with col_req:
        bam_sat = st.checkbox("Bám sát nội dung đề cương tải lên", value=True)
        
    yeu_cau_khac = st.text_area("Yêu cầu khác", placeholder="Ví dụ: ...", label_visibility="collapsed")
    
    st.write("")
    # Nút bấm thực thi (Tạm thời là nút tĩnh, logic AI sẽ gắn vào sau)
    st.button("🚀 Khởi tạo Đề Kiểm Tra", type="primary", use_container_width=True)
