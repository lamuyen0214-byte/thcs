# =====================================================================
# FILE: export/word_export.py (TRÌNH XUẤT BẢN IN WORD MƯỢT MÀ SẠCH LỖI)
# =====================================================================
import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import io

class WordExportEngine:
    @staticmethod
    def export_to_word(exam_data):
        """
        Hàm vẽ bảng Khung ma trận 9 cột, bảng Đặc tả kĩ thuật và 
        đổ nội dung đề thi từ AI ra file Word chuẩn lề 3pt hành chính.
        """
        doc = docx.Document()
        
        # 1. Cấu hình căn lề chuẩn văn bản hành chính Việt Nam (Top 2cm, Bottom 2cm, Left 3cm, Right 2cm)
        for section in doc.sections:
            section.top_margin = Inches(0.79)
            section.bottom_margin = Inches(0.79)
            section.left_margin = Inches(1.18)
            section.right_margin = Inches(0.79)
            
        doc.styles['Normal'].font.name = 'Times New Roman'
        doc.styles['Normal'].font.size = Pt(12)
        
        def bg_cell(cell, hex_color):
            cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))

        topic_name = exam_data.get("custom_req", "Kiến thức bài học")
        c1 = exam_data.get("c1", "12")
        c2 = exam_data.get("c2", "1")
        tl_scores = exam_data.get("tl_scores", ["1.0", "1.0", "1.0", "1.0"])
        
        # 2. XÂY DỰNG KHUNG MA TRẬN ĐỀ KIỂM TRA ĐỊNH KỲ
        p1 = doc.add_paragraph()
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_after = Pt(3)
        p1.add_run("KHUNG MA TRẬN ĐỀ KIỂM TRA ĐỊNH KỲ").bold = True
        
        t_mt = doc.add_table(rows=5, cols=9)
        t_mt.style = 'Table Grid'
        hd_mt = ["STT", "Chủ đề kiến thức", "Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao", "Tổng TN", "Tổng TL", "Tổng điểm"]
        
        for idx, text in enumerate(hd_mt):
            cell_hd = t_mt.rows[0].cells[idx]
            cell_hd.text = text
            bg_cell(cell_hd, "F2F4F4")
            cell_hd.paragraphs[0].runs[0].font.bold = True
            cell_hd.paragraphs[0].paragraph_format.space_after = Pt(3)
            
        r_data = [
            ["1", f"Nội dung trọng tâm về: {topic_name}", f"{c1} câu", "0 câu", "2 câu", "0 câu", f"{c1} câu", "2 câu", "5.0đ"],
            ["2", f"Nội dung phân hóa về: {topic_name}", "0 câu", f"{c2} câu", "0 câu", "1 câu", f"{c2} câu", "1 câu", "2.0đ"],
            ["3", "Nội dung thực hành ứng dụng tổng hợp", "0 câu", "2 câu", "2 câu", "0 câu", "2 câu", "2 câu", "3.0đ"],
            ["", "TỔNG CỘNG HOÀN CHỈNH ĐỀ THI", f"{exam_data.get('tn_total','16')} câu", f"{int(c2)+2} câu", "4 câu", "1 câu", f"{exam_data.get('tn_total','16')} câu", f"{len(tl_scores)} câu", "10đ"]
        ]
        
        for r_idx, data in enumerate(r_data, start=1):
            for col_idx, text in enumerate(data):
                cell_data = t_mt.rows[r_idx].cells[col_idx]
                cell_data.text = text
                cell_data.paragraphs[0].paragraph_format.space_after = Pt(3)
                if r_idx == 4:
                    bg_cell(cell_data, "EBF5FB")
                    cell_data.paragraphs[0].runs[0].font.bold = True

        # 3. ĐỔ NỘI DUNG ĐỀ THI VÀ ĐÁP ÁN CHẤM TỪ AI CHUẨN ĐỊNH DẠNG 3PT
        doc.add_paragraph("\n").paragraph_format.space_after = Pt(3)
        p3 = doc.add_paragraph()
        p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p3.add_run("NỘI DUNG ĐỀ KIỂM TRA VÀ ĐÁP ÁN CHẤM THỰC TẾ TỪ AI").bold = True
        
        p_school = doc.add_paragraph()
        p_school.paragraph_format.space_after = Pt(3)
        p_school.add_run("TRƯỜNG THCS NGUYỄN DU\nTài liệu trích xuất tự động từ hệ thống trợ lý Trợ giảng AI.").font.italic = True
        
        ai_content = exam_data.get("ai_generated_content", "")
        clean_content = ai_content.replace("**", "").replace("###", "").replace("##", "")
        
        for line in clean_content.split('\n'):
            if line.strip(): 
                p_line = doc.add_paragraph(line.strip())
                p_line.paragraph_format.space_before = Pt(0)
                p_line.paragraph_format.space_after = Pt(3)
                if line.strip().startswith("I.") or line.strip().startswith("II.") or "PHẦN" in line or "ĐÁP ÁN" in line or "HƯỚNG DẪN" in line:
                    if p_line.runs: 
                        p_line.runs[0].font.bold = True
                        
        # Xuất dữ liệu ra bộ nhớ bytes truyền ngược lại Streamlit download
        bio = io.BytesIO()
        doc.save(bio)
        bio.seek(0)
        return bio.getvalue()
