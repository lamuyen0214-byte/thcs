# =====================================================================
# FILE: export/export_word.py (TỆP ĐIỀU PHỐI ĐỒNG BỘ NẠP MODULE MA TRẬN ĐỘNG CHUẨN)
# =====================================================================
import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
import re

# Nạp trực tiếp cấu trúc từ 2 module độc lập vừa tạo ở trên
from export.equation_formatter import EquationFormatter
from export.table_builder import TableBuilder

class WordExportEngine:
    @staticmethod
    def export_to_word(exam_data):
        """
        Hàm trung tâm phối hợp bốc ma trận động, bảng đặc tả động 
        và đề thi chính thức đổ trực tiếp ra luồng Bytes bản in Word.
        """
        doc = docx.Document()
        
        # Cấu hình căn lề văn bản hành chính quy chuẩn Việt Nam
        for section in doc.sections:
            section.top_margin = Inches(0.79)
            section.bottom_margin = Inches(0.79)
            section.left_margin = Inches(1.18)
            section.right_margin = Inches(0.79)
            
        doc.styles['Normal'].font.name = 'Times New Roman'
        doc.styles['Normal'].font.size = Pt(12)

        # 1. GỌI HOẠT ĐỘNG MODULE DỰNG BẢNG MA TRẬN ĐỘNG CÔNG VĂN 799 (ĐÃ SỬA LỖI _ROWS)
        TableBuilder.build_matrix_table(doc, exam_data)
        
        # 2. GỌI HOẠT ĐỘNG MODULE DỰNG BẢNG ĐẶC TẢ KỸ THUẬT ĐỘNG CHUẨN
        TableBuilder.build_specification_table(doc, exam_data)

        # 3. TIẾN HÀNH ĐỔ VĂN BẢN ĐỀ THI VÀ DIỆT SẠCH RÁC LATEX TOÁN HỌC
        doc.add_paragraph("\n").paragraph_format.space_after = Pt(3)
        p3 = doc.add_paragraph()
        p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p3.paragraph_format.space_after = Pt(3)
        p3.add_run("NỘI DUNG ĐỀ KIỂM TRA VÀ ĐÁP ÁN CHẤM CHI TIẾT").bold = True
        
        ai_content = exam_data.get("ai_generated_content", "")
        clean_content = ai_content.replace("**", "").replace("###", "").replace("##", "")
        
        for line in clean_content.split('\n'):
            if line.strip():
                p_line = doc.add_paragraph()
                p_line.paragraph_format.space_before = Pt(0)
                p_line.paragraph_format.space_after = Pt(3) # Khóa khoảng cách dòng lề hành chính 3pt
                
                # Gọi bộ định dạng để nạp văn bản sạch rác toán học vào hàng dòng
                EquationFormatter.inject_math_run(p_line, line.strip())
                
                if line.strip().startswith("I.") or line.strip().startswith("II.") or "PHẦN" in line or "ĐÁP ÁN" in line or "HƯỚNG DẪN" in line:
                    if p_line.runs:
                        p_line.runs[0].font.bold = True
                        
        # Đóng gói hồ sơ đề kiểm tra và trả về luồng Bytes download
        bio = io.BytesIO()
        doc.save(bio)
        bio.seek(0)
        return bio.getvalue()
