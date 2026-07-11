# =====================================================================
# FILE: models/lesson.py (ĐỐI TƯỢNG QUẢN LÝ DỮ LIỆU KẾ HOẠCH BÀI DẠY)
# =====================================================================

class Lesson:
    def __init__(self, ten_bai, mon_hoc, lop, thoi_luong, noi_dung_tich_hop, ai_content=""):
        """
        Khởi tạo cấu trúc lưu trữ thông số một giáo án / KHBD chuẩn 5512
        """
        self.ten_bai = ten_bai.strip()
        self.mon_hoc = mon_hoc.strip()
        self.lop = str(lop).strip()
        self.thoi_luong = str(thoi_luong).strip()
        
        # Đảm bảo nội dung tích hợp luôn là dạng mảng danh sách (List)
        self.noi_dung_tich_hop = noi_dung_tich_hop if isinstance(noi_dung_tich_hop, list) else []
        
        # Văn bản chi tiết tiến trình 4 hoạt động do AI soạn giảng thực tế
        self.ai_content = ai_content

    def to_dict(self):
        return {
            "ten_bai": self.ten_bai,
            "mon_hoc": self.mon_hoc,
            "lop": self.lop,
            "thoi_luong": self.thoi_luong,
            "noi_dung_tich_hop": self.noi_dung_tich_hop,
            "ai_content": self.ai_content
        }

    @classmethod
    def from_dict(cls, data):
        if not data: return None
        return cls(
            ten_bai=data.get("ten_bai", ""),
            mon_hoc=data.get("mon_hoc", "Khoa học Tự nhiên"),
            lop=data.get("lop", "7"),
            thoi_luong=data.get("thoi_luong", "1"),
            noi_dung_tich_hop=data.get("noi_dung_tich_hop", []),
            ai_content=data.get("ai_content", "")
        )
