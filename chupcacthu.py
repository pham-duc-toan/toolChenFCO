import pyautogui
import cv2
import numpy as np

def capture_and_save_screenshot(x1, y1, x2, y2, filename):
    width, height = x2 - x1, y2 - y1
    screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)  # Chuyển ảnh sang grayscale
    cv2.imwrite(filename, screenshot)  # Lưu ảnh dưới dạng grayscale
    print(f"Ảnh đã được lưu vào {filename}")

if __name__ == "__main__":
    x1, y1 = 1165, 787
    x2, y2 = 1266, 812
    filename = "checkBox.png"
    capture_and_save_screenshot(x1, y1, x2, y2, filename)