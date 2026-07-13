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
        """Bộ lọc chuyên sâu: Chuyển đổi ký hiệu Toán học sang Unicode an toàn tuyệt đối"""
        # Xóa ký hiệu khối toán học
        text = text.replace("$", "").replace("\\[", "").replace("\\]", "")
        
        # 1. THAY THẾ AN TOÀN (Sửa lỗi bad escape \p)
        # Sử dụng chuỗi Replace cơ bản cho các ký tự chứa \, không dùng Regex
        exact_map = {
            r'\neq': '≠', r'\pm': '±', r'\triangle': '△',
            r'\mathbb{R}': 'ℝ', r'mathbb{R}': 'ℝ',
            r'\in': '∈', r'\le': '≤', r'\ge': '≥',
            r'\pi': 'π', r'\alpha': 'α', r'\beta': 'β', 
            r'\sqrt': '√', r'\rightarrow': '→', r'\leftrightarrow': '↔',
            r'\infty': '∞', '^2': '²', '^3': '³'
        }
        for tex, uni in exact_map.items():
            text = text.replace(tex, uni)
            
        # 2. XỬ LÝ AI QUÊN DẤU BACKSLASH (Dùng Regex Word Boundary \b)
        safe_regex = {
            r'\bneq\b': '≠',
            r'\bpm\b': '±',
            r'\btriangle\b': '△',
            r'\ble\b': '≤',
            r'\bge\b': '≥',
            r'\bpi\b': 'π',
            r'\balpha\b': 'α',
            r'\bbeta\b': 'β',
            r'\binfty\b': '∞',
            # Bảo vệ Tiếng Việt: Chỉ đổi "x in" thành "x ∈" khi đứng trước ℝ hoặc khoảng trắng
            r'\bx in\b(?=\s*ℝ)': 'x ∈',
            r'\bx in\b(?=\s*math)': 'x ∈'
        }
        for pat, uni in safe_regex.items():
            text = re.sub(pat, uni, text)
            
        # 3. Xử lý phân số dạng \frac{a}{b} hoặc frac{a}{b} -> (a)/(b)
        text = re.sub(r'\\?frac\{([^}]+)\}\{([^}]+)\}', r'(\1)/(\2)', text)
        return text

    @staticmethod
    def _parse_inline_formatting(paragraph, text: str):
        """Xử lý in đậm (**), in nghiêng (*) trên cùng một dòng"""
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
            cells = [cell.strip() for cell in row_text.split('|')][1:-1] 
            
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
            
            # XỬ LÝ BẢNG (TABLE)
            if line.startswith('|') and line.endswith('|'):
                in_table = True
                table_rows.append(line)
                continue
            else:
                if in_table:
                    MarkdownParser._build_word_table(doc, table_rows)
                    in_table = False
                    table_rows = []
                    doc.add_paragraph() 
            
            if not line:
                continue

            line = MarkdownParser.clean_math(line)

            # XỬ LÝ TIÊU ĐỀ (HEADING)
            heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
            if heading_match:
                level = len(heading_match.group(1))
                text_content = heading_match.group(2)
                h = doc.add_heading(text_content, level=level)
                for run in h.runs: run.font.color.rgb = RGBColor(0, 0, 0)
                continue

            # XỬ LÝ DANH SÁCH
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

            # VĂN BẢN THƯỜNG
            p = doc.add_paragraph()
            MarkdownParser._parse_inline_formatting(p, line)

        if in_table:
            MarkdownParser._build_word_table(doc, table_rows)
