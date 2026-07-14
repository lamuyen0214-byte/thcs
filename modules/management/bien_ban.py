import streamlit as st
import pandas as pd
import io
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
# KẾT NỐI CHÍNH THỨC VỚI TRÁI TIM ĐA LUỒNG
from utils.ai_processor import AIProcessor 

# 1. HÀM ĐỌC FILE WORD
def read_docx(file):
    try:
        doc = docx.Document(file)
        return '\n'.join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"Lỗi đọc file: {e}"

# 2. HÀM XUẤT FILE WORD 
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
    p_sub.add_run(f"({tieu_de})").italic = True
    
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

# 3. GIAO DIỆN CHÍNH 
def render_bien_ban(supabase):
    st.markdown("## 📝 Quản Lý Hồ Sơ Biên Bản Tổ Chuyên Môn")
    bb_tabs = st.tabs(["➕ Viết Biên Bản AI", "📋 Kho Biên Bản"])
    
    with bb_tabs[0]:
        st.markdown("### ✍️ Thông tin cuộc họp")
        tieu_de = st.selectbox("Chọn Chủ đề cuộc họp:", [
            "Sinh hoạt chuyên môn theo NCBH", "Sinh hoạt theo chuyên đề", 
            "Sinh hoạt hành chính định kỳ", "Sinh hoạt bồi dưỡng thường xuyên"
        ])
        
        c1, c2, c3 = st.columns(3)
        ngay_hop = c1.date_input("Ngày họp")
        chu_tri = c2.text_input("Chủ trì", value="Lê Hồng Dưỡng")
        thu_ky = c3.text_input("Thư ký", placeholder="Nhập tên thư ký...")
        
        c4, c5 = st.columns(2)
        dia_diem = c4.text_input("Địa điểm", value="Văn phòng trường")
        vang_mat = c5.text_input("Vắng mặt", placeholder="VD: Không")
        
        st.markdown("---")
        st.markdown("### 🤖 Trợ lý AI Hỗ trợ viết Biên bản (Kết nối Đa luồng)")
        
        # CHUẨN HÓA LẤY API KEY TỪ TRÁI TIM ĐA LUỒNG (Không tự tạo ô nhập lung tung nữa)
        api_key = st.session_state.get('gemini_api_key', '')
        if not api_key:
            st.error("⚠️ Ứng dụng chưa nhận được API Key. Vui lòng quay lại thanh menu bên trái, dán API Key và bấm 'Kiểm tra hệ thống AI'.")
            st.stop() # Dừng vẽ giao diện nếu chưa có Key

        file_ke_hoach = st.file_uploader("Tải lên 'Kế hoạch tổ CM' (.docx)", type=['docx'])
        bam_sat_kh = st.checkbox("🎯 AI BẮT BUỘC bám sát nội dung file Kế hoạch", value=True)
        ghi_chu_ai = st.text_input("Ghi chú thêm cho AI", placeholder="VD: Nhấn mạnh vào việc thi giáo viên giỏi...")

        if 'ai_noi_dung' not in st.session_state: st.session_state['ai_noi_dung'] = ""
        if 'ai_ket_luan' not in st.session_state: st.session_state['ai_ket_luan'] = ""

        if st.button("✨ Nhờ AI Viết Biên Bản", type="primary"):
            # KHỞI TẠO BỘ XỬ LÝ ĐA LUỒNG TỪ LÕI HỆ THỐNG
            ai_processor = AIProcessor(api_key)
            
            prompt_base = f"Đóng vai thư ký cuộc họp chuyên nghiệp. Viết chi tiết [NỘI DUNG] và [KẾT LUẬN] cho biên bản '{tieu_de}'. "
            
            if tieu_de == "Sinh hoạt chuyên môn theo NCBH":
                prompt_base += "Tập trung phân tích kế hoạch bài dạy, dự giờ, quan sát học sinh, rút kinh nghiệm."
            elif tieu_de == "Sinh hoạt theo chuyên đề":
                prompt_base += "Tập trung báo cáo lý thuyết chuyên đề, thảo luận thực tiễn."
            elif tieu_de == "Sinh hoạt hành chính định kỳ":
                prompt_base += "Đánh giá chi tiết công tác tháng qua, nề nếp học sinh, phân công nhiệm vụ."
            elif tieu_de == "Sinh hoạt bồi dưỡng thường xuyên":
                prompt_base += "Triển khai module bồi dưỡng, chia sẻ phương pháp sư phạm."
            
            if file_ke_hoach and bam_sat_kh:
                docx_text = read_docx(file_ke_hoach)
                prompt_base += f"\n\nBẮT BUỘC ĐỌC KẾ HOẠCH NÀY ĐỂ VIẾT:\n{docx_text}\n"
            
            if ghi_chu_ai: prompt_base += f"\nLưu ý thêm: {ghi_chu_ai}"
            
            prompt_base += "\n\nTrả về ĐÚNG cấu trúc:\nPHẦN 1: NỘI DUNG\n(chi tiết)\nPHẦN 2: KẾT LUẬN\n(chi tiết)"

            with st.spinner("🤖 Trái tim đa luồng đang phân tích dữ liệu..."):
                # GỌI TRỰC TIẾP QUA TRÁI TIM ĐA LUỒNG THAY VÌ GỌI GOOGLE API
                response_text = ai_processor.generate_response(prompt_base)
                
                if response_text.startswith("Lỗi"):
                    st.error(f"❌ Hệ thống báo lỗi: {response_text}. \n\n💡 Gợi ý: Hãy chắc chắn thầy đã sửa file requirements.txt thành 'google-generativeai==0.8.3'")
                else:
                    try:
                        if "PHẦN 2: KẾT LUẬN" in response_text:
                            p1 = response_text.split("PHẦN 2: KẾT LUẬN")[0].replace("PHẦN 1: NỘI DUNG", "").strip()
                            p2 = response_text.split("PHẦN 2: KẾT LUẬN")[1].strip()
                        else:
                            p1 = response_text
                            p2 = "Không có kết luận."
                        st.session_state['ai_noi_dung'] = p1
                        st.session_state['ai_ket_luan'] = p2
                    except:
                        st.session_state['ai_noi_dung'] = response_text
                        st.session_state['ai_ket_luan'] = ""
                    st.rerun()

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
                st.success("🎉 Đã lưu thành công!")
                st.session_state['ai_noi_dung'] = ""
                st.session_state['ai_ket_luan'] = ""
            except Exception as e:
                st.error(f"Lỗi lưu: {e}")

    with bb_tabs[1]:
        try:
            response = supabase.table("bien_ban").select("*").order("ngay_hop", desc=True).execute()
            df_bb = pd.DataFrame(response.data)
        except:
            df_bb = pd.DataFrame()

        if df_bb.empty:
            st.info("📭 Chưa có biên bản nào.")
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
                    
                    c_a, c_b = st.columns(2)
                    with c_a:
                        st.download_button("📥 Tải File Word", data=docx_file, file_name=f"BienBan_{row['ngay_hop']}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", key=f"dl_{row['id']}")
                    with c_b:
                        if st.button("🗑️ Xóa", key=f"del_{row['id']}"):
                            supabase.table("bien_ban").delete().eq("id", row['id']).execute()
                            st.rerun()
