import re
from docx.oxml import parse_xml
from docx.shared import RGBColor

class ScienceNormalizer:
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    SUP = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")
    
    @classmethod
    def normalize(cls, text: str) -> str:
        # Hóa học: H2SO4 -> H₂SO₄, Fe3+ -> Fe³⁺
        text = re.sub(r'([A-Za-z]+\d*)\^(\d*[+\-])', lambda m: m.group(1).translate(cls.SUB) + m.group(2).translate(cls.SUP), text)
        text = re.sub(r'([A-Z][a-z]?|\))(\d+)', lambda m: m.group(1) + m.group(2).translate(cls.SUB), text)
        return text
# Bổ sung vào class ScienceNormalizer
    TRANSLATION_MAP = {
        r'\perp': '⊥',
        r'\circ': '°',
        r'\widehat{A}': 'Â', # Tạm thời xử lý ký tự đơn giản
        r'\text{cm}': 'cm'
    }
    
    # Cập nhật trong hàm normalize:
    for latex, unicode_char in cls.TRANSLATION_MAP.items():
        text = text.replace(latex, unicode_char)
class MathRenderer:
    @classmethod
    def render_inline_math(cls, paragraph, latex_str: str):
        clean_text = latex_str.replace(
            r'\frac{', '('
        ).replace('}{', ')/(').replace('}', ')')

        run = paragraph.add_run(
            ScienceNormalizer.normalize(clean_text)
        )
        run.font.name = 'Times New Roman'

    @classmethod
    def render_display_math(cls, doc, node):
        p = doc.add_paragraph()
        p.alignment = 1

        latex_content = node.get("content", "")

        run = p.add_run(latex_content)
        run.font.name = 'Times New Roman'
        run.font.italic = True
