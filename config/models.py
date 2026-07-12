# =====================================================================
# FILE: config/models.py (HỆ THỐNG PHÂN PHỐI ĐA LUỒNG TOÀN DIỆN NĂM 2026)
# =====================================================================

# LUỒNG 1: Khai báo định danh các lõi mô hình thế hệ mới dựa trên bảng tài nguyên trống của thầy
CORE_LUONG_FLASH = "models/gemini-3.5-flash"        # Dung lượng trống 12/20 RPD
CORE_LUONG_LITE  = "models/gemini-3.1-flash-lite"   # Dung lượng cực đại trống 7/500 RPD
CORE_LUONG_PRO   = "models/gemini-3.5-flash"        # Ép dòng Pro phụ tải sang Flash để tránh lỗi 429

# LUỒNG 2: Bản đồ ánh xạ menu hiển thị giao diện sang mã API kỹ thuật
MODEL_MAPPING = {
    "3.1 Flash-Lite": CORE_LUONG_LITE,
    "3.5 Flash": CORE_LUONG_FLASH,
    "3.1 Pro": CORE_LUONG_PRO,
    "Tư duy mở rộng": CORE_LUONG_PRO
}

def get_fallback_queue(chosen_display_name, phan_he_mode="de_kt"):
    """
    LUỒNG ĐIỀU PHỐI THÔNG MINH (Fallback Router):
    Tự động tính toán hàng đợi dự phòng và phân tách dòng máy ưu tiên theo từng phân hệ sư phạm.
    """
    primary = MODEL_MAPPING.get(chosen_display_name, CORE_LUONG_FLASH)
    
    # Phân tách luồng nghiệp vụ dựa trên phân hệ làm việc
    if phan_he_mode == "khbd":
        # Ưu tiên Flash xử lý tài liệu đề cương dài, nhúng Năng lực số & AI nhanh
        base_queue = [primary, CORE_LUONG_FLASH, CORE_LUONG_LITE]
    else:
        # Ưu tiên Lite có 500 câu/ngày để giáo viên ra ma trận đặc tả toán học liên tục
        base_queue = [primary, CORE_LUONG_LITE, CORE_LUONG_FLASH]
        
    # Loại bỏ hoàn toàn các dòng máy 2.5 cũ đã bị cạn kiệt kịch trần 20/20 requests
    clean_queue = []
    for model in base_queue:
        if model not in clean_queue:
            clean_queue.append(model)
            
    return clean_queue
