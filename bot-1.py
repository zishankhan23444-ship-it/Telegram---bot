import os
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

ABUSE_WORDS = [
    'mc', 'bc', 'chutiya', 'bhosdike', 'madarchod', 'behenchod',
    'gandu', 'laude', 'bsdk', 'randi', 'chutiye', 'bhosdi',
    'gand', 'lund', 'chod', 'fuck', 'shit',
    'bitch', 'asshole', 'bastard', 'damn', 'crap', 'stupid'
]

user_warnings = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        f"🤖 Hello {message.from_user.first_name}!\n\n"
        f"Main Abuse Detector Bot hoon! 🛡️\n"
        f"3 warnings = Auto mute! ⚠️\n\n"
        f"/help — Sab commands dekho"
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message,
        "📋 HELP MENU\n\n"
        "🛡️ Abuse Protection:\n"
        "• Auto-detect gaali\n"
        "• 3 warnings = mute\n\n"
        "📱 Commands:\n"
        "/start — Bot start\n"
        "/help — Ye menu\n"
        "/status — Apna status\n"
        "/rules — Group rules\n\n"
        "Stay respectful! ✅"
    )

@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    warnings = user_warnings.get(user_id, 0)

    if warnings == 0:
        status_msg = "🟢 Safe"
    elif warnings == 1:
        status_msg = "🟡 Caution"
    elif warnings == 2:
        status_msg = "🟠 Danger"
    else:
        status_msg = "🔴 Muted"

    bot.reply_to(message,
        f"📊 {name}'s Status\n\n"
        f"Status: {status_msg}\n"
        f"Warnings: {warnings}/3"
    )

@bot.message_handler(commands=['rules'])
def rules(message):
    bot.reply_to(message,
        "📋 GROUP RULES\n\n"
        "✅ Allowed:\n"
        "• Respectful baat\n"
        "• Helpful discussion\n\n"
        "🚫 Not Allowed:\n"
        "• Gaali/abuse\n"
        "• Spam\n"
        "• Personal attacks\n\n"
        "⚠️ 3 warnings = mute!"
    )

@bot.message_handler(func=lambda message: True)
def detect_abuse(message):
    if not message.text:
        return

    user_id = message.from_user.id
    name = message.from_user.first_name
    text = message.text.lower()

    found_abuse = []
    for word in ABUSE_WORDS:
        if word in text:
            found_abuse.append(word)

    if found_abuse:
        user_warnings[user_id] = user_warnings.get(user_id, 0) + 1
        warnings = user_warnings[user_id]

        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

        if warnings == 1:
            msg = f"⚠️ Warning 1/3\nHey {name}!\n🚫 Gaali mat karo!\nPlease respect others! 🙏"
        elif warnings == 2:
            msg = f"🟠 Warning 2/3\nHey {name}!\n⚠️ Last warning! Next = Mute!"
        else:
            msg = f"🔴 MUTED!\nHey {name}!\n3 warnings complete!\nThink about it! 🤔"
            user_warnings[user_id] = 0

        bot.reply_to(message, msg)

print("🤖 Abuse Detector Bot Starting...")
print("✅ Bot is running 24/7!")
bot.polling(none_stop=True)
