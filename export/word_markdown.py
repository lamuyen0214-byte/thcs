import re
from typing import List, Dict, Any

class MarkdownTokenizer:
    _HEADING_RE = re.compile(r'^(#{1,6})\s+(.*)')
    _IMAGE_RE = re.compile(r'^!\[(.*?)\]\((.*?)\)')
    _BULLET_RE = re.compile(r'^([\*\-])\s+(.*)')
    _NUMBER_RE = re.compile(r'^(\d+\.)\s+(.*)')
    _MATH_RE = re.compile(r'(\$.*?\$|\\\([^()]*\\\))')

    @classmethod
    def parse(cls, markdown_text: str) -> List[Dict[str, Any]]:
        if not isinstance(markdown_text, str):
            return []

        forbidden_prefixes = ("Chào bạn", "Với vai trò", "Tôi là", "Lưu ý về")
        lines = [
            line for line in markdown_text.splitlines() 
            if not line.lstrip().startswith(forbidden_prefixes)
        ]
        
        ast_nodes = []
        table_buffer = []

        def flush_table():
            if table_buffer:
                ast_nodes.append(cls._parse_table(table_buffer))
                table_buffer.clear()

        for raw_line in lines:
            line = raw_line.strip()
            
            if not line:
                flush_table()
                continue

            if line.startswith('|'):
                table_buffer.append(line)
                continue
            
            flush_table()

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

        flush_table()
        return ast_nodes

    @staticmethod
    def _parse_table(lines: List[str]) -> Dict[str, Any]:
        """Cấu trúc lại Table về dạng sơ khai nhất để khớp hoàn toàn với bộ render LaTeX cũ"""
        rows = []
        headers = []
        
        for line in lines:
            raw_cells = [c.strip() for c in line.split('|')]
            
            # SỬA LỖI LOGIC: Cắt bỏ cột rỗng ở đầu/cuối do dấu gạch đứng '|' sinh ra
            if raw_cells and raw_cells[0] == '':
                raw_cells.pop(0)
            if raw_cells and raw_cells[-1] == '':
                raw_cells.pop()
                
            if not raw_cells:
                continue

            # Bỏ qua dòng gạch ngang phân cách tiêu đề (---)
            if any(re.match(r'^:?---+:?$', c) for c in raw_cells):
                continue

            # TRẢ VỀ CHUỖI THUẦN: Tránh lồng mảng/dict sâu khiến bộ render crash
            processed_cells = [{"content": c} for c in raw_cells]

            if not headers:
                headers = processed_cells
            else:
                rows.append(processed_cells)
                
        return {
            "type": "table", 
            "headers": headers, 
            "rows": rows, 
            "cols": len(headers) if headers else 0
        }

    @staticmethod
    def _parse_inline_content(text: str) -> List[Dict[str, str]]:
        tokens = []
        if not text:
            return tokens

        parts = MarkdownTokenizer._MATH_RE.split(text)
        
        for part in parts:
            if not part:
                continue
                
            if (part.startswith('$') and part.endswith('$')) or \
               (part.startswith(r'\(') and part.endswith(r'\)')):
                
                if part.startswith('$'):
                    clean_math = part.strip('$')
                else:
                    clean_math = part[2:-2]
                    
                tokens.append({"type": "inline_math", "content": clean_math})
            else:
                tokens.append({"type": "text", "content": part})
                
        return tokens
