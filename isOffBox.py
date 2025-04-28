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


def main( ):
    x1, y1 = 1096, 594
    x2, y2 = 1215, 631
     
    reference_image = cv2.imread('onBox.png', cv2.IMREAD_GRAYSCALE)
    
    if reference_image is None:
        print("Lỗi: Không thể đọc ảnh checkBox.png. Kiểm tra đường dẫn!")
        return
    while True:
        
        captured_image = capture_region(x1, y1, x2, y2)
        if not compare_images(captured_image, reference_image):
            break
        
        
    
  

if __name__ == "__main__":
    
    main()
    