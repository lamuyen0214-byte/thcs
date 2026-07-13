import sys
import os

# 1. Tự động lùi thư mục tìm về đúng thư mục gốc chứa ai_config.py
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = current_dir
while not os.path.exists(os.path.join(root_dir, 'ai_config.py')) and root_dir != os.path.dirname(root_dir):
    root_dir = os.path.dirname(root_dir)

if root_dir not in sys.path:
    sys.path.append(root_dir)

# 2. Hút dữ liệu trực tiếp từ "Trái tim" trung tâm
try:
    from ai_config import get_ai_client
except ImportError:
    get_ai_client = lambda: None

# 3. Tạo các biến giả lập để đánh lừa các module cũ đang import
gemini_instance = get_ai_client()

def get_model():
    return get_ai_client()
