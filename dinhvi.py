import pyautogui
import keyboard

def get_mouse_position():
    while True:
        if keyboard.is_pressed('a'):
            x, y = pyautogui.position()
            print(f'Vị trí chuộtaa: ({x}, {y})')
            break
def clicked(x,y):
    pyautogui.click(x,y)
if __name__ == "__main__":
    print("Nhấn phím 'a' để lấy vị trí chuột...")
    get_mouse_position()
    # clicked( 1361, 41aaaa2 )
