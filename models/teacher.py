# =====================================================================
# FILE: models/teacher.py (ĐỐI TƯỢNG HỒ SƠ QUẢN LÝ GIÁO VIÊN)
# =====================================================================

class Teacher:
    def __init__(self, token_id, ho_ten, mon_giang_day, api_key_ca_nhan=""):
        """
        Khởi tạo đối tượng quản lý tài khoản hồ sơ giáo viên cốt cán
        """
        self.token_id = token_id.strip()
        self.ho_ten = ho_ten.strip()
        self.mon_giang_day = mon_giang_day if isinstance(mon_giang_day, list) else [mon_giang_day]
        self.api_key_ca_nhan = api_key_ca_nhan.strip()

    def to_dict(self):
        return {
            "token_id": self.token_id,
            "ho_ten": self.ho_ten,
            "mon_giang_day": self.mon_giang_day,
            "api_key_ca_nhan": self.api_key_ca_nhan
        }

    @classmethod
    def from_dict(cls, data):
        if not data: return None
        return cls(
            token_id=data.get("token_id", "GV001"),
            ho_ten=data.get("ho_ten", "Giáo viên"),
            mon_giang_day=data.get("mon_giang_day", ["Khoa học Tự nhiên"]),
            api_key_ca_nhan=data.get("api_key_ca_nhan", "")
        )
