"""
Module: export/word_markdown.py
Nhiệm vụ: Bộ phân tích cú pháp (Parser) chuyển đổi văn bản thô thành AST Nodes.
Cơ chế: Không thao tác trực tiếp với Word. Chỉ bóc tách chuỗi thành các Token (Heading, Table, Math, Text).
"""

import re
from typing import List, Dict, Any

class MarkdownTokenizer:
    @staticmethod
    def _parse_inline_content(text: str) -> List[Dict[str, str]]:
        """
        Bóc tách các thành phần nội dòng (Inline): Text bình thường, Text in đậm/nghiêng và Công thức Toán.
        Bảo vệ tuyệt đối các công thức Toán nội dòng ($...$ hoặc \(...\)) khỏi Regex thông thường.
        """
        tokens = []
        if not text:
            return tokens

        # Tách chuỗi bằng các block toán học inline: $math$ hoặc \(math\)
        # Cấu trúc regex này giữ lại các block toán học làm phần tử trong danh sách kết quả
        math_pattern = r'(\$.*?\$|\\\([^()]*\\\))'
        parts = re.split(math_pattern, text)

        for part in parts:
            if not part:
                continue
                
            # Nếu là block toán học
            if (part.startswith('$') and part.endswith('$')) or \
               (part.startswith(r'\(') and part.endswith(r'\)')):
                clean_math = part.strip('$').removeprefix(r'\(').removesuffix(r'\)')
                tokens.append({"type": "inline_math", "content": clean_math})
            else:
                # Nếu là text thường, tiếp tục bóc tách in đậm, in nghiêng
                # (Sẽ được xử lý định dạng ở tầng StyleManager, ở đây chỉ lưu chuỗi)
                tokens.append({"type": "text", "content": part})
                
        return tokens

    @staticmethod
    def _normalize_table(rows: List[str]) -> Dict[str, Any]:
        """
        Tiêu chuẩn hóa bảng: Cân bằng số cột, xử lý bảng khuyết ô, bóc tách Header.
        """
        valid_rows = []
        for r in rows:
            # Loại bỏ dòng kẻ phân cách Markdown (vd: |---|---|)
            clean_r = r.replace("|", "").replace("-", "").replace(":", "").strip()
            if not clean_r:
                continue
            valid_rows.append(r)
            
        if not valid_rows:
            return None

        # Tính số cột tối đa thực tế (trừ 2 đầu mút | trống do split)
        max_cols = max(len([c for c in row.split('|') if c.strip() or c == '']) - 2 for row in valid_rows)
        if max_cols <= 0:
            return None
        
        normalized_data = []
        for row in valid_rows:
            # Lấy các ô ở giữa, bỏ rác đầu đuôi
            cells = row.split('|')[1:-1]
            # Điền bù ô rỗng nếu hàng đó bị thiếu cột
            row_data = [cells[i].strip() if i < len(cells) else "" for i in range(max_cols)]
            
            # Đưa từng ô qua bộ phân tích inline để lấy AST của ô đó
            ast_row = [MarkdownTokenizer._parse_inline_content(cell) for cell in row_data]
            normalized_data.append(ast_row)

        return {
            "type": "table",
            "cols": max_cols,
            "headers": normalized_data[0] if len(normalized_data) > 0 else [],
            "rows": normalized_data[1:] if len(normalized_data) > 1 else []
        }

    @classmethod
    def parse(cls, markdown_text: str) -> List[Dict[str, Any]]:
        """
        Quét văn bản từ trên xuống dưới, phân loại thành các Block Level Nodes (Đoạn văn, Bảng, Danh sách...).
        """
        ast_nodes = []
        lines = markdown_text.split('\n')
        
        in_table = False
        table_buffer = []
        
        in_math_block = False
        math_buffer = []

        for line in lines:
            raw_line = line.strip()

            # --- 1. BLOCK MATH CẢNH GIỚI (Hiển thị phương trình Toán/Lý/Hóa đa dòng) ---
            if raw_line.startswith(r'\begin{') or raw_line == '$$':
                in_math_block = True
                math_buffer.append(raw_line)
                continue
            elif in_math_block:
                math_buffer.append(raw_line)
                if raw_line.startswith(r'\end{') or raw_line == '$$':
                    in_math_block = False
                    # Bỏ các thẻ $$ bao bọc nếu có để truyền chuỗi LaTeX sạch
                    clean_content = "\n".join(math_buffer).strip('$')
                    ast_nodes.append({
                        "type": "math_block", 
                        "content": clean_content
                    })
                    math_buffer = []
                continue

            # --- 2. BẢNG (TABLES) ---
            if raw_line.startswith('|') and raw_line.endswith('|'):
                in_table = True
                table_buffer.append(raw_line)
                continue
            elif in_table:
                table_node = cls._normalize_table(table_buffer)
                if table_node:
                    ast_nodes.append(table_node)
                in_table = False
                table_buffer = []

            # Bỏ qua các dòng trống hoàn toàn ngoài bảng và toán
            if not raw_line:
                continue

            # --- 3. TIÊU ĐỀ (HEADINGS) ---
            heading_match = re.match(r'^(#{1,6})\s+(.*)', raw_line)
            if heading_match:
                level = len(heading_match.group(1))
                content = heading_match.group(2)
                ast_nodes.append({
                    "type": "heading",
                    "level": level,
                    "tokens": cls._parse_inline_content(content)
                })
                continue

            # --- 4. HÌNH ẢNH (IMAGES) ---
            img_match = re.match(r'^!\[(.*?)\]\((.*?)\)', raw_line)
            if img_match:
                ast_nodes.append({
                    "type": "image",
                    "alt": img_match.group(1),
                    "url": img_match.group(2)
                })
                continue

            # --- 5. DANH SÁCH (LISTS) ---
            bullet_match = re.match(r'^([\*\-])\s+(.*)', raw_line)
            if bullet_match:
                ast_nodes.append({
                    "type": "list_item",
                    "style": "bullet",
                    "tokens": cls._parse_inline_content(bullet_match.group(2))
                })
                continue
                
            number_match = re.match(r'^(\d+\.)\s+(.*)', raw_line)
            if number_match:
                ast_nodes.append({
                    "type": "list_item",
                    "style": "number",
                    "tokens": cls._parse_inline_content(number_match.group(2))
                })
                continue

            # --- 6. ĐOẠN VĂN (PARAGRAPHS) ---
            ast_nodes.append({
                "type": "paragraph",
                "tokens": cls._parse_inline_content(raw_line)
            })

        # Chốt bảng nếu dữ liệu kết thúc mà bảng vẫn chưa đóng
        if in_table:
            table_node = cls._normalize_table(table_buffer)
            if table_node:
                ast_nodes.append(table_node)

        return ast_nodes
