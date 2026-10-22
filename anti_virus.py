# filename: stealth_utils.py
import os
import ctypes

def hide_file(filepath):
    """Đặt thuộc tính ẩn cho tệp tin (chỉ Windows)."""
    try:
        if os.name == 'nt': # Nếu là Windows
            # FILE_ATTRIBUTE_HIDDEN = 0x02
            # FILE_ATTRIBUTE_SYSTEM = 0x04
            # FILE_ATTRIBUTE_ARCHIVE = 0x20
            # Kết hợp các thuộc tính để tệp tin khó bị nhìn thấy hơn
            ctypes.windll.kernel32.SetFileAttributesW(filepath, 0x02 | 0x04 | 0x20)
            print(f"[*] Đã ẩn tệp tin: {filepath}")
    except Exception as e:
        print(f"[-] Lỗi khi ẩn tệp tin {filepath}: {e}")

if __name__ == "__main__":
    # Ví dụ sử dụng: ẩn chính file script này
    current_script = os.path.abspath(__file__)
    hide_file(current_script)
