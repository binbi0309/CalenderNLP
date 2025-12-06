import sys
import json
from nlp_engine import process_text

def main():
    """
    Hàm chính để nhận văn bản từ dòng lệnh và xử lý.
    """
    # Kiểm tra xem có đối số nào được truyền từ terminal không
    if len(sys.argv) > 1:
        # Nếu có, nối tất cả các đối số lại thành một câu hoàn chỉnh
        text = " ".join(sys.argv[1:])
    else:
        # Nếu không, yêu cầu người dùng nhập trực tiếp từ terminal
        text = input("Vui lòng nhập lịch: ")

    print(f"\nĐang xử lý câu: '{text}'")
    print("-" * 30)
    
    result = process_text(text)
    
    print("\n--- KẾT QUẢ TRÍCH XUẤT ---")
    print(json.dumps(result, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
