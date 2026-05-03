import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

ABUSE_WORDS = [
    'mc', 'bc', 'chutiya', 'bhosdike', 'madarchod', 'behenchod',
    'gandu', 'laude', 'bsdk', 'randi', 'chutiye', 'bhosdi',
    'gand', 'lund', 'chod', 'fuck', 'shit',
    'bitch', 'asshole', 'bastard', 'damn', 'crap', 'stupid'
]

user_warnings = {}

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(
        f"🤖 Hello {user.first_name}!\n\n"
        f"Main Abuse Detector Bot hoon! 🛡️\n"
        f"3 warnings = Auto mute! ⚠️\n\n"
        f"/help — Sab commands dekho"
    )

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
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

def status(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    name = update.effective_user.first_name
    warnings = user_warnings.get(user_id, 0)

    if warnings == 0:
        status_msg = "🟢 Safe"
    elif warnings == 1:
        status_msg = "🟡 Caution"
    elif warnings == 2:
        status_msg = "🟠 Danger"
    else:
        status_msg = "🔴 Muted"

    update.message.reply_text(
        f"📊 {name}'s Status\n\n"
        f"Status: {status_msg}\n"
        f"Warnings: {warnings}/3"
    )

def rules(update: Update, context: CallbackContext):
    update.message.reply_text(
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

def detect_abuse(update: Update, context: CallbackContext):
    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    name = update.effective_user.first_name
    text = update.message.text.lower()

    found_abuse = []
    for word in ABUSE_WORDS:
        if word in text:
            found_abuse.append(word)

    if found_abuse:
        user_warnings[user_id] = user_warnings.get(user_id, 0) + 1
        warnings = user_warnings[user_id]

        try:
            update.message.delete()
        except:
            pass

        if warnings == 1:
            msg = f"⚠️ Warning 1/3\nHey {name}!\n🚫 Gaali mat karo!\nPlease respect others! 🙏"
        elif warnings == 2:
            msg = f"🟠 Warning 2/3\nHey {name}!\n⚠️ Last warning! Next = Mute!"
        else:
            msg = f"🔴 MUTED!\nHey {name}!\n3 warnings complete!\nThink about it! 🤔"
            user_warnings[user_id] = 0

        update.message.reply_text(msg)

def main():
    print("🤖 Abuse Detector Bot Starting...")
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, detect_abuse))
    print("✅ Bot is running 24/7!")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
