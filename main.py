import telebot
from telebot import types

TOKEN = "8356524795:AAFR_dI7jmYfeJZ-AaJE86Zl-pMrD7kQKzQ"
ADMIN_ID = 7816419648  # bu yerga O‘Z Telegram ID’ingni yoz

bot = telebot.TeleBot(TOKEN)

users = set()

# /start
@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.chat.id)

    text = (
        "🌙 *Assalomu alaykum va rahmatullohu va barakatuh!*\n\n"
        "Ramazon oyining fayz va barakasi barchamizga nasib etsin 🙌\n\n"
        "👇 Quyidagi tugmalar orqali RamazonApp ilovalariga o‘ting"
    )

    markup = types.InlineKeyboardMarkup(row_width=1)

    markup.add(
        types.InlineKeyboardButton(
            "🌙 RamazonApp",
            web_app=types.WebAppInfo(
                "https://javlonbe27-cmd.github.io/Myapp/"
            )
        ),
        types.InlineKeyboardButton(
            "🗓 TAQVIM",
            web_app=types.WebAppInfo(
                "https://javlonbe27-cmd.github.io/Taqvim/"
            )
        ),
        types.InlineKeyboardButton(
            "Ramazon Hadyasi😍",
            web_app=types.WebAppInfo(
                "https://javlonbe27-cmd.github.io/Airamazon/"
            )
        ),
        types.InlineKeyboardButton(
            "🤝 Hamkorlik",
            url="https://t.me/javl0nbe"
        ),
        types.InlineKeyboardButton(
            "📢 Botni ulashish",
            switch_inline_query=(
                "Assalomu alaykum!\n"
                "@RAMAZONAPP_BOT ga kiring va turli xil funksiyalardan "
                "habardor bo‘ling. 🕌📅"
            )
        )
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ADMIN PANEL
@bot.message_handler(commands=['javlon'])
def admin_panel(message):
    if message.chat.id != ADMIN_ID:
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📊 Statistika")
    markup.add("✉️ Xabar yuborish")
    markup.add("🔁 Forward xabar")

    bot.send_message(
        message.chat.id,
        "⚙️ *Admin panel*",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# Statistika
@bot.message_handler(func=lambda m: m.text == "📊 Statistika")
def stats(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(
            message.chat.id,
            f"👥 Foydalanuvchilar soni: {len(users)}"
        )

# Oddiy xabar yuborish
@bot.message_handler(func=lambda m: m.text == "✉️ Xabar yuborish")
def ask_broadcast(message):
    if message.chat.id == ADMIN_ID:
        msg = bot.send_message(
            message.chat.id,
            "Yuboriladigan xabarni yozing:"
        )
        bot.register_next_step_handler(msg, broadcast)

def broadcast(message):
    if message.chat.id == ADMIN_ID:
        for user in users:
            try:
                bot.send_message(user, message.text)
            except:
                pass
        bot.send_message(message.chat.id, "✅ Xabar yuborildi")

# Forward xabar
@bot.message_handler(func=lambda m: m.text == "🔁 Forward xabar")
def ask_forward(message):
    if message.chat.id == ADMIN_ID:
        msg = bot.send_message(
            message.chat.id,
            "Forward qilinadigan xabarni yuboring:"
        )
        bot.register_next_step_handler(msg, forward_msg)

def forward_msg(message):
    if message.chat.id == ADMIN_ID:
        for user in users:
            try:
                bot.forward_message(
                    user,
                    message.chat.id,
                    message.message_id
                )
            except:
                pass
        bot.send_message(message.chat.id, "✅ Forward yuborildi")

print("Bot ishlayapti...")
bot.infinity_polling()
