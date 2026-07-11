import os

class PromptManager:
    @staticmethod
    def get_stem_prompt(chu_de, mon_hoc, lop, yeu_cau_dac_biet):
        """
        Hàm tạo prompt chuẩn cho việc thiết kế bài dạy STEM
        """
        system_instruction = "Bạn là một chuyên gia giáo dục STEM và sư phạm môn Khoa học Tự nhiên cấp THCS. Bạn có chuyên môn sâu về việc xây dựng các dự án học tập gắn liền với thực tiễn."
        
        prompt = f"""
        Hãy thiết kế một kế hoạch bài dạy STEM chi tiết cho:
        - Chủ đề dự án: {chu_de}
        - Môn học chủ đạo: {mon_hoc}
        - Đối tượng: Học sinh lớp {lop}
        - Yêu cầu bổ sung: {yeu_cau_dac_biet}
        
        Cấu trúc bài dạy cần tuân thủ tiêu chuẩn 5 hoạt động (Gắn kết, Khám phá, Giải thích, Áp dụng, Đánh giá).
        Hãy trình bày rõ ràng, sử dụng định dạng Markdown, phân chia các phần mạch lạc.
        """
        return system_instruction, prompt

    @staticmethod
    def get_khbd_prompt(ten_bai, mon_hoc, lop, thoi_luong, noi_dung_tich_hop):
        """
        Hàm tạo prompt chuẩn cho việc xây dựng Kế hoạch bài dạy (Công văn 5512)
        """
        system_instruction = "Bạn là một giáo viên cốt cán môn Khoa học Tự nhiên cấp THCS, có nhiều kinh nghiệm soạn giảng theo định hướng phát triển năng lực và yêu cầu của Công văn 5512."
        
        # Xử lý chuỗi tích hợp an toàn
        tich_hop_str = ", ".join(noi_dung_tich_hop) if noi_dung_tich_hop else "Không có"
        
        # Tránh ảo giác toán học F-string bằng cách bọc chuỗi văn bản thuần cho LaTeX
        prompt = f"""
        Hãy soạn một Kế hoạch bài dạy (Giáo án) chi tiết theo chuẩn Công văn 5512 cho:
        - Tên bài học: {ten_bai}
        - Môn học: {mon_hoc}
        - Khối lớp: {lop}
        - Thời lượng: {thoi_luong} tiết
        - Nội dung cần tích hợp vào bài: {tich_hop_str}
        
        Yêu cầu cấu trúc:
        I. Mục tiêu (Năng lực, Phẩm chất)
        II. Thiết bị dạy học và học liệu
        III. Tiến trình dạy học (Gồm 4 hoạt động: Khởi động, Hình thành kiến thức mới, Luyện tập, Vận dụng)
        
        Lưu ý: Chú trọng đặc biệt vào phần nội dung tích hợp. Sử dụng định dạng Markdown rõ ràng. Đối với các công thức hóa học hoặc vật lý, hãy sử dụng định dạng chuẩn LaTeX (ví dụ: $H_2O$, $v = s/t$).
        """
        return system_instruction, prompt
