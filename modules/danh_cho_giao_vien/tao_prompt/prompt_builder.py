import streamlit as st
import os
import sys

# =====================================================================
# 1. ĐỊNH VỊ ĐƯỜNG DẪN GỐC TỰ ĐỘNG TÌM AI_ENGINE (ƯU TIÊN TUYỆT ĐỐI)
# =====================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = current_dir
# Quét ngược lên các thư mục cha cho đến khi thấy lõi 'ai_engine'
while not os.path.exists(os.path.join(root_dir, 'ai_engine')) and root_dir != os.path.dirname(root_dir):
    root_dir = os.path.dirname(root_dir)

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Đảm bảo hệ thống tìm thấy thư mục export
export_path = os.path.abspath(os.path.join(root_dir, 'export'))
if export_path not in sys.path:
    sys.path.append(export_path)

# =====================================================================
# 2. NẠP ĐỘNG CƠ TỪ KIẾN TRÚC MỚI
# =====================================================================
from ai_engine.ai_config import get_api_key
from ai_engine.ai_runner import run_ai_with_fallback

def get_word_engine():
    try:
        from export.export_word import WordExportEngine
        return WordExportEngine
    except Exception as e:
        print(f"Lỗi nạp module Word: {e}")
        return None

def render_prompt_module():
    st.markdown("""
        <style>
        .header-blue {color: #0000FF; font-weight: bold; font-size: 15px; text-align: left; margin-bottom: 2px;}
        .box-prompt {background-color: #D0E8F2; padding: 15px; border-radius: 8px; border-left: 5px solid #5C9EAD; margin-bottom: 15px;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="box-prompt">💡 <b>Kỹ sư Prompt:</b> Công cụ giúp Giáo viên cấu trúc hóa các ý tưởng thành "Siêu câu lệnh" chuẩn mực, tối ưu hóa sức mạnh của AI trong công việc.</div>', unsafe_allow_html=True)

    # 1. KHUNG NHẬP LIỆU Ý TƯỞNG
    st.markdown('<p class="header-blue">Thầy/Cô muốn AI làm gì? (Nhập ý tưởng thô):</p>', unsafe_allow_html=True)
    y_tuong_tho = st.text_area(
        "Ý tưởng", 
        placeholder="Ví dụ: Tôi muốn AI viết một bài giới thiệu về ngày hội STEM của trường cấp 2, nghe thật hào hứng để đăng lên Fanpage...", 
        height=100, label_visibility="collapsed"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="header-blue">Đóng vai (Role):</p>', unsafe_allow_html=True)
        vai_tro = st.selectbox("Vai trò", ["Chuyên gia Giáo dục", "Nhà sáng tạo nội dung", "Giáo viên Tâm lý", "Kỹ sư Công nghệ", "Tùy chọn khác"], label_visibility="collapsed")
    with col2:
        st.markdown('<p class="header-blue">Định dạng đầu ra (Format):</p>', unsafe_allow_html=True)
        dinh_dang = st.selectbox("Định dạng", ["Bài viết mạng xã hội", "Văn bản trang trọng (Word)", "Bảng biểu (Markdown)", "Kịch bản (Script)"], label_visibility="collapsed")

    # 2. XỬ LÝ AI - TỐI ƯU PROMPT
    if st.button("🚀 TỐI ƯU HÓA SIÊU CÂU LỆNH (PROMPT)", type="primary", use_container_width=True):
        if not y_tuong_tho.strip():
            st.warning("⚠️ Thầy/Cô vui lòng nhập ý tưởng thô trước khi tối ưu hóa.")
            st.stop()

        # =====================================================================
        # BỘ ĐIỀU KHIỂN TRUNG TÂM (AI ENGINE)
        # =====================================================================
        api_key = get_api_key()
        
        if not api_key:
            st.error("⚠️ Lỗi cấu hình: Vui lòng nhập Gemini API Key ở thanh bên (Sidebar) trước!")
            st.stop()

        with st.spinner("🤖 Hệ thống đang phân tích và tái cấu trúc câu lệnh..."):
            prompt_he_thong = f"""
Bạn là một Chuyên gia Kỹ sư Prompt (Prompt Engineer) hàng đầu. Nhiệm vụ của bạn là nâng cấp ý tưởng thô của người dùng thành một "Siêu câu lệnh" (Meta-prompt) cực kỳ chi tiết, chuyên nghiệp và hiệu quả để họ có thể copy và dùng cho các AI khác (như ChatGPT, Gemini, Claude).

Thông tin đầu vào từ người dùng:
- Ý tưởng cốt lõi: {y_tuong_tho}
- Vai trò AI cần đóng vai: {vai_tro}
- Định dạng mong muốn: {dinh_dang}

Hãy xuất ra cấu trúc như sau (Sử dụng Markdown rõ ràng):
1. **Đánh giá ý tưởng:** Nhận xét ngắn gọn 2 dòng về mục tiêu của người dùng.
2. **SIÊU CÂU LỆNH ĐÃ TỐI ƯU:** Cung cấp câu lệnh hoàn chỉnh. Hãy đóng khung câu lệnh này trong một khối code (code block) để người dùng dễ dàng bấm nút COPY. Câu lệnh này phải bao gồm các yếu tố: 
   - [Vai trò]
   - [Bối cảnh cụ thể]
   - [Nhiệm vụ chi tiết]
   - [Giọng văn/Phong cách]
   - [Cấu trúc đầu ra mong muốn].
3. **Mẹo sử dụng:** Đưa ra 1-2 mẹo nhỏ để người dùng điền thêm biến số nếu cần.
"""
            
            # Gọi API thông qua kiến trúc chuẩn
            result = run_ai_with_fallback(
                prompt=prompt_he_thong,
                api_key=api_key,
                model_mode="flash"
            )
            
            if result.get("success"):
                st.session_state['current_prompt_data'] = {
                    "is_khbd": True, # Giữ cờ này để xuất Word ổn định
                    "title": "Công cụ Tối ưu Prompt",
                    "subject": "Kỹ năng AI",
                    "grade": "Giáo viên",
                    "ten_bai_save": "Sieu_Cau_Lenh_AI",
                    "ai_generated_content": result.get("text")
                }
                st.success(f"✅ Đã chế tạo thành công Siêu câu lệnh trong {result.get('time'):.2f} giây!")
                st.rerun()
            else:
                st.error("❌ Lỗi máy chủ AI: Máy chủ từ chối phản hồi.")
                with st.expander("🔍 Chi tiết lỗi kỹ thuật ngầm", expanded=True):
                    st.code(result.get("error"))

    # 3. KẾT XUẤT WORD
    st.markdown("---")
    prompt_cache = st.session_state.get('current_prompt_data')
    if prompt_cache:
        with st.expander("🔍 Xem trước Siêu câu lệnh", expanded=True):
            st.markdown(prompt_cache["ai_generated_content"])
            
        WordEngine = get_word_engine()
        word_file = None
        if WordEngine:
            try:
                word_file = WordEngine.export_to_word(prompt_cache)
            except Exception as e:
                st.error(f"⚠️ Lỗi xuất Word: {e}")

        col_dl, col_del = st.columns(2)
        with col_dl:
            if word_file:
                st.download_button(
                    label="📄 Tải Prompt (Word)", 
                    data=word_file, 
                    file_name="Sieu_Cau_Lenh_AI.docx", 
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            else:
                st.button("📄 Tải Prompt (Đang xử lý)", disabled=True, use_container_width=True)
                
        with col_del:
            if st.button("❌ Xóa bản nháp", use_container_width=True):
                del st.session_state['current_prompt_data']
                st.rerun()
