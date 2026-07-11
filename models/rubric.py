# =====================================================================
# FILE: models/rubric.py (ĐỐI TƯỢNG QUẢN LÝ TIÊU CHÍ ĐÁNH GIÁ RUBRIC)
# =====================================================================

class Rubric:
    def __init__(self, ten_nhiem_vu, tieu_chi_list, muc_do_list, ai_matrix_content=""):
        """
        Khởi tạo cấu trúc bảng Rubric đánh giá năng lực/phẩm chất học sinh
        """
        self.ten_nhiem_vu = ten_nhiem_vu.strip()
        self.tieu_chi_list = tieu_chi_list if isinstance(tieu_chi_list, list) else []
        self.muc_do_list = muc_do_list if isinstance(muc_do_list, list) else ["Chưa đạt", "Đạt", "Khá", "Tốt"]
        self.ai_matrix_content = ai_matrix_content

    def to_dict(self):
        return {
            "ten_nhiem_vu": self.ten_nhiem_vu,
            "tieu_chi_list": self.tieu_chi_list,
            "muc_do_list": self.muc_do_list,
            "ai_matrix_content": self.ai_matrix_content
        }

    @classmethod
    def from_dict(cls, data):
        if not data: return None
        return cls(
            ten_nhiem_vu=data.get("ten_nhiem_vu", ""),
            tieu_chi_list=data.get("tieu_chi_list", []),
            muc_do_list=data.get("muc_do_list", []),
            ai_matrix_content=data.get("ai_matrix_content", "")
        )
