"""
Module: export/export_word.py
Mô tả: Động cơ điều phối chính (Facade) tích hợp Markdown Parser.
"""
import io
import docx
from docx.shared import Pt, Inches

class WordExportEngine:
    @classmethod
    def export_to_word(cls, data_cache) -> bytes:
        doc = docx.Document()
        
        # Cấu hình lề trang A4 chuẩn GDPT
        for section in doc.sections:
            section.top_margin = Inches(0.79)
            section.bottom_margin = Inches(0.79)
            section.left_margin = Inches(1.18)
            section.right_margin = Inches(0.79)
            
        doc.styles['Normal'].font.name = 'Times New Roman'
        doc.styles['Normal'].font.size = Pt(13)

        # Import bộ phiên dịch Markdown an toàn
        try:
            from .word_markdown import MarkdownParser
        except ImportError:
            doc.add_paragraph("⚠️ Thiếu file word_markdown.py trong thư mục export/")
            bio = io.BytesIO()
            doc.save(bio)
            bio.seek(0)
            return bio.getvalue()

        # Dữ liệu AI sinh ra
        ai_text = data_cache.get("ai_generated_content", "")
        
        # Giao toàn bộ việc vẽ vời cho Markdown Parser
        MarkdownParser.parse(doc, ai_text)

        # Trả file về trình duyệt
        bio = io.BytesIO()
        doc.save(bio)
        bio.seek(0)
        return bio.getvalue()
