# =====================================================================
# FILE: export/export_word.py (SỬA TRIỆT ĐỂ LỖI DUYỆT MẢNG Ô OUT OF RANGE)
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
    def clean_math_formulas(text_line):
        """Bộ lọc quét sạch mã rác toán LaTeX chuyển sang định dạng in ấn sạch"""
        text_line = text_line.replace("$", "")
        text_line = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1/\2)', text_line)
        text_line = re.sub(r'\\sqrt\{([^}]+)\}', r'√(\1)', text_line)
        text_line = text_line.replace("\\sum", "∑").replace("\\lim", "lim").replace("\\pi", "π")
        text_line = text_line.replace("\\alpha", "α").replace("\\beta", "β").replace("\\Delta", "Δ")
        text_line = text_line.replace("\\rightarrow", "→").replace("\\leftrightarrow", "↔")
        text_line = text_line.replace("\\le", "≤").replace("\\ge", "≥").replace("\\approx", "≈")
        text_line = text_line.replace("\\in", "∈").replace("\\subset", "⊂")
        text_line = text_line.replace("^2", "²").replace("^3", "³")
        text_line = text_line.replace("\\", "")
        return text_line.strip()

    @staticmethod
    def build_matrix_table(doc, exam_data):
        """Vẽ bảng ma trận trộn ô Công văn 799 - Sửa sạch lỗi duyệt mảng ô cell"""
        table = doc.add_table(rows=4, cols=11)
        table.style = 'Table Grid'
        table.autofit = False
        
        col_widths = [Inches(0.4), Inches(1.6), Inches(1.6), Inches(0.4), Inches(0.4), Inches(0.4), Inches(0.4), Inches(0.4), Inches(0.4), Inches(0.4), Inches(0.7)]
        
        def bg_cell(cell, hex_color):
            cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))

        # Khởi tạo tiêu đề gốc tại các ô cell tĩnh ban đầu
        table.cell(0, 0).text = "STT"
        table.cell(0, 1).text = "Chủ đề"
        table.cell(0, 2).text = "Nội dung"
        table.cell(0, 3).text = "Nhận biết"
        table.cell(0, 5).text = "Thông hiểu"
        table.cell(0, 7).text = "Vận dụng"
        table.cell(0, 9).text = "VDC"
        table.cell(0, 10).text = "Tổng"
        
        # Tiến hành trộn ngang tầng 1 và điền nhãn TN/TL cho tầng 2 bằng chỉ số tọa độ
        for col_idx in:
            table.cell(0, col_idx).merge(table.cell(0, col_idx + 1))
            table.cell(1, col_idx).text = "TN"
            table.cell(1, col_idx + 1).text = "TL"
        table.cell(1, 9).text = "TL"
        
        # Tiến hành trộn dọc cô lập cho các cột không chia tầng
        for col_idx in:
            table.cell(0, col_idx).merge(table.cell(1, col_idx))

        # ĐÃ VÁ LỖI CHÍ MẠNG OUT OF RANGE: Duyệt trực tiếp qua tập hợp cell thực tế thay vì tọa độ cứng range(11)
        for r_idx in:
            for cell in table.rows[r_idx].cells:
                bg_cell(cell, "F2F4F4")
                if cell.paragraphs and cell.paragraphs[0].runs:
                    cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].paragraph_format.space_after = Pt(3)

        topic = exam_data.get("custom_req", "Nội dung đề thi")
        c1 = exam_data.get("c1", 12)
        c2 = exam_data.get("c2", 2)
        c3 = exam_data.get("c3", 1)
        c4 = exam_data.get("c4", 1)
        tn_score_v = exam_data.get("tn_score", "4.0")
        tl_score_v = exam_data.get("tl_score", "6.0")

        matrix_rows = [
            ["1", topic, "Kiến thức lý thuyết trọng tâm", f"{c1}", "0", "0", f"{c2}", "0", "1", "0", f"{float(tn_score_v)*0.6:.1f}đ"],
            ["2", topic, "Bài tập thực hành phân hóa", "0", "0", "0", "0", f"{int(c3)+int(c4)}", "0", "1", f"{float(tl_score_v):.1f}đ"],
            ["", "TỔNG CỘNG ĐỀ KIỂM TRA ĐẠT CHUẨN", f"{c1}", "0", "0", f"{c2}", "2", "1", "1", "1", "10.0 điểm"]
        ]
        for r, data in enumerate(matrix_rows, start=2):
            for c, text in enumerate(data):
                cell = table.cell(r, c)
                cell.text = text
                cell.paragraphs[0].paragraph_format.space_after = Pt(3)
                if r == 4:
                    bg_cell(cell, "EBF5FB")
                    if cell.paragraphs[0].runs: cell.paragraphs[0].runs[0].font.bold = True

        for row in table.rows:
            for idx, w in enumerate(col_widths): row.cells[idx].width = w
            
    @staticmethod
    def build_specification_table(doc, exam_data):
        table = doc.add_table(rows=3, cols=5)
        table.style = 'Table Grid'
        table.autofit = False
        
        col_widths = [Inches(0.5), Inches(1.5), Inches(3.7), Inches(0.8), Inches(0.8)]
        def bg_cell(hex_color, cell_obj):
            cell_obj._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))

        hd = ["STT", "Chủ đề kiến thức", "Yêu cầu cần đạt chi tiết phân hóa từ AI", "Số câu TN", "Số câu TL"]
        for idx, text in enumerate(hd):
            cell = table.cell(0, idx)
            cell.text = text
            bg_cell("F2F4F4", cell)
            if cell.paragraphs[0].runs: cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].paragraph_format.space_after = Pt(3)
            
        topic = exam_data.get("custom_req", "Chủ đề bài học")
        dt_data = [
            ["1", topic, "- Nhận biết và trích xuất đúng định nghĩa hiện tượng khoa học.\n- Vận dụng lý thuyết giải toán bám sát đề cương tài liệu.", f"{exam_data.get('c1','12')} câu", "0 câu"],
            ["2", "Tổng hợp ứng dụng", "- Khái quát hóa đơn vị kiến thức liên môn thực tiễn.\n- Đánh giá năng lực tư duy giải quyết câu hỏi phân hóa cao.", "4 câu", f"{exam_data.get('tl_total','3')} câu"]
        ]
        for r, data in enumerate(dt_data, start=1):
            for c, text in enumerate(data):
                cell = table.cell(r, c)
                cell.text = text
                cell.paragraphs[0].paragraph_format.space_after = Pt(3)
                
        for row in table.rows:
            for idx, w in enumerate(col_widths): row.cells[idx].width = w

    @staticmethod
    def export_to_word(data_cache):
        """Hàm điều phối trung tâm kết xuất tệp Word hành chính"""
        doc = docx.Document()
        for section in doc.sections:
            section.top_margin, section.bottom_margin = Inches(0.79), Inches(0.79)
            section.left_margin, section.right_margin = Inches(1.18), Inches(0.79)
            
        doc.styles['Normal'].font.name = 'Times New Roman'
        doc.styles['Normal'].font.size = Pt(12)

        # Trích xuất trọn vẹn văn bản thô đồng bộ từ khóa cho cả 2 cổng phân hệ
        ai_text = data_cache.get("ai_generated_content", "")

        if data_cache.get("is_khbd") == True:
            p_top = doc.add_paragraph()
            p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_top.add_run(f"KẾ HOẠCH BÀI DẠY MÔN {data_cache.get('subject','').upper()} - {data_cache.get('grade','').upper()}").bold = True
        else:
            WordExportEngine.build_matrix_table(doc, data_cache)
            doc.add_paragraph("\n")
            WordExportEngine.build_specification_table(doc, data_cache)
            doc.add_paragraph("\n")

        clean_content = ai_text.replace("**", "").replace("###", "").replace("##", "")
        for line in clean_content.split('\n'):
            if line.strip():
                processed = WordExportEngine.clean_math_formulas(line)
                p_item = doc.add_paragraph(processed)
                p_item.paragraph_format.space_before = Pt(0)
                p_item.paragraph_format.space_after = Pt(3)
                if line.strip().startswith("I.") or line.strip().startswith("II.") or "Hoạt động" in line or "MỤC TIÊU" in line or "TIẾN TRÌNH" in line:
                    if p_item.runs: p_item.runs[0].font.bold = True

        bio = io.BytesIO()
        doc.save(bio)
        bio.seek(0)
        return bio.getvalue()
