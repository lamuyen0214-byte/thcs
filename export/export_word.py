"""
export_word.py
Khung WordExportEngine mẫu để thay thế và mở rộng.
"""

import io
import re
import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

class WordExportEngine:
    @staticmethod
    def clean_math_formulas(text: str) -> str:
        if not text:
            return ""
        text = text.replace("$","")
        text = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1/\2)', text)
        text = re.sub(r'\\sqrt\{([^}]+)\}', r'√(\1)', text)
        repl = {
            "\\alpha":"α","\\beta":"β","\\pi":"π","\\Delta":"Δ",
            "\\rightarrow":"→","\\leftrightarrow":"↔",
            "\\le":"≤","\\ge":"≥","\\approx":"≈",
            "\\sum":"∑","\\lim":"lim"
        }
        for k,v in repl.items():
            text=text.replace(k,v)
        return text.replace("\\","").strip()

    @staticmethod
    def _normal_style(doc):
        s=doc.styles["Normal"]
        s.font.name="Times New Roman"
        s.font.size=Pt(13)

    @staticmethod
    def build_matrix_table(doc, data):
        tbl=doc.add_table(rows=5, cols=11)
        tbl.style="Table Grid"
        headers=["STT","Chủ đề","Nội dung","NB","NB","TH","TH","VD","VD","VDC","Tổng"]
        for i,h in enumerate(headers):
            tbl.cell(0,i).text=h
        for c in [0,1,2,10]:
            tbl.cell(0,c).merge(tbl.cell(1,c))
        for c in (3,5,7):
            tbl.cell(0,c).merge(tbl.cell(0,c+1))
            tbl.cell(1,c).text="TN"
            tbl.cell(1,c+1).text="TL"
        tbl.cell(0,9).merge(tbl.cell(1,9))
        tbl.cell(0,9).text="VDC"
        rows=[
            ["1",data.get("custom_req","Chủ đề"),"Kiến thức","","","","","","","",""],
            ["2",data.get("custom_req","Chủ đề"),"Vận dụng","","","","","","","",""],
            ["","TỔNG","","","","","","","","","10 điểm"]
        ]
        for r,row in enumerate(rows,start=2):
            for c,val in enumerate(row):
                tbl.cell(r,c).text=str(val)

    @staticmethod
    def build_specification_table(doc,data):
        t=doc.add_table(rows=3,cols=5)
        t.style="Table Grid"
        hd=["STT","Chủ đề","Yêu cầu cần đạt","TN","TL"]
        for i,h in enumerate(hd):
            t.cell(0,i).text=h
        t.cell(1,0).text="1"
        t.cell(1,1).text=data.get("custom_req","Chủ đề")
        t.cell(1,2).text="Yêu cầu cần đạt do AI sinh."
        t.cell(2,0).text="2"
        t.cell(2,1).text="Tổng hợp"

    @staticmethod
    def export_to_word(data_cache):
        doc=docx.Document()
        WordExportEngine._normal_style(doc)
        sec=doc.sections[0]
        sec.top_margin=Inches(0.79)
        sec.bottom_margin=Inches(0.79)
        sec.left_margin=Inches(1.18)
        sec.right_margin=Inches(0.79)

        if data_cache.get("is_khbd"):
            p=doc.add_paragraph()
            p.alignment=WD_ALIGN_PARAGRAPH.CENTER
            r=p.add_run("KẾ HOẠCH BÀI DẠY")
            r.bold=True
        else:
            WordExportEngine.build_matrix_table(doc,data_cache)
            doc.add_paragraph()
            WordExportEngine.build_specification_table(doc,data_cache)
            doc.add_paragraph()

        txt=data_cache.get("ai_generated_content","")
        for line in txt.splitlines():
            if line.strip():
                doc.add_paragraph(WordExportEngine.clean_math_formulas(line))
        bio=io.BytesIO()
        doc.save(bio)
        bio.seek(0)
        return bio.getvalue()
