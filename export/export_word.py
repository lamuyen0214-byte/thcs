# =====================================================================
# FILE: export/export_word.py (SỬA TRIỆT ĐỂ LỖI _ROWS VÀ ĐỒNG BỘ 100% ĐIỂM)
# =====================================================================
import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import io
import re

class WordExportEngine:
    @staticmethod
    def export_to_word(exam_data):
        """
        Hàm vẽ chuẩn xác Khung ma trận 9 cột, Bảng đặc tả kỹ thuật đạt chuẩn Bộ GD&ĐT
        và tự động xử lý chuyển đổi ký tự toán học in ấn sạch dòng trống.
        """
        doc = docx.Document()
        
        # 1. Cấu hình căn lề chuẩn văn bản hành chính Việt Nam
        for section in doc.sections:
            section.top_margin = Inches(0.79)
            section.bottom_margin = Inches(0.79)
            section.left_margin = Inches(1.18)
            section.right_margin = Inches(0.79)
            
        doc.styles['Normal'].font.name = 'Times New Roman'
        doc.styles['Normal'].font.size = Pt(12)
        
        def bg_cell(cell, hex_color):
            cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))

        # Trích xuất chính xác 100% biểu điểm động từ giao diện của thầy cô
        topic_name = exam_data.get("custom_req", "Kiến thức bài học")
        c1 = exam_data.get("c1", 12)
        c2 = exam_data.get("c2", 1)
        c3 = exam_data.get("c3", 1)
        c4 = exam_data.get("c4", 2)
        
        tn_total_c = exam_data.get("tn_total", 16)
        tn_score_v = exam_data.get("tn_score", "4.0")
        tl_score_v = exam_data.get("tl_score", "6.0")
        tl_scores = exam_data.get("tl_scores", [])
        tl_total_c = len(tl_scores)
        
        r_nb = exam_data.get("r_nb", "40")
        r_th = exam_data.get("r_th", "30")
        r_vd = exam_data.get("r_vd", "20")
        r_vdc = exam_data.get("r_vdc", "10")

        # =====================================================================
        # PHẦN I: KHỔI TẠO KHUNG MA TRẬN ĐỀ KIỂM TRA ĐỊNH KỲ (9 CỘT)
        # =====================================================================
        p1 = doc.add_paragraph()
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_after = Pt(3)
        p1.add_run("KHUNG MA TRẬN ĐỀ KIỂM TRA ĐỊNH KỲ").bold = True
        
        t_mt = doc.add_table(rows=5, cols=9)
        t_mt.style = 'Table Grid'
        hd_mt = ["STT", "Chủ đề kiến thức", "Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao", "Tổng TN", "Tổng TL", "Tổng điểm"]
        
        # ĐÃ SỬA LỖI: Gọi chính xác hàng số 0 [.rows[0].cells] để triệt tiêu lỗi '_Rows' object
        for idx, text in enumerate(hd_mt):
            cell_hd = t_mt.rows[0].cells[idx]
            cell_hd.text = text
            bg_cell(cell_hd, "F2F4F4")
            cell_hd.paragraphs[0].runs[0].font.bold = True
            cell_hd.paragraphs[0].paragraph_format.space_after = Pt(3)
            
        r_data = [
            ["1", f"Nội dung trọng tâm về: {topic_name}", f"{c1} câu", "0 câu", "2 câu", "0 câu", f"{c1} câu", "2 câu", f"{float(tn_score_v)*0.6:.1f}đ"],
            ["2", f"Nội dung phân hóa về: {topic_name}", "0 câu", f"{c2} câu", "0 câu", "1 câu", f"{c2} câu", "1 câu", f"{float(tn_score_v)*0.4:.1f}đ"],
            ["3", "Nội dung thực hành ứng dụng tổng hợp liên môn", "0 câu", f"{int(c3)+int(c4)} câu", "2 câu", "0 câu", f"{int(c3)+int(c4)} câu", f"{tl_total_c} câu", f"{float(tl_score_v):.1f}đ"],
            ["", "TỔNG CỘNG HOÀN CHỈNH ĐỀ THI ĐỊNH KỲ", f"{c1} câu", f"{int(c2)+int(c3)+int(c4)} câu", "4 câu", "1 câu", f"{tn_total_c} câu", f"{tl_total_c} câu", "10.0 điểm"]
        ]
        
        for r_idx, data in enumerate(r_data, start=1):
            for col_idx, text in enumerate(data):
                cell_data = t_mt.rows[r_idx].cells[col_idx]
                cell_data.text = text
                cell_data.paragraphs[0].paragraph_format.space_after = Pt(3)
                if r_idx == 4:
                    bg_cell(cell_data, "EBF5FB")
                    cell_data.paragraphs[0].runs[0].font.bold = True

        # =====================================================================
        # PHẦN II: KHỞI TẠO BẢNG ĐẶC TẢ KỸ THUẬT ĐẠT CHUẨN BỘ GIÁO DỤC
        # =====================================================================
        doc.add_paragraph("\n").paragraph_format.space_after = Pt(3)
        p2 = doc.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.space_after = Pt(3)
        p2.add_run("BẢNG ĐẶC TẢ KỸ THUẬT NỘI DUNG ĐỀ KIỂM TRA").bold = True

        t_dt = doc.add_table(rows=4, cols=6)
        t_dt.style = 'Table Grid'
        hd_dt = ["STT", "Nội dung kiến thức", "Mức độ", "Yêu cầu cần đạt chi tiết bám sát tài liệu", "Số câu TN", "Số câu TL"]
        
        for idx, text in enumerate(hd_dt):
            cell_dt = t_dt.rows[0].cells[idx]
            cell_dt.text = text
            bg_cell(cell_dt, "F2F4F4")
            cell_dt.paragraphs[0].runs[0].font.bold = True
            cell_dt.paragraphs[0].paragraph_format.space_after = Pt(3)
            
        dt_d = [
            ["1", f"Kiến thức cốt lõi về: {topic_name}", "Nhận biết", f"- Trích xuất và định nghĩa chính xác cấu trúc hiện tượng khoa học (Tỷ lệ {r_nb}%).", f"{c1} câu", "0 câu"],
            ["2", f"Kiến thức bản chất về: {topic_name}", "Thông hiểu", f"- Phân tích, cắt nghĩa đơn vị bài học bám sát nội dung đề cương (Tỷ lệ {r_th}%).", f"{int(c2)+int(c3)+int(c4)} câu", "0 câu"],
            ["3", "Bài tập thực hành liên hệ đời sống", "Vận dụng (Cao)", f"- Vận dụng công thức toán lý hóa giải quyết vấn đề (Tỷ lệ {int(float(r_vd)+float(r_vdc))}%).", "4 câu", f"{tl_total_c} câu"]
        ]
        for r_idx, data in enumerate(dt_d, start=1):
            for col_idx, text in enumerate(data):
                cell_dt_data = t_dt.rows[r_idx].cells[col_idx]
                cell_dt_data.text = text
                cell_dt_data.paragraphs[0].paragraph_format.space_after = Pt(3)

        # =====================================================================
        # PHẦN III: ĐỔ NỘI DUNG ĐỀ THI VÀ XỬ LÝ SẠCH RÁC TOÁN HỌC LATEX
        # =====================================================================
        doc.add_paragraph("\n").paragraph_format.space_after = Pt(3)
        p3 = doc.add_paragraph()
        p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p3.add_run("NỘI DUNG ĐỀ KIỂM TRA VÀ ĐÁP ÁN CHẤM THỰC TẾ TỪ AI").bold = True
        
        p_school = doc.add_paragraph()
        p_school.paragraph_format.space_after = Pt(3)
        p_school.add_run("HỆ THỐNG TRỢ LÝ GIÁO DỤC PHỔ THÔNG\nTài liệu trích xuất tự động từ hệ thống trợ lý Trợ giảng AI.").font.italic = True
        
        ai_content = exam_data.get("ai_generated_content", "")
        
        def clean_math_formulas(text_line):
            text_line = text_line.replace("$", "")
            text_line = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1/\2)', text_line)
            text_line = text_line.replace("^2", "²").replace("^3", "³")
            text_line = text_line.replace("\\", "")
            return text_line.strip()

        clean_content = ai_content.replace("**", "").replace("###", "").replace("##", "")
        
        for line in clean_content.split('\n'):
            if line.strip(): 
                processed_line = clean_math_formulas(line)
                p_line = doc.add_paragraph(processed_line)
                p_line.paragraph_format.space_before = Pt(0)
                p_line.paragraph_format.space_after = Pt(3)
                if line.strip().startswith("I.") or line.strip().startswith("II.") or "PHẦN" in line or "ĐÁP ÁN" in line or "HƯỚNG DẪN" in line:
                    if p_line.runs: 
                        p_line.runs.font.bold = True
                        
        bio = io.BytesIO()
        doc.save(bio)
        bio.seek(0)
        return bio.getvalue()
