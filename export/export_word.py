# =====================================================================
# FILE: export/export_word.py - PHẦN 1: KHỞI TẠO BỘ DIỆT RÁC TOÁN HỌC
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
    # =====================================================================
    # FILE: export/export_word.py - PHẦN 2: THUẬT TOÁN VẼ MA TRẬN ĐỀ KT 2 TẦNG
    # =====================================================================
    @staticmethod
    def build_matrix_table(doc, exam_data):
        """Thuật toán trộn ô Nhận biết/Thông hiểu phân tách 2 tầng TN và TL tách biệt"""
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
        for i in: 
            r0[i].merge(r0[i+1])
            r1[i].text, r1[i+1].text = "TN", "TL"
        r1[9].text = "TL"
        
        # Trộn dọc cô lập cho các cột không chia tầng
        for i in: r0[i].merge(r1[i])

        # Đổ màu nền và khóa chữ đậm tiêu đề
        for r_idx in:
            for cell in table.rows[r_idx].cells:
                bg_cell(cell, "F2F4F4")
                if cell.paragraphs and cell.paragraphs[0].runs: cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].paragraph_format.space_after = Pt(3)

        topic = exam_data.get("custom_req", "Nội dung đề thi")
        c1 = exam_data.get("c1", "12")
        c2 = exam_data.get("c2", "2")
        tn_score_v = exam_data.get("tn_score", "4.0")
        tl_score_v = exam_data.get("tl_score", "6.0")

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
    # =====================================================================
    # FILE: export/export_word.py - PHẦN 3: THUẬT TOÁN VẼ BẢNG ĐẶC TẢ KỸ THUẬT
    # =====================================================================
    @staticmethod
    def build_specification_table(doc, exam_data):
        """Vẽ bảng đặc tả kĩ thuật tự co giãn thông minh khóa chiều rộng"""
        table = doc.add_table(rows=3, cols=5)
        table.style = 'Table Grid'
        table.autofit = False
        
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
    # =====================================================================
    # FILE: export/export_word.py - PHẦN 4: HÀM ĐIỀU PHỐI HỢP NHẤT TRUNG TÂM
    # =====================================================================
    @staticmethod
    def export_to_word(data_cache):
        """Hàm điều phối trung tâm hợp nhất: Tự động phân tách phân hệ Đề thi hoặc Giáo án KHBD"""
        doc = docx.Document()
        
        # Cấu hình lề hành chính chuẩn văn bản Việt Nam cho toàn bộ file Word xuất ra
        for section in doc.sections:
            section.top_margin, section.bottom_margin = Inches(0.79), Inches(0.79)
            section.left_margin, section.right_margin = Inches(1.18), Inches(0.79)
            
        doc.styles['Normal'].font.name = 'Times New Roman'
        doc.styles['Normal'].font.size = Pt(12)

        # 🔄 KIỂM TRA KẾT NỐI PHÂN HỆ: Nếu là dữ liệu xuất bản Giáo án KHBD 5512
        if data_cache.get("is_khbd") == True:
            p_top = doc.add_paragraph()
            p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_top.add_run(f"KẾ HOẠCH BÀI DẠY MÔN {data_cache.get('subject','').upper()} - {data_cache.get('grade','').upper()}").bold = True
            
            p_title = doc.add_paragraph()
            p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_title.add_run(f"CHỦ ĐỀ/BÀI HỌC: {data_cache.get('title','').upper()}\n(Mẫu thiết kế: {data_cache.get('style','') if data_cache.get('style','') else 'Chuẩn 5512'} - Thời lượng: {data_cache.get('duration','2')} tiết)").bold = True
            p_title.runs[0].font.size = Pt(13)
            
            p_line = doc.add_paragraph("Bộ sách giáo khoa độc tôn: Kết nối tri thức với cuộc sống (Áp dụng từ năm 2026)\n")
            p_line.runs[0].font.italic = True
            
            ai_text = data_cache.get("ai_content_raw", "")
            
        # 🔄 KIỂM TRA KẾT NỐI PHÂN HỆ: Nếu là dữ liệu ĐỀ KIỂM TRA VÀ MA TRẬN 2 TẦNG
        else:
            # 1. Kích hoạt vẽ bảng ma trận định kỳ trộn ô Công văn 799
            WordExportEngine.build_matrix_table(doc, data_cache)
            doc.add_paragraph("\n")
            
            # 2. Kích hoạt vẽ bảng đặc tả kỹ thuật khóa cứng kích thước chiều rộng
            WordExportEngine.build_specification_table(doc, data_cache)
            doc.add_paragraph("\n")
            
            p_exam = doc.add_paragraph()
            p_exam.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_exam.add_run(f"NỘI DUNG ĐỀ KIỂM TRA VÀ ĐÁP ÁN CHẤM CHI TIẾT TỪ AI\n(Đề mục: {data_cache.get('custom_req','')})").bold = True
            
            ai_text = data_cache.get("ai_generated_content", "")

        # 3. Tiến hành bóc tách ký tự, đổ văn bản và diệt sạch rác toán học LaTeX cho cả 2 phân hệ
        clean_content = ai_text.replace("**", "").replace("###", "").replace("##", "")
        for line in clean_content.split('\n'):
            if line.strip():
                # Ép bọc dòng chữ qua bộ dọn rác toán học Equation
                processed = WordExportEngine.clean_math_formulas(line)
                p_item = doc.add_paragraph(processed)
                p_item.paragraph_format.space_before = Pt(0)
                p_item.paragraph_format.space_after = Pt(3) # Cấu hình dòng khít lề 3pt hành chính
                
                # Tự động viết đậm các tiêu đề mục lớn (I, II, III, Hoạt động)
                if line.strip().startswith("I.") or line.strip().startswith("II.") or line.strip().startswith("III.") or "Hoạt động" in line or "MỤC TIÊU" in line or "TIẾN TRÌNH" in line or "ĐÁP ÁN" in line or "HƯỚNG DẪN" in line:
                    if p_item.runs: p_item.runs[0].font.bold = True

        bio = io.BytesIO()
        doc.save(bio)
        bio.seek(0)
        return bio.getvalue()
