import pyautogui
import cv2
import numpy as np
import threading
import time
from checkBox import main as checkBox
from chupgiacu import capture_and_save_screenshot as cap
from datetime import datetime
from isOffBox import main as checkOffBox
from chupgiacu import chupmau
from playsound import playsound
from telebot import TeleBot
def capture_region(x1giacu, y1giacu, x2giacu, y2giacu):
    width, height = x2giacu - x1giacu, y2giacu - y1giacu
    screenshot = pyautogui.screenshot(region=(x1giacu, y1giacu, width, height))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)  # Chuyển sang ảnh xám
    return screenshot

def compare_images(img1, img2, threshold=100, top_n=10):
    if img1.shape != img2.shape:
        print("Kích thước ảnh không khớp!")
        return False
    
   
    # Tính sự khác biệt tuyệt đối giữa hai ảnh
    difference = cv2.absdiff(img1, img2)
    difference_smooth = cv2.GaussianBlur(difference, (5, 5), 0)
    # Chuyển ma trận sai số thành danh sách 1D và sắp xếp theo thứ tự giảm dần
    flattened_diff = difference_smooth.flatten()
    top_diffs = np.sort(flattened_diff)[-top_n:]  # Lấy top 20 giá trị sai số lớn nhất

    # Tính trung bình của 20 pixel có sai số lớn nhất
    mean_top_diff = np.mean(top_diffs)

    

    # So sánh với threshold
    return mean_top_diff < threshold

# Khai báo bot Telegram
TOKEN = "7169529565:AAF_VTyhriBeWLvRHd8G5J-fM9pZdCR8PSQ"
CHAT_ID = "7345469514"
bot = TeleBot(TOKEN)
running_v1 = False  # Biến kiểm soát vòng lặp
v1_thread = None  # Luồng chạy v1
def main(stop_event,i=0 ):
    listloc = [(1460, 278),(1456, 339),(1452, 394),(1447, 449),(1461, 514),(1444, 562),(1441, 630),(1438, 678),(1458, 743),(1440, 796),(1443, 860)]
    x1giacu, y1giacu = 1361, 412
    x2giacu, y2giacu = 1511, 442
    xmaxgia, ymaxgia = 1466, 435  
    xmingia,ymingia=1473, 443
    if i>= len(listloc):
        bot.send_message(CHAT_ID, "i không hợp lệ!")
        return 
    xRe, yRe = listloc[i]
    
    xOk, yOk = 1246, 799
    xCancel, yCancel = 1414, 807
    reference_image = cv2.imread('giacu.png', cv2.IMREAD_GRAYSCALE)

    if reference_image is None:
        print("Lỗi: Không thể đọc ảnh gia. Kiểm tra đường dẫn!")
        return
    
    

    while not stop_event.is_set():
    
        
        captured_image = capture_region(x1giacu, y1giacu, x2giacu, y2giacu)

        if compare_images(captured_image, reference_image):
            pyautogui.click(xCancel, yCancel)
            pyautogui.moveTo(xRe, yRe)
            pyautogui.sleep(0.2)
            pyautogui.click(xRe, yRe)
            checkBox(stop_event,xRe, yRe)
        else:
            pyautogui.click(xmingia, ymingia)
            pyautogui.click(xOk, yOk)

            print(datetime.now())

            checkOffBox()
            pyautogui.click(1735, 572)
            pyautogui.moveTo(xRe, yRe)
            pyautogui.sleep(0.2)
            pyautogui.click(xRe, yRe)
            checkBox(stop_event,xRe, yRe)

            # Chụp ảnh màn hình và lưu file
            file_name = datetime.now().strftime("%Y%m%d_%H%M%S") + "res.png"
            
            chupmau(0,0,1917, 1028,filename=file_name)
            # Gửi ảnh qua Telegram
            send_image_telegram(file_name)

            cap(x1giacu, y1giacu, x2giacu, y2giacu, "giacu.png")
            reference_image = cv2.imread('giacu.png', cv2.IMREAD_GRAYSCALE)

            if reference_image is None:
                print("Lỗi: Không thể đọc ảnh gia. Kiểm tra đường dẫn!")
                return

            # playsound("noti.mp3")
            # break
# Hàm gửi ảnh qua Telegram
def send_image_telegram(image_path):
    try:
        bot.send_message(CHAT_ID, "chèn V1 thành công !")
        with open(image_path, "rb") as photo:
            bot.send_photo(CHAT_ID, photo)
        print("✅ Đã gửi ảnh chụp màn hình qua Telegram!")
    except Exception as e:
        print(f"❌ Lỗi khi gửi ảnh: {e}")
if __name__ == "__main__":
    main()


# C:\Users\LENOVO\AppData\Local\Programs\Python\Python312\python.exe C:\tool\toolchenv1.py