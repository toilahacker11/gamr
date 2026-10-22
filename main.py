import hello
import game
import anti_virus
# Thêm các module khác nếu bạn muốn gọi chúng

print("=== CHƯƠNG TRÌNH TỔNG HỢP ===")
print("1. Chạy Hello")
print("2. Chạy Game")
print("3. Chạy Anti-Virus")

choice = input("Chọn chức năng: ")
if choice == "1":
    hello.main()
elif choice == "2":
    game.main()
elif choice == "3":
    anti_virus.main()

