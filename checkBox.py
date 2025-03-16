import pyautogui
import cv2
import numpy as np
import time

def capture_region(x1, y1, x2, y2):
    width, height = x2 - x1, y2 - y1
    screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    return screenshot

def compare_images(img1, img2, threshold=10):
    if img1.shape != img2.shape:
        return False
    difference = cv2.absdiff(img1, img2)
    return np.mean(difference) < threshold  # Cho phép sai số nhỏ


def main(stop_event,xmua=1266,ymua =  919):
    from telebot import TeleBot

    # Khai báo bot Telegram
    TOKEN = "7169529565:AAF_VTyhriBeWLvRHd8G5J-fM9pZdCR8PSQ"
    CHAT_ID = "7345469514"
    bot = TeleBot(TOKEN)
    x1, y1 = 1186, 786
    x2, y2 = 1230, 816
     
    reference_image = cv2.imread('checkBox.png', cv2.IMREAD_GRAYSCALE)
    start_time = time.time()
    if reference_image is None:
        print("Lỗi: Không thể đọc ảnh checkBox.png. Kiểm tra đường dẫn!")
        return
    while not stop_event.is_set():
        captured_image = capture_region(x1, y1, x2, y2)
        if compare_images(captured_image, reference_image):
            break
        if time.time() - start_time >= 30:
            
            bot.send_message(CHAT_ID, "⚠️ Đang kiểm tra captcha!")

            screenshot_path = "screenshot.png"
            pyautogui.screenshot(screenshot_path)
            with open(screenshot_path, "rb") as photo:
                bot.send_photo(CHAT_ID, photo, caption="📸 Ảnh chụp màn hình mới nhất")

            capcha = capture_region(731, 483,1172, 523 )
            if compare_images(capcha,cv2.imread('capcha.png',cv2.IMREAD_GRAYSCALE)):
                
                pyautogui.click(1118, 613)
                time.sleep(1)
                
                pyautogui.click(xmua, ymua)
            else:
                capcha2=capture_region(1011, 609,1185, 637 )
                if compare_images(capcha2,cv2.imread('capcha2.png',cv2.IMREAD_GRAYSCALE)):
                # click xac nhan
                    pyautogui.click(1107, 635)
                    time.sleep(1)
                    
                    pyautogui.click(xmua, ymua)
                elif compare_images(capture_region(736, 440, 1123, 526  ),cv2.imread('capcha3.png',cv2.IMREAD_GRAYSCALE)):
                 # click xac nhan
                    pyautogui.click(1094, 629)
                    time.sleep(1)
                   
                    pyautogui.click(xmua, ymua)
                else:
                    pyautogui.moveTo(188, 697)
                    time.sleep(1)
                    pyautogui.moveTo(xmua, ymua)
                    time.sleep(1)
                    pyautogui.click(xmua, ymua)
            start_time = time.time() 
        
    
  

if __name__ == "__main__":
    main()