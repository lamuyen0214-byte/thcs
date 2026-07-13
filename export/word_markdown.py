"""
Module: export/word_markdown.py
Nhiệm vụ: Chuyển đổi Markdown và Toán học (LaTeX) sang định dạng Microsoft Word nguyên bản.
"""
import re
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

class MarkdownParser:
    @staticmethod
    def clean_math(text: str) -> str:
        """Bộ lọc chuyên sâu: Chuyển đổi ký hiệu Toán học LaTeX sang Unicode nét chuẩn Word"""
        # Xóa ký hiệu khối toán học
        text = text.replace("$", "").replace("\\[", "").replace("\\]", "")
        
        # Ánh xạ các ký hiệu toán học phổ biến (Cả có và không có dấu backslash)
        math_map = {
            r'\neq': '≠', r'\bneq\b': '≠',
            r'\pm': '±', r'\bpm\b': '±',
            r'\triangle': '△', r'\btriangle\b': '△',
            r'\mathbb{R}': 'ℝ', r'\bmathbb\{R\}\b': 'ℝ',
            r'\in': '∈', r'\bin\b': '∈',
            r'\le': '≤', r'\ble\b': '≤',
            r'\ge': '≥', r'\bge\b': '≥',
            r'\pi': 'π', r'\bpi\b': 'π',
            r'\alpha': 'α', r'\bbeta\b': 'β',
            r'\sqrt': '√',
            r'\rightarrow': '→', r'\leftrightarrow': '↔',
            r'\infty': '∞', r'\binfty\b': '∞',
            r'^2': '²', r'^3': '³'
        }
        
        # Thực hiện thay thế bằng Regex để quét chính xác từ
        for tex, uni in math_map.items():
            text = re.sub(tex, uni, text)
            
        # Xử lý phân số dạng \frac{a}{b} hoặc frac{a}{b} -> (a)/(b)
        text = re.sub(r'\\?frac\{([^}]+)\}\{([^}]+)\}', r'(\1)/(\2)', text)
        return text

    @staticmethod
    def _parse_inline_formatting(paragraph, text: str):
        """Xử lý in đậm (**), in nghiêng (*) trên cùng một dòng"""
        # Chia tách chuỗi dựa trên các cặp dấu sao
        parts = re.split(r'(\*\*.*?\*\*|\*.*?\*)', text)
        
        for part in parts:
            if not part:
                continue
            if part.startswith('**') and part.endswith('**'):
                run = paragraph.add_run(part[2:-2])
                run.bold = True
            elif part.startswith('*') and part.endswith('*'):
                run = paragraph.add_run(part[1:-1])
                run.italic = True
            else:
                paragraph.add_run(part)

    @staticmethod
    def _build_word_table(doc, table_rows_data):
        """Kiến tạo Bảng Word tự động từ cấu trúc Bảng Markdown"""
        if not table_rows_data:
            return

        # Tính toán số cột dựa trên dòng đầu tiên
        num_cols = len([cell for cell in table_rows_data[0].split('|') if cell.strip()])
        if num_cols == 0: return

        table = doc.add_table(rows=len(table_rows_data), cols=num_cols)
        table.style = 'Table Grid'
        table.autofit = True

        for r_idx, row_text in enumerate(table_rows_data):
            # Lọc bỏ dấu | ở đầu và cuối dòng
            cells = [cell.strip() for cell in row_text.split('|')][1:-1] 
            
            # Đảm bảo không bị lỗi IndexError nếu hàng thiếu cột
            for c_idx in range(min(num_cols, len(cells))):
                cell_text = cells[c_idx]
                
                # Bỏ qua dòng phân cách bảng của Markdown (ví dụ: |---|---|)
                if set(cell_text.replace(":", "")) == {"-"}:
                    continue 
                
                cell_p = table.cell(r_idx, c_idx).paragraphs[0]
                MarkdownParser._parse_inline_formatting(cell_p, MarkdownParser.clean_math(cell_text))
                
                # In đậm hàng tiêu đề
                if r_idx == 0:
                    for run in cell_p.runs: run.bold = True

    @staticmethod
    def parse(doc, markdown_text: str):
        """Hàm điều phối trung tâm: Đọc từng dòng và vẽ ra Word"""
        lines = markdown_text.split('\n')
        
        in_table = False
        table_rows = []

        for line in lines:
            line = line.strip()
            
            # 1. XỬ LÝ BẢNG (TABLE) - Khắc phục ma trận bị cụt
            if line.startswith('|') and line.endswith('|'):
                in_table = True
                table_rows.append(line)
                continue
            else:
                if in_table:
                    MarkdownParser._build_word_table(doc, table_rows)
                    in_table = False
                    table_rows = []
                    doc.add_paragraph() # Dòng trống sau bảng
            
            if not line:
                continue

            # Dọn dẹp Toán học trước khi xét định dạng
            line = MarkdownParser.clean_math(line)

            # 2. XỬ LÝ TIÊU ĐỀ (HEADING) - Khắc phục thừa dấu ####
            heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
            if heading_match:
                level = len(heading_match.group(1))
                text_content = heading_match.group(2)
                h = doc.add_heading(text_content, level=level)
                # Đổi màu tiêu đề về đen chuẩn thay vì xanh dương của Word
                for run in h.runs: run.font.color.rgb = RGBColor(0, 0, 0)
                continue

            # 3. XỬ LÝ DANH SÁCH (BULLETS/NUMBERS) - Khắc phục dấu * đầu dòng
            list_match = re.match(r'^[\*\-]\s+(.*)', line)
            if list_match:
                p = doc.add_paragraph(style='List Bullet')
                MarkdownParser._parse_inline_formatting(p, list_match.group(1))
                continue
                
            num_match = re.match(r'^(\d+\.)\s+(.*)', line)
            if num_match:
                p = doc.add_paragraph(style='List Number')
                MarkdownParser._parse_inline_formatting(p, num_match.group(2))
                continue

            # 4. ĐOẠN VĂN BẢN BÌNH THƯỜNG (PARAGRAPH)
            p = doc.add_paragraph()
            MarkdownParser._parse_inline_formatting(p, line)

        # Chốt hạ nếu bảng nằm ở tận cùng văn bản
        if in_table:
            MarkdownParser._build_word_table(doc, table_rows)
