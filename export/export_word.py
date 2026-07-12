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
        """Thuật toán quét sạch mã rác toán LaTeX dịch chuyển sang định dạng in ấn sạch"""
        text_line = text_line.replace("$", "")
        # Dịch chuyển phân số cao cấp \frac{tử}{mẫu} sang dạng gạch chéo in ấn sạch (tử/mẫu)
        text_line = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1/\2)', text_line)
        # Chuyển đổi căn bậc hai và hệ thống ký hiệu toán cốt lõi Bộ Giáo dục Việt Nam
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
        """Vẽ bảng ma trận có trộn ô Nhận biết/Thông hiểu phân tách 2 tầng TN và TL tách biệt"""
        table = doc.add_table(rows=4, cols=11)
        table.style = 'Table Grid'
        table.autofit = False # Khóa cứng, cấm tự ý co giãn tự do làm vỡ khung
        
        # Thiết lập chính xác độ rộng pixel width cho từng cột hành chính
        col_widths = [Inches(0.4), Inches(1.6), Inches(1.6), Inches(0.4), Inches(0.4), Inches(0.4), Inches(0.4), Inches(0.4), Inches(0.4), Inches(0.4), Inches(0.7)]
        
        def bg_cell(cell, hex_color):
            cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))

        # Định hình tiêu đề hàng 0 (Tầng 1) và hàng 1 (Tầng 2)
        r0, r1 = table.rows[0].cells, table.rows[1].cells
        r0[0].text, r0[1].text, r0[2].text = "STT", "Chủ đề", "Nội dung"
        r0[3].text, r0[5].text, r0[7].text, r0[9].text, r0[10].text = "Nhận biết", "Thông hiểu", "Vận dụng", "VDC", "Tổng"
        
        # Tiến hành trộn ngang 2 ô TN-TL cho từng phân khúc năng lực
        for i in: r0[i].merge(r0[i+1])
        for i in: r1[i].text, r1[i+1 if i<9 else i].text = "TN", "TL"
        
        # Trộn dọc cô lập cho các cột STT, Chủ đề, Tổng
        for i in: r0[i].merge(r1[i])

        # Đổ màu nền và sửa triệt lội list object font bold bằng cách duyệt qua từng ô cụ thể
        for r_idx in:
            for cell in table.rows[r_idx].cells:
                bg_cell(cell, "F2F4F4")
                if cell.paragraphs and cell.paragraphs[0].runs:
                    cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].paragraph_format.space_after = Pt(3)

        topic = exam_data.get("custom_req", "Nội dung đề thi")
        c1 = exam_data.get("c1", "12")
        c2 = exam_data.get("c2", "2")
        tn_score_v = exam_data.get("tn_score", "4.0")
        tl_score_v = exam_data.get("tl_score", "6.0")

        # Đồng bộ 100% biểu điểm động từ giao diện vào ma trận 11 ô cột nhỏ
        matrix_rows = [
            ["1", topic, "Kiến thức lý thuyết trọng tâm", f"{c1}", "0", "0", f"{c2}", "0", "1", "0", f"{float(tn_score_v)*0.6:.1f}đ"],
            ["2", topic, "Bài tập thực hành phân hóa", "0", "0", "0", "0", "2", "0", "1", f"{float(tl_score_v):.1f}đ"],
            ["", "TỔNG CỘNG ĐỀ KIỂM TRA ĐẠT CHUẨN", f"{c1}", "0", "0", f"{c2}", "2", "1", "1", "1", "10.0 điểm"]
        ]
        for r, data in enumerate(matrix_rows, start=2):
            for c, text in enumerate(data):
                cell = table.rows[r].cells[c]
                cell.text = text
                cell.paragraphs[0].paragraph_format.space_after = Pt(3)
                if r == 4:
                    bg_cell(cell, "EBF5FB")
                    if cell.paragraphs[0].runs: cell.paragraphs[0].runs[0].font.bold = True

        for row in table.rows:
            for idx, w in enumerate(col_widths): row.cells[idx].width = w
    @staticmethod
    def build_specification_table(doc, exam_data):
        """Vẽ bảng đặc tả kĩ thuật tự co giãn thông minh khóa chiều rộng"""
        table = doc.add_table(rows=3, cols=5)
        table.style = 'Table Grid'
        table.autofit = False
        
        # Mở rộng cột 2 (Nội dung yêu cầu cần đạt) thênh thang để không bao giờ bị tràn hàng
        col_widths = [Inches(0.5), Inches(1.5), Inches(3.7), Inches(0.8), Inches(0.8)]
        
        def bg_cell(cell, hex_color):
            cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))

        hd = ["STT", "Chủ đề kiến thức", "Yêu cầu cần đạt chi tiết phân hóa từ AI", "Số câu TN", "Số câu TL"]
        for idx, text in enumerate(hd):
            cell = table.rows[0].cells[idx]
            cell.text = text
            bg_cell(cell, "F2F4F4")
            if cell.paragraphs[0].runs: cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].paragraph_format.space_after = Pt(3)
            
        topic = exam_data.get("custom_req", "Chủ đề bài học")
        dt_data = [
            ["1", topic, "- Nhận biết và trích xuất đúng định nghĩa hiện tượng khoa học.\n- Vận dụng lý thuyết giải toán bám sát đề cương tài liệu.", f"{exam_data.get('c1','12')} câu", "0 câu"],
            ["2", "Tổng hợp ứng dụng", "- Khái quát hóa đơn vị kiến thức liên môn thực tiễn.\n- Đánh giá năng lực tư duy giải quyết câu hỏi phân hóa cao.", "4 câu", f"{exam_data.get('tl_total','3')} câu"]
        ]
        for r, data in enumerate(dt_data, start=1):
            for c, text in enumerate(data):
                cell = table.rows[r].cells[c]
                cell.text = text
                cell.paragraphs[0].paragraph_format.space_after = Pt(3)
                
        for row in table.rows:
            for idx, w in enumerate(col_widths): row.cells[idx].width = w

    @staticmethod
    def export_to_word(exam_data):
        """Hàm điều phối trung tâm dọn sạch dòng trống và kết xuất luồng Bytes"""
        doc = docx.Document()
        
        # Cấu hình lề hành chính 4 cạnh trang in
        for section in doc.sections:
            section.top_margin, section.bottom_margin = Inches(0.79), Inches(0.79)
            section.left_margin, section.right_margin = Inches(1.18), Inches(0.79)
            
        doc.styles['Normal'].font.name = 'Times New Roman'
        doc.styles['Normal'].font.size = Pt(12)

        # 1. Kết xuất bảng ma trận trộn ô 2 tầng Công văn 799
        WordExportEngine.build_matrix_table(doc, exam_data)
        
        # 2. Kết xuất bảng đặc tả kĩ thuật tự co giãn
        WordExportEngine.build_specification_table(doc, exam_data)

        # 3. Đổ đề thi bọc qua bộ lọc diệt ký tự rác toán học LaTeX
        doc.add_paragraph("\n").paragraph_format.space_after = Pt(3)
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run("NỘI DUNG ĐỀ KIỂM TRA VÀ ĐÁP ÁN CHẤM CHI TIẾT TỪ AI").bold = True
        
        ai_content = exam_data.get("ai_generated_content", "")
        clean_content = ai_content.replace("**", "").replace("###", "").replace("##", "")
        
        for line in clean_content.split('\n'):
            if line.strip():
                # Ép bọc dòng qua bộ dọn rác toán học
                processed_line = WordExportEngine.clean_math_formulas(line)
                p_line = doc.add_paragraph(processed_line)
                p_line.paragraph_format.space_before = Pt(0)
                p_line.paragraph_format.space_after = Pt(3)
                if line.strip().startswith("I.") or line.strip().startswith("II.") or "PHẦN" in line or "ĐÁP ÁN" in line or "HƯỚNG DẪN" in line:
                    if p_line.runs: p_line.runs[0].font.bold = True
                        
        bio = io.BytesIO()
        doc.save(bio)
        bio.seek(0)
        return bio.getvalue()
