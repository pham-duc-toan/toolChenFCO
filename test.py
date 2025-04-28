import telebot
import pyautogui
import threading
import time
BOT_TOKEN = "7169529565:AAF_VTyhriBeWLvRHd8G5J-fM9pZdCR8PSQ"
bot = telebot.TeleBot(BOT_TOKEN)
from chupgiacu import capture_and_save_screenshot as chup
from toolchenv1 import main as abc
from toolchenv2 import main as xyz
listloc = [(1460, 278),(1456, 339),(1452, 394),(1447, 449),(1461, 514),(1444, 562),(1441, 630),(1438, 678),(1458, 743),(1440, 796),(1443, 860)]
# Tạo danh sách tọa độ động
LOCATION_LIST = {
    "button hủy": (1403, 803),
    "button reV2" : (1266, 919 ), 
    "button cancel capcha":(1118, 613),
}
# Thêm các button re_i vào danh sách
for i, coords in enumerate(listloc, start=1):
    LOCATION_LIST[f"button reV1_{i}"] = coords

@bot.message_handler(func=lambda message: message.text.lower().startswith("press "))
def handle_press(message):
    """Xử lý lệnh press <tên button>"""
    try:
        _, button_name = message.text.split(" ", 1)  # Tách lấy tên button
        click_button(button_name, message)
    except ValueError:
        bot.reply_to(message, "⚠️ Lệnh không đúng. Dùng: press [tên button]")

def click_button(button_name, message=None):
    """Hàm click vào button theo tên trong LOCATION_LIST"""
    if button_name in LOCATION_LIST:
        x, y = LOCATION_LIST[button_name]
        pyautogui.click(x, y)
        if message:
            bot.reply_to(message, f"✅ Đã nhấp chuột vào '{button_name}' tại tọa độ ({x}, {y})")
    else:
        if message:
            bot.reply_to(message, f"⚠️ Button '{button_name}' không tồn tại!")

@bot.message_handler(func=lambda message: message.text.lower().startswith("click "))
def handle_click(message):
    try:
        _, x, y = message.text.split()
        x, y = int(x), int(y)
        pyautogui.click(x, y)  # Click vào tọa độ đã nhập
        bot.reply_to(message, f"✅ Đã nhấp chuột tại tọa độ ({x}, {y})")
    except ValueError:
        bot.reply_to(message, "⚠️ Lệnh không đúng. Dùng: click x y")

@bot.message_handler(func=lambda message: message.text.lower() == "location")
def send_location_list(message):
    response = "Danh sách tọa độ thường dùng:\n"
    for name, (x, y) in LOCATION_LIST.items():
        response += f"- {name}: click {x} {y}\n"

    bot.reply_to(message, response)  
@bot.message_handler(func=lambda message: message.text.lower() == "backspace")
def handle_backspace(message):
    for _ in range(5):
        pyautogui.press("backspace")  # Nhấn phím Space 5 lần
    bot.reply_to(message, "✅ Đã nhấn 5 lần phím xóa")

# Lệnh cap: Chụp màn hình và gửi ảnh
@bot.message_handler(func=lambda message: message.text.lower() == "cap")
def handle_capture(message):
    screenshot_path = "screenshot.png"
    pyautogui.screenshot(screenshot_path)
    with open(screenshot_path, "rb") as photo:
        bot.send_photo(message.chat.id, photo)
    bot.reply_to(message, "📸 Đã chụp màn hình!")
@bot.message_handler(func=lambda message: message.text.lower() == "check giacu")
def handle_capture(message):
    screenshot_path = "giacu.png"
    
    with open(screenshot_path, "rb") as photo:
        bot.send_photo(message.chat.id, photo)
    bot.reply_to(message, "Đã gửi giacu!")
# Lệnh menu: Hiển thị danh sách các lệnh và trạng thái tiến trình
@bot.message_handler(func=lambda message: message.text.lower() == "menu")
def send_menu(message):
    v1_status = "🟢 *Đang chạy*" if current_thread_v1 and current_thread_v1.is_alive() else "🔴 *Đã dừng*"
    v2_status = "🟢 *Đang chạy*" if current_thread_v2 and current_thread_v2.is_alive() else "🔴 *Đã dừng*"

    menu_text = (
        "📜 *Danh sách lệnh:*\n"
        f"- `check giacu` 📍 → Hiển thị giá cũ\n"
        f"- `location` 📍 → Hiển thị danh sách tọa độ\n"
        f"- `click x y` 🎯 → Click vào tọa độ (x, y)\n"
        f"- `cap` 📸 → Chụp màn hình\n"
        f"- `backspace` ⌨️ → Nhấn 5 lần phím Space\n"
        f"- `chup` 📸 → Chụp màn hình ngay lập tức\n"
        f"- `start_v1 i` ▶️ → Chạy `abc(i)` với tham số i\n"
        f"- `cancel_v1` ⏹️ → Dừng `abc()`\n"
        f"- `start_v2` ▶️ → Chạy `xyz()`\n"
        f"- `cancel_v2` ⏹️ → Dừng `xyz()`\n"
        f"- `menu` 📜 → Hiển thị danh sách lệnh\n"
        f"\n📌 *Trạng thái:*\n"
        f"- `v1 (abc)`: {v1_status}\n"
        f"- `v2 (xyz)`: {v2_status}"
    )
    bot.reply_to(message, menu_text, parse_mode="Markdown")






# Biến lưu trữ các thread và trạng thái chạy
current_thread_v1 = None
current_thread_v2 = None
stop_event_v1 = threading.Event()
stop_event_v2 = threading.Event()



# Lệnh start_v1 i: Bắt đầu abc với tham số i
@bot.message_handler(func=lambda message: message.text.lower().startswith("start_v1 "))
def start_v1(message):
    global current_thread_v1, stop_event_v1

    try:
        _, i = message.text.split()
        i = int(i) - 1

        if current_thread_v1 and current_thread_v1.is_alive():
            stop_event_v1.set()
            current_thread_v1.join()

        stop_event_v1.clear()
        current_thread_v1 = threading.Thread(target=abc, args=( stop_event_v1,i), daemon=True)
        current_thread_v1.start()

        bot.reply_to(message, f"✅ Đã bắt đầu v1({i+1})")
    except ValueError:
        bot.reply_to(message, "⚠️ Lệnh không đúng. Dùng: start_v1 i")
# Lệnh start_v2: Bắt đầu xyz()
@bot.message_handler(func=lambda message: message.text.lower() == "start_v2")
def start_v2(message):
    global current_thread_v2, stop_event_v2

    if current_thread_v2 and current_thread_v2.is_alive():
        stop_event_v2.set()
        current_thread_v2.join()

    stop_event_v2.clear()
    current_thread_v2 = threading.Thread(target=xyz, args=(stop_event_v2,), daemon=True)
    current_thread_v2.start()

    bot.reply_to(message, "✅ Đã bắt đầu v2()")
# Lệnh cancel_v1: Dừng abc()
@bot.message_handler(func=lambda message: message.text.lower() == "cancel_v1")
def cancel_v1(message):
    global current_thread_v1, stop_event_v1

    if current_thread_v1 and current_thread_v1.is_alive():
        stop_event_v1.set()
        current_thread_v1.join()
        bot.reply_to(message, "⏹️ Đã dừng abc()")
    else:
        bot.reply_to(message, "⚠️ Không có tiến trình abc() nào đang chạy!")

# Lệnh cancel_v2: Dừng xyz()
@bot.message_handler(func=lambda message: message.text.lower() == "cancel_v2")
def cancel_v2(message):
    global current_thread_v2, stop_event_v2

    if current_thread_v2 and current_thread_v2.is_alive():
        stop_event_v2.set()
        current_thread_v2.join()
        bot.reply_to(message, "⏹️ Đã dừng xyz()")
    else:
        bot.reply_to(message, "⚠️ Không có tiến trình xyz() nào đang chạy!")

# Lệnh chup: Chụp ảnh màn hình ngay lập tức
@bot.message_handler(func=lambda message: message.text.lower() == "chup")
def handle_chup(message):
    chup(1361, 412, 1511, 442, "giacu.png")
    bot.reply_to(message, "📸 Đã cập nhật giá!")
    try:
        with open("giacu.png", "rb") as photo:
            bot.send_photo("7345469514", photo)
        print("✅ Đã gửi ảnh chụp màn hình qua Telegram!")
    except Exception as e:
        print(f"❌ Lỗi khi gửi ảnh: {e}")

bot.polling()



# C:\Users\LENOVO\AppData\Local\Programs\Python\Python312\python.exe C:\tool\test.py
# "7169529565:AAF_VTyhriBeWLvRHd8G5J-fM9pZdCR8PSQ"