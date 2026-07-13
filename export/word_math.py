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

class MathRenderer:
    @classmethod
    def render_inline_math(cls, paragraph, latex_str: str):
        # Đơn giản hóa: Chuyển đổi LaTeX cơ bản sang Unicode trước khi chèn vào Run
        clean_text = latex_str.replace(r'\frac{', '(').replace('}{', ')/(').replace('}', ')')
        run = paragraph.add_run(ScienceNormalizer.normalize(clean_text))
        run.font.name = 'Times New Roman'
