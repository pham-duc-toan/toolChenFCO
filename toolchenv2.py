import pyautogui
import cv2
import numpy as np
import keyboard
import time
from checkBox import main as checkBox
from chup import capture_and_save_screenshot as cap
from chup import chupmau
from isOffBox import main as checkOffBox
from datetime import datetime


def capture_region(x1gia, y1gia, x2gia, y2gia):
    width, height = x2gia - x1gia, y2gia - y1gia
    screenshot = pyautogui.screenshot(region=(x1gia, y1gia, width, height))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)  # Chuyển sang ảnh xám
    return screenshot

def compare_images(img1, img2, threshold=100, top_n=10):
    if img1.shape != img2.shape:
        print("Kích thước ảnh không khớp!")
        return False
    
    difference = cv2.absdiff(img1, img2)
    difference_smooth = cv2.GaussianBlur(difference, (5, 5), 0)
    
    flattened_diff = difference_smooth.flatten()
    top_diffs = np.sort(flattened_diff)[-top_n:]
    mean_top_diff = np.mean(top_diffs)
    if mean_top_diff >= threshold:
      print(f"Sai số trung bình của {top_n} pixel có sai lệch lớn nhất: {mean_top_diff:.2f}")
      
    return mean_top_diff < threshold

def main(stop_event):
    x1gia, y1gia = 1361, 412
    x2gia, y2gia = 1511, 442
    xmax, ymax = 1466, 435  
    xmua, ymua = 1266, 919  
    xOk, yOk = 1235, 802
    xCancel, yCancel = 1403, 803
    reference_image = cv2.imread('giacu.png', cv2.IMREAD_GRAYSCALE)
    
    if reference_image is None:
        print("Lỗi: Không thể đọc ảnh gia. Kiểm tra đường dẫn!")
        return
    
    print("Chương trình bắt đầu. Nhấn **Backspace** để dừng ngay lập tức.")
    
    while not stop_event.is_set():
        
        captured_image = capture_region(x1gia, y1gia, x2gia, y2gia)
        
        if compare_images(captured_image, reference_image):
            pyautogui.click(xCancel, yCancel)
            time.sleep(0.2)
            pyautogui.click(xmua, ymua)
            checkBox(stop_event)
        else:
            pyautogui.click(xmax, ymax)
            
            pyautogui.click(xOk, yOk)
            
            print(datetime.now())
            # doi load lai sau khi bam mua 
            checkOffBox()
            # luu ket qua 
            file_name = datetime.now().strftime("%Y%m%d_%H%M%S") + "res.png"
            

            # Gửi ảnh lên Telegram
            

            pyautogui.click(xmua, ymua)
            send_image_to_telegram(file_name)
            checkBox(stop_event)
            # # cap nhat gia cu
            cap(x1gia, y1gia, x2gia, y2gia, "giacu.png")
            
            


            reference_image = cv2.imread('giacu.png', cv2.IMREAD_GRAYSCALE)
    
            if reference_image is None:
                print("Lỗi: Không thể đọc ảnh gia. Kiểm tra đường dẫn!")
                return
            break

def send_image_to_telegram(image_path):
    from telebot import TeleBot

    # Khai báo bot Telegram
    TOKEN = "7169529565:AAF_VTyhriBeWLvRHd8G5J-fM9pZdCR8PSQ"
    CHAT_ID = "7345469514"
    bot = TeleBot(TOKEN)
    bot.send_message(CHAT_ID, "chèn V2 thành công !")
    with open(image_path, "rb") as photo:
        bot.send_photo(CHAT_ID, photo, caption="📸 Ảnh chụp màn hình mới nhất")



if __name__ == "__main__":
    main()
