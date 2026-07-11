# File: ai_engine/layer_3_reasoning/prompt_manager.py
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
