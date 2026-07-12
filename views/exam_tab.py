import streamlit as st
import os
import requests

def get_word_engine():
    try:
        from export.word_export import WordExportEngine
        return WordExportEngine
    except Exception:
        return None

def render_exam_module():
    st.subheader("📝 Xây dựng Đề kiểm tra & Ma trận")
    # ... (giữ nguyên phần tải file và cấu hình tỷ lệ của thầy) ...
    
    # 5. KHỐI LỆNH ĐIỀU KHIỂN - ĐÃ SỬA LỖI CẤU TRÚC VÀ THỤT LỀ
    if st.button("⚙️ Tự động tạo ma trận & đề thi chính thức"):
        st.write("Đã nhận lệnh khởi tạo!") # Dòng kiểm tra
        
        user_raw_key = st.session_state.get("user_gemini_key", "").strip()
        if not user_raw_key:
            if "GEMINI_API_KEY" in st.secrets: user_raw_key = st.secrets["GEMINI_API_KEY"].strip()
            elif "GOOGLE_API_KEY" in st.secrets: user_raw_key = st.secrets["GOOGLE_API_KEY"].strip()

        if not user_raw_key:
            st.error("⚠️ Vui lòng nhập Gemini API Key ở thanh bên (Sidebar)!")
            return

        # CẤU HÌNH LẠI SYSTEM_INSTRUCTION CHO ĐÚNG BIẾN
        file_text = st.session_state.get('uploaded_file_content', '')
        system_instruction = f"""
        Bạn là chuyên gia khảo thí THCS Bộ GD&ĐT Việt Nam. Hãy biên soạn đề thi bám sát tài liệu: "{chosen_topic}".
        Tuân thủ tỷ lệ: {ratio_str}.
        Phần trắc nghiệm ({total_tn_score} điểm), Phần tự luận ({total_tl_score} điểm).
        """
        
        with st.spinner("🤖 Trợ lý AI đang ra đề..."):
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
            headers = {"Content-Type": "application/json"}
            api_url = f"{url}?key={user_raw_key}"
            payload = {"contents": [{"parts": [{"text": f"{system_instruction}\n\n[DỮ LIỆU]:\n{file_text[:4000]}"}]}]}
            
            try:
                response = requests.post(api_url, headers=headers, json=payload)
                if response.status_code == 200:
                    response_json = response.json()
                    ai_generated_text = response_json['candidates'][0]['content']['parts'][0]['text']
                    
                    st.session_state['current_exam_data'] = {
                        "custom_req": chosen_topic,
                        "c1": c1, "c2": c2, "c3": c3, "c4": c4,
                        "tn_score": str(total_tn_score), "tl_total": str(total_tl_score),
                        "tl_scores": [str(v) for v in tl_scores],
                        "ai_generated_content": ai_generated_text
                    }
                    st.rerun() # Phải rerun để hiện nút Tải về
                else:
                    st.error(f"❌ Lỗi API ({response.status_code}): {response.text}")
            except Exception as e:
                st.error(f"❌ Lỗi kết nối: {e}")

    # 6. KHUNG HIỂN THỊ ĐỀ THI - PHẦN NÀY PHẢI ĐỂ NGOÀI KHỐI IF NÚT BẤM
    if 'current_exam_data' in st.session_state:
        exam_cache = st.session_state['current_exam_data']
        with st.expander("🔍 Xem trước Đề & Đáp án", expanded=True):
            st.markdown(exam_cache["ai_generated_content"])
            
        WordEngine = get_word_engine()
        if WordEngine:
            try:
                word_file = WordEngine.export_to_word(exam_cache)
                st.download_button(label="📄 Tải file Word", data=word_file, file_name="De_Thi.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            except Exception as e:
                st.error(f"⚠️ Lỗi xuất Word: {e}")
        
        st.success(f"✅ Đã nạp thành công {len(loaded_names)} file: {', '.join(loaded_names)}")
        st.session_state['uploaded_file_content'] = uploaded_content
    else:
        st.info("ℹ️ Chưa có tài liệu nào được nạp. AI sẽ ra đề dựa trên chủ đề yêu cầu.")
        st.session_state['uploaded_file_content'] = ""
    # 2. KHUNG TỶ LỆ MỨC ĐỘ NHẬN THỨC CHUẨN SƯ PHẠM
    st.markdown("##### 📊 Tỷ lệ mức độ nhận thức (%)")
    c_ratio1, c_ratio2, c_ratio3, c_ratio4 = st.columns(4)
    with c_ratio1: r_nb = st.number_input("Nhận biết:", min_value=0, max_value=100, value=40, step=5)
    with c_ratio2: r_th = st.number_input("Thông hiểu:", min_value=0, max_value=100, value=30, step=5)
    with c_ratio3: r_vd = st.number_input("Vận dụng:", min_value=0, max_value=100, value=20, step=5)
    with c_ratio4: r_vdc = st.number_input("Vận dụng cao:", min_value=0, max_value=100, value=10, step=5)
    ratio_str = f"Nhận biết {r_nb}%, Thông hiểu {r_th}%, Vận dụng {r_vd}%, Vận dụng cao {r_vdc}%"

    # ĐÃ VÁ LỖI CÚ PHÁP: Bổ sung khối mã thụt lề 4 dấu cách nghiêm ngặt để triệt tiêu lỗi IndentationError
    if (r_nb + r_th + r_vd + r_vdc) != 100:
        st.error("⚠️ Tổng tỷ lệ phần trăm mức độ nhận thức phải bằng 100%!")

    # 3. PHÂN HỆ MA TRẬN ĐỀ THI ĐỘNG CHIA 2 CỘT SONG SONG
    st.markdown("##### ⚙️ Thiết lập Ma trận Điểm số")
    col_tn, col_tl = st.columns(2)

    with col_tn:
        st.markdown("<div style='background-color:#FADBD8; padding:8px; border-radius:5px; color:black; font-weight:bold; text-align:center;'>PHẦN TRẮC NGHIỆM KHÁCH QUAN</div>", unsafe_allow_html=True)
        c1 = st.number_input("Số câu Nhiều lựa chọn (A, B, C, D):", min_value=0, max_value=40, value=12)
        s1 = st.number_input("Tổng điểm Nhiều lựa chọn:", min_value=0.0, max_value=10.0, value=3.0, step=0.5)
        
        c2 = st.number_input("Số câu Đúng / Sai:", min_value=0, max_value=10, value=2)
        s2 = st.number_input("Tổng điểm Đúng / Sai:", min_value=0.0, max_value=10.0, value=1.0, step=0.5)
        
        c3 = st.number_input("Số câu Điền khuyết:", min_value=0, max_value=10, value=1)
        s3 = st.number_input("Tổng điểm Điền khuyết:", min_value=0.0, max_value=10.0, value=0.0, step=0.5)
        
        c4 = st.number_input("Số câu Trả lời ngắn:", min_value=0, max_value=10, value=1)
        s4 = st.number_input("Tổng điểm Trả lời ngắn:", min_value=0.0, max_value=10.0, value=0.0, step=0.5)
        
        total_tn_score = s1 + s2 + s3 + s4
        st.markdown(f"**🔴 TỔNG SỐ CÂU TNKQ: {c1+c2+c3+c4} câu | TỔNG ĐIỂM TRẮC NGHIỆM: <span style='color:#C0392B; font-size:16px;'>{total_tn_score}đ</span>**", unsafe_allow_html=True)
    with col_tl:
        st.markdown("<div style='background-color:#D5F5E3; padding:8px; border-radius:5px; color:black; font-weight:bold; text-align:center;'>PHẦN TỰ LUẬN</div>", unsafe_allow_html=True)
        tl_count = st.number_input("TỔNG SỐ CÂU TỰ LUẬN:", min_value=0, max_value=10, value=3)
        
        tl_scores = []
        st.markdown("*Nhập số điểm chi tiết cho từng câu tự luận:*")
        
        for i in range(tl_count):
            default_val = 2.0 if i == 0 else 1.0
            score_i = st.number_input(f"Điểm Câu {i+1}: ", min_value=0.0, max_value=10.0, value=default_val, step=0.5, key=f"tl_score_{i}")
            tl_scores.append(score_i)
            
        total_tl_score = sum(tl_scores)
        st.markdown(f"**🔵 TỔNG SỐ CÂU TL: {tl_count} câu | TỔNG ĐIỂM TỰ LUẬN: <span style='color:#1F618D; font-size:16px;'>{total_tl_score}đ</span>**", unsafe_allow_html=True)

    chosen_topic = st.text_input("Nhập yêu cầu đặc biệt hoặc phạm vi chủ đề kiểm tra:", value="Bài tập chương 1 về Tốc độ và Đo tốc độ môn Khoa học tự nhiên 7")
    
    total_exam_score = total_tn_score + total_tl_score
    if total_exam_score != 10.0:
        st.warning(f"⚠️ Cảnh báo sư phạm: Tổng điểm toàn bộ đề thi hiện tại đang là {total_exam_score}đ (Chuẩn phải bằng 10.0 điểm). Thầy cô nên điều chỉnh lại.")
    # 5. KHỐI LỆNH ĐIỀU KHIỂN - ĐÃ VÁ LỖI URL VÀ CẤU TRÚC PAYLOAD
    if st.button("⚙️ Tự động tạo ma trận & đề thi chính thức"):
            # ... (Phần kiểm tra Key giữ nguyên) ...
            
            with st.spinner("🤖 Trợ lý AI đang tiếp nhận API Key cá nhân và tiến hành ra đề thi..."):
                # URL chuẩn cho Gemini API
                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
                
                headers = {
                    "Content-Type": "application/json"
                }
                
                # Payload cần kèm Key ở cuối URL hoặc trong Header theo chuẩn Google
                api_url = f"{url}?key={user_raw_key}"
                
                payload = {
                    "contents": [{
                        "parts": [{"text": f"{system_instruction}\n\n[DỮ LIỆU TÀI LIỆU FILE ĐÍNH KÈM GỐC]:\n{file_text[:4000]}"}]
                    }]
                }
                
                try:
                    response = requests.post(api_url, headers=headers, json=payload)
                    
                    if response.status_code == 200:
                        response_json = response.json()
                        # Trích xuất chuỗi chữ theo đúng cấu trúc phản hồi của Gemini 1.5
                        ai_generated_text = response_json['candidates'][0]['content']['parts'][0]['text']
                        
                        st.session_state['current_exam_data'] = {
                            "type": "Trắc nghiệm kết hợp tự luận", "custom_req": chosen_topic,
                            "tn_total": total_tn, "c1": c1, "c2": c2, "c3": c3, "c4": c4,
                            "tn_score": str(total_tn_score), "tl_total": str(total_tl_score),
                            "tl_scores": [str(v) for v in tl_scores], "r_nb": str(r_nb), "r_th": str(r_th), "r_vd": str(r_vd), "r_vdc": str(r_vdc),
                            "ai_generated_content": ai_generated_text
                        }
                        st.rerun()
                    else:
                        st.error(f"❌ Phản hồi từ Google API (Mã {response.status_code}): {response.text}")
                except Exception as http_err: 
                    st.error(f"❌ Trục trặc phân tích dữ liệu: {http_err}")

    # 6. KHUNG HIỂN THỊ ĐỀ THI KÈM NÚT KẾT XUẤT FILE WORD BẢN IN
    if 'current_exam_data' in st.session_state:
        exam_cache = st.session_state['current_exam_data']
        st.markdown("---")
        with st.expander("🔍 Xem trước Nội dung Đề kiểm tra & Đáp án chi tiết từ AI", expanded=True):
            st.markdown(exam_cache["ai_generated_content"])
        WordEngine = get_word_engine()
        if WordEngine:
            try:
                word_file = WordEngine.export_to_word(exam_cache)
                st.download_button(
                    label="📄 Tải xuống file Word (.docx) chứa Ma trận & Đề thi", data=word_file,
                    file_name=f"Bo_De_Kiem_Tra_{chosen_topic.replace(' ', '_')[:30]}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as doc_err: st.error(f"⚠️ Trình kết xuất file Word đang được cập nhật: {doc_err}")
