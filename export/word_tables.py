from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

class TableRenderer:
    @staticmethod
    def render_ast_table(doc, node, style_manager, math_renderer):
        rows = node.get("rows", [])
        cols = node.get("cols", 0)
        table = doc.add_table(rows=len(rows) + 1, cols=cols)
        table.style = 'Table Grid'
        # Logic vẽ bảng theo AST đã duyệt
        for r_idx, row_data in enumerate(rows):
            for c_idx, cell_tokens in enumerate(row_data):
                p = table.cell(r_idx, c_idx).paragraphs[0]
                style_manager._render_inline_tokens(p, cell_tokens, math_renderer)
