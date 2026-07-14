import streamlit as st
import pandas as pd
import io
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
import google.generativeai as genai

# 1. HÀM ĐỌC FILE WORD TẢI LÊN
def read_docx(file):
    try:
        doc = docx.Document(file)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        return f"Lỗi đọc file: {e}"

# 2. HÀM XUẤT FILE WORD (CHUẨN HÀNH CHÍNH)
def create_word_document(tieu_de, ngay_hop, dia_diem, chu_tri, thu_ky, vang_mat, noi_dung, ket_luan):
    doc = docx.Document()
    
    p_quoc_hieu = doc.add_paragraph()
    p_quoc_hieu.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_qh = p_quoc_hieu.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    run_qh.bold = True
    run_qh.font.size = Pt(13)
    run_tn = p_quoc_hieu.add_run("Độc lập - Tự do - Hạnh phúc")
    run_tn.bold = True
    run_tn.font.size = Pt(14)
    
    doc.add_paragraph()
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("BIÊN BẢN CUỘC HỌP\n")
    run_title.bold = True
    run_title.font.size = Pt(16)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run(f"({tieu_de})")
    run_sub.italic = True
    run_sub.font.size = Pt(13)
    
    doc.add_paragraph()
    doc.add_paragraph(f"Thời gian: {ngay_hop}")
    doc.add_paragraph(f"Địa điểm: {dia_diem}")
    doc.add_paragraph(f"Chủ trì: {chu_tri}")
    doc.add_paragraph(f"Thư ký: {thu_ky}")
    doc.add_paragraph(f"Vắng mặt: {vang_mat}")
    
    doc.add_heading('I. NỘI DUNG TRIỂN KHAI:', level=2)
    doc.add_paragraph(noi_dung)
    
    doc.add_heading('II. KẾT LUẬN CỦA CHỦ TỌA:', level=2)
    doc.add_paragraph(ket_luan)
    
    doc.add_paragraph()
    
    table = doc.add_table(rows=1, cols=2)
    cell_1 = table.cell(0, 0)
    cell_1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cell_1.paragraphs[0].add_run("THƯ KÝ\n(Ký và ghi rõ họ tên)").bold = True
    
    cell_2 = table.cell(0, 1)
    cell_2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cell_2.paragraphs[0].add_run("CHỦ TRÌ\n(Ký và ghi rõ họ tên)").bold = True
    
    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()

# 3. GIAO DIỆN CHÍNH CỦA BIÊN BẢN
def render_bien_ban(supabase):
    st.markdown("## 📝 Quản Lý Hồ Sơ Biên Bản Tổ Chuyên Môn")
    bb_tabs = st.tabs(["➕ Viết Biên Bản AI", "📋 Kho Biên Bản"])
    
    with bb_tabs[0]:
        st.markdown("### ✍️ Thông tin cuộc họp")
        
        loai_sinh_hoat = [
            "Sinh hoạt chuyên môn theo NCBH", "Sinh hoạt theo chuyên đề", 
            "Sinh hoạt hành chính định kỳ", "Sinh hoạt bồi dưỡng thường xuyên"
        ]
        tieu_de = st.selectbox("Chọn Chủ đề cuộc họp:", loai_sinh_hoat)
        
        c1, c2, c3 = st.columns(3)
        ngay_hop = c1.date_input("Ngày họp")
        chu_tri = c2.text_input("Chủ trì", value="Lê Hồng Dưỡng")
        thu_ky = c3.text_input("Thư ký", placeholder="Nhập tên thư ký...")
        
        c4, c5 = st.columns(2)
        dia_diem = c4.text_input("Địa điểm", value="Văn phòng trường")
        vang_mat = c5.text_input("Vắng mặt", placeholder="VD: Không")
        
        st.markdown("---")
        st.markdown("### 🤖 Trợ lý AI Hỗ trợ viết Biên bản")
        
        api_key = ""
        for k, v in st.session_state.items():
            if isinstance(v, str) and (v.startswith("AIza") or v.startswith("AQ.")):
                api_key = v
                break
                
        if not api_key:
            st.warning("⚠️ Ứng dụng chưa nhận được Key từ thanh menu. Thầy vui lòng dán lại API Key vào ô dưới đây để kết nối nhé:")
            api_key = st.text_input("🔑 Nhập Gemini API Key tại đây:", type="password")

        file_ke_hoach = st.file_uploader("Tải lên 'Kế hoạch tổ CM' (Định dạng .docx) để AI bám sát", type=['docx'])
        bam_sat_kh = st.checkbox("🎯 Yêu cầu AI BẮT BUỘC bóc tách và bám sát nội dung file Kế hoạch tải lên", value=True)
        ghi_chu_ai = st.text_input("Ghi chú thêm cho AI (Tùy chọn)", placeholder="VD: Nhấn mạnh vào việc thi giáo viên giỏi...")

        if 'ai_noi_dung' not in st.session_state: st.session_state['ai_noi_dung'] = ""
        if 'ai_ket_luan' not in st.session_state: st.session_state['ai_ket_luan'] = ""

        if st.button("✨ Nhờ AI Viết Biên Bản", type="primary"):
            if not api_key:
                st.error("❌ Thầy chưa dán API Key. Hãy dán vào thanh menu phía trên để sử dụng AI ạ!")
            else:
                try:
                    genai.configure(api_key=api_key)
                    
                    prompt_base = f"Đóng vai một thư ký cuộc họp chuyên nghiệp của trường học. Hãy viết chi tiết phần [NỘI DUNG] và [KẾT LUẬN] cho biên bản '{tieu_de}'. "
                    
                    if tieu_de == "Sinh hoạt chuyên môn theo NCBH":
                        prompt_base += "Nội dung cần tập trung vào việc phân tích kế hoạch bài dạy, dự giờ, quan sát hoạt động của học sinh, rút kinh nghiệm. "
                    elif tieu_de == "Sinh hoạt theo chuyên đề":
                        prompt_base += "Nội dung cần tập trung vào báo cáo lý thuyết chuyên đề, thảo luận thực tiễn áp dụng tại trường. "
                    elif tieu_de == "Sinh hoạt hành chính định kỳ":
                        prompt_base += "Nội dung cần đánh giá chi tiết công tác tháng qua, tình hình nề nếp học sinh, và phân công nhiệm vụ. "
                    elif tieu_de == "Sinh hoạt bồi dưỡng thường xuyên":
                        prompt_base += "Nội dung tập trung vào việc triển khai các module bồi dưỡng, chia sẻ phương pháp sư phạm. "
                    
                    if file_ke_hoach and bam_sat_kh:
                        docx_text = read_docx(file_ke_hoach)
                        prompt_base += f"\n\nBẮT BUỘC: Bạn phải đọc và bóc tách các nội dung từ tài liệu 'Kế hoạch tổ CM' sau đây để viết biên bản:\n[KẾ HOẠCH]\n{docx_text}\n[HẾT KẾ HOẠCH]\n"
                    
                    if ghi_chu_ai:
                        prompt_base += f"\nLưu ý thêm từ Tổ trưởng: {ghi_chu_ai}"
                        
                    prompt_base += "\n\nHãy trả về kết quả theo cấu trúc sau:\nPHẦN 1: NỘI DUNG\n(viết chi tiết ở đây)\nPHẦN 2: KẾT LUẬN\n(viết chi tiết ở đây)"

                    with st.spinner("🤖 AI đang đọc tài liệu và thử các mô hình để soạn biên bản. Thầy chờ vài giây nhé..."):
                        
                        # VÒNG LẶP THÔNG MINH: Thử lần lượt các Model chuẩn nhất hiện nay
                        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro']
                        response = None
                        last_error = None
                        
                        for model_name in models_to_try:
                            try:
                                model = genai.GenerativeModel(model_name)
                                response = model.generate_content(prompt_base)
                                break  # Nếu thành công, thoát khỏi vòng lặp ngay lập tức
                            except Exception as e:
                                last_error = e
                                continue  # Nếu lỗi (ví dụ 404), tiếp tục thử Model tiếp theo
                        
                        # Nếu thử hết cả 3 cái mà vẫn lỗi thì mới báo ra màn hình
                        if response is None:
                            raise last_error

                        ai_text = response.text
                        
                        try:
                            if "PHẦN 2: KẾT LUẬN" in ai_text:
                                phan_1 = ai_text.split("PHẦN 2: KẾT LUẬN")[0].replace("PHẦN 1: NỘI DUNG", "").strip()
                                phan_2 = ai_text.split("PHẦN 2: KẾT LUẬN")[1].strip()
                            else:
                                phan_1 = ai_text
                                phan_2 = "Không có kết luận cụ thể."
                                
                            st.session_state['ai_noi_dung'] = phan_1
                            st.session_state['ai_ket_luan'] = phan_2
                        except:
                            st.session_state['ai_noi_dung'] = ai_text
                            st.session_state['ai_ket_luan'] = ""
                        
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"❌ Lỗi từ AI: Thầy kiểm tra lại đường truyền mạng hoặc API Key nhé. Chi tiết lỗi: {e}")

        noi_dung = st.text_area("1. Nội dung cuộc họp (Có thể chỉnh sửa):", value=st.session_state['ai_noi_dung'], height=250)
        ket_luan = st.text_area("2. Kết luận (Có thể chỉnh sửa):", value=st.session_state['ai_ket_luan'], height=150)
        
        if st.button("💾 LƯU BIÊN BẢN LÊN HỆ THỐNG", use_container_width=True):
            new_bb = {
                "tieu_de": tieu_de, "ngay_hop": str(ngay_hop), "dia_diem": dia_diem,
                "chu_tri": chu_tri, "thu_ky": thu_ky, "vang_mat": vang_mat if vang_mat else "Không",
                "noi_dung": noi_dung, "ket_luan": ket_luan
            }
            try:
                supabase.table("bien_ban").insert(new_bb).execute()
                st.success("🎉 Đã lưu biên bản thành công! Thầy sang tab 'Kho Biên Bản' để xem và tải file Word.")
                st.session_state['ai_noi_dung'] = ""
                st.session_state['ai_ket_luan'] = ""
            except Exception as e:
                st.error(f"Lỗi lưu Supabase: {e}")

    with bb_tabs[1]:
        try:
            response = supabase.table("bien_ban").select("*").order("ngay_hop", desc=True).execute()
            df_bb = pd.DataFrame(response.data)
        except:
            df_bb = pd.DataFrame()

        if df_bb.empty:
            st.info("📭 Tổ chuyên môn chưa có biên bản nào được lưu.")
        else:
            for index, row in df_bb.iterrows():
                with st.expander(f"📌 {row['ngay_hop']} | {row['tieu_de']}"):
                    st.markdown(f"**Chủ trì:** {row['chu_tri']} | **Thư ký:** {row['thu_ky']}")
                    st.markdown(f"**Nội dung:**\n{row['noi_dung']}")
                    st.markdown(f"**Kết luận:**\n{row['ket_luan']}")
                    
                    docx_file = create_word_document(
                        row['tieu_de'], row['ngay_hop'], row['dia_diem'], 
                        row['chu_tri'], row['thu_ky'], row['vang_mat'], 
                        row['noi_dung'], row['ket_luan']
                    )
                    
                    colA, colB = st.columns(2)
                    with colA:
                        st.download_button(
                            label="📥 Tải Biên Bản (File Word chuẩn)",
                            data=docx_file,
                            file_name=f"BienBan_{row['ngay_hop']}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key=f"dl_{row['id']}"
                        )
                    with colB:
                        if st.button("🗑️ Xóa biên bản", key=f"del_{row['id']}"):
                            supabase.table("bien_ban").delete().eq("id", row['id']).execute()
                            st.rerun()
