import re
from typing import List, Dict, Any

class MarkdownTokenizer:
    # Gom các Regex biên dịch trước (Compiled Regex) để tối ưu hiệu năng
    _HEADING_RE = re.compile(r'^(#{1,6})\s+(.*)')
    _IMAGE_RE = re.compile(r'^!\[(.*?)\]\((.*?)\)')
    _BULLET_RE = re.compile(r'^([\*\-])\s+(.*)')
    _NUMBER_RE = re.compile(r'^(\d+\.)\s+(.*)')
    _MATH_RE = re.compile(r'(\$.*?\$|\\\([^()]*\\\))')

    @classmethod
    def parse(cls, markdown_text: str) -> List[Dict[str, Any]]:
        # 1. BỘ LỌC RÁC TOÀN CỤC (Sử dụng tuple.startswith tối ưu hơn list)
        forbidden_prefixes = ("Chào bạn", "Với vai trò", "Tôi là", "Lưu ý về")
        lines = [
            line for line in markdown_text.splitlines() 
            if not line.lstrip().startswith(forbidden_prefixes)
        ]
        
        ast_nodes = []
        table_buffer = []

        # Hàm bổ trợ giúp giảm lặp code khi đẩy bảng vào AST
        def flush_table():
            if table_buffer:
                ast_nodes.append(cls._parse_table(table_buffer))
                table_buffer.clear()

        # 2. XỬ LÝ DÒNG VÀ GOM NHÓM BẢNG
        for raw_line in lines:
            line = raw_line.strip()
            
            if not line:
                flush_table()
                continue

            # Nhận diện hàng của bảng
            if line.startswith('|'):
                table_buffer.append(line)
                continue
            
            # Nếu dòng hiện tại không phải bảng, xuất buffer cũ (nếu có)
            flush_table()

            # 3. CÁC ĐỊNH DẠNG KHÁC (Áp dụng kỹ thuật Walrus Operator `:=` của Python 3.8+)
            if match := cls._HEADING_RE.match(line):
                ast_nodes.append({
                    "type": "heading", 
                    "level": len(match.group(1)), 
                    "tokens": cls._parse_inline_content(match.group(2))
                })
            elif match := cls._IMAGE_RE.match(line):
                ast_nodes.append({
                    "type": "image", 
                    "alt": match.group(1), 
                    "url": match.group(2)
                })
            elif match := cls._BULLET_RE.match(line):
                ast_nodes.append({
                    "type": "list_item", 
                    "style": "bullet", 
                    "tokens": cls._parse_inline_content(match.group(2))
                })
            elif match := cls._NUMBER_RE.match(line):
                ast_nodes.append({
                    "type": "list_item", 
                    "style": "number", 
                    "tokens": cls._parse_inline_content(match.group(2))
                })
            else:
                ast_nodes.append({
                    "type": "paragraph", 
                    "tokens": cls._parse_inline_content(line)
                })

        # Kết thúc vòng lặp, kiểm tra nếu còn sót bảng
        flush_table()
        return ast_nodes

    @staticmethod
    def _parse_table(lines: List[str]) -> Dict[str, Any]:
        """Chuyển đổi danh sách các dòng bảng thành cấu trúc dữ liệu chính xác"""
        rows = []
        headers = []
        
        for line in lines:
            # Sửa lỗi logic strip bỏ ô trống: Tách dấu '|' và bỏ phần tử rỗng ở đầu/cuối do Markdown Table sinh ra
            cells = [c.strip() for c in line.split('|')]
            if len(cells) > 1 and cells[0] == '': cells.pop(0)
            if len(cells) > 0 and cells[-1] == '': cells.pop()
            
            if not cells:
                continue

            # Nếu dòng chứa '---', bỏ qua (đây là dòng căn lề ngăn cách của bảng)
            if any(re.match(r'^:?---+:?$', c) for c in cells):
                continue

            if not headers:
                headers = [{"content": c} for c in cells]
            else:
                rows.append([{"content": c} for c in cells])
                
        return {"type": "table", "headers": headers, "rows": rows, "cols": len(headers)}

    @staticmethod
    def _parse_inline_content(text: str) -> List[Dict[str, str]]:
        tokens = []
        if not text:
            return tokens

        # Sử dụng Regex đã compiled sẵn bên trên
        parts = MarkdownTokenizer._MATH_RE.split(text)
        
        for part in parts:
            if not part:
                continue
                
            # Kiểm tra định dạng Inline Math
            if (part.startswith('$') and part.endswith('$')) or \
               (part.startswith(r'\(') and part.endswith(r'\)')):
                
                # Trích xuất phần nội dung toán thuần túy
                if part.startswith('$'):
                    clean_math = part.strip('$')
                else:
                    clean_math = part[2:-2] # Bỏ '\(' và '\)' nhanh hơn replace
                    
                tokens.append({"type": "inline_math", "content": clean_math})
            else:
                tokens.append({"type": "text", "content": part})
                
        return tokens
