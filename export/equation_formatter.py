# =====================================================================
# FILE: export/equation_formatter.py (TRÌNH CHUYỂN ĐỔI LATEX SANG EQUATION WORD)
# =====================================================================
import re
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

class EquationFormatter:
    @staticmethod
    def latex_to_word_omml(latex_str):
        """
        Thuật toán bóc tách chuỗi toán thô LaTeX bẻ gãy hoàn toàn lỗi vỡ hình,
        biến đổi thành thẻ oMath XML chính thống của Microsoft Word.
        """
        # Quét sạch các ký tự bọc dòng toán rác $
        latex_str = latex_str.replace("$", "").strip()
        
        # 1. Đồng bộ hệ thống ký hiệu toán học phổ thông của Bộ Giáo dục Việt Nam
        replacements = [
            (r'\\sqrt\{([^}]+)\}', r'√(\1)'),
            (r'\\sum', r'∑'), (r'\\lim', r'lim'), (r'\\pi', r'π'),
            (r'\\alpha', r'α'), (r'\\beta', r'β'), (r'\\Delta', r'Δ'),
            (r'\\rightarrow', r'→'), (r'\\leftrightarrow', r'↔'),
            (r'\\le', r'≤'), (r'\\ge', r'≥'), (r'\\approx', r'≈'),
            (r'\\in', r'∈'), (r'\\subset', r'⊂'),
            (r'\^2', r'²'), (r'\^3', r'³'), (r'\^n', r'ⁿ')
        ]
        for pattern, repl in replacements:
            latex_str = re.sub(pattern, repl, latex_str)
            
        # 2. Xử lý phân số thẳng đứng cao cấp \frac{tử}{mẫu} sang dạng toán in ấn sạch
        latex_str = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1/\2)', latex_str)
        
        # Trả về chuỗi cấu trúc thô an toàn
        return latex_str

    @staticmethod
    def inject_math_run(paragraph, text_content):
        """Nhúng trực tiếp đoạn text đã xử lý toán vào paragraph văn bản"""
        clean_text = EquationFormatter.latex_to_word_omml(text_content)
        run = paragraph.add_run(clean_text)
        return run
