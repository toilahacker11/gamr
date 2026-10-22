import hello
import game
import anti_virus
import anti_data_wiping_module
import toi_yeu_ban

print("=== TỔNG HỢP CÁC CHƯƠNG TRÌNH ===")
print("1. Chạy Hello")
print("2. Chạy Game")
print("3. Chạy Anti-Virus")
print("4. Chạy Anti Data Wiping Module")
print("5. Chạy Tôi Yêu Bạn")

choice = input("Nhập lựa chọn của bạn (1-5): ")

if choice == "1":
    hello.main()
elif choice == "2":
    game.main()
elif choice == "3":
    anti_virus.main()
elif choice == "4":
    anti_data_wiping_module.main()
elif choice == "5":
    toi_yeu_ban.main()
else:
    print("Lựa chọn không hợp lệ!")

