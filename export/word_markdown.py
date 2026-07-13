import re
from typing import List, Dict, Any

class MarkdownTokenizer:
    @staticmethod
    def _parse_inline_content(text: str) -> List[Dict[str, str]]:
        tokens = []
        if not text:
            return tokens

        # Sửa lỗi: Đảm bảo mọi pattern đều là raw string r'...'
        math_pattern = r'(\$.*?\$|\\\([^()]*\\\))'
        parts = re.split(math_pattern, text)

        for part in parts:
            if not part:
                continue
            
            # Kiểm tra toán học với regex an toàn
            if (part.startswith('$') and part.endswith('$')) or \
               (part.startswith(r'\(') and part.endswith(r'\)')):
                clean_math = part.strip('$').replace(r'\(', '').replace(r'\)', '')
                tokens.append({"type": "inline_math", "content": clean_math})
            else:
                tokens.append({"type": "text", "content": part})
        return tokens

    @classmethod
    def parse(cls, markdown_text: str) -> List[Dict[str, Any]]:
        ast_nodes = []
        lines = markdown_text.split('\n')
        
        for line in lines:
            raw_line = line.strip()
            if not raw_line:
                continue

            # Các regex đã được ép kiểu r'...' để tránh lỗi bad escape
            if re.match(r'^(#{1,6})\s+(.*)', raw_line):
                match = re.match(r'^(#{1,6})\s+(.*)', raw_line)
                ast_nodes.append({"type": "heading", "level": len(match.group(1)), "tokens": cls._parse_inline_content(match.group(2))})
            
            elif re.match(r'^!\[(.*?)\]\((.*?)\)', raw_line):
                match = re.match(r'^!\[(.*?)\]\((.*?)\)', raw_line)
                ast_nodes.append({"type": "image", "alt": match.group(1), "url": match.group(2)})
            
            elif re.match(r'^([\*\-])\s+(.*)', raw_line):
                match = re.match(r'^([\*\-])\s+(.*)', raw_line)
                ast_nodes.append({"type": "list_item", "style": "bullet", "tokens": cls._parse_inline_content(match.group(2))})

            elif re.match(r'^(\d+\.)\s+(.*)', raw_line):
                match = re.match(r'^(\d+\.)\s+(.*)', raw_line)
                ast_nodes.append({"type": "list_item", "style": "number", "tokens": cls._parse_inline_content(match.group(2))})
                
            else:
                ast_nodes.append({"type": "paragraph", "tokens": cls._parse_inline_content(raw_line)})

        return ast_nodes
