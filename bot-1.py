import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# 🔑 BOT TOKEN
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# 🚫 ABUSE WORDS
ABUSE_WORDS = [
    'mc', 'bc', 'chutiya', 'bhosdike', 'madarchod', 'behenchod',
    'gandu', 'laude', 'bsdk', 'randi', 'chutiye', 'bhosdi',
    'gand', 'lund', 'chod', 'maa', 'behen', 'fuck', 'shit',
    'bitch', 'asshole', 'bastard', 'damn', 'crap', 'stupid'
]

user_warnings = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🤖 Hello {user.first_name}!\n\n"
        f"Main Abuse Detector Bot hoon! 🛡️\n"
        f"3 warnings = Auto mute! ⚠️\n\n"
        f"/help — Sab commands dekho"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 HELP MENU\n\n"
        "🛡️ Abuse Protection:\n"
        "• Auto-detect gaali\n"
        "• 3 warnings = 2 min mute\n\n"
        "📱 Commands:\n"
        "/start — Bot start\n"
        "/help — Ye menu\n"
        "/status — Apna status\n"
        "/rules — Group rules\n\n"
        "Stay respectful! ✅"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    await update.message.reply_text(
        f"📊 {name}'s Status\n\n"
        f"Status: {status_msg}\n"
        f"Warnings: {warnings}/3"
    )

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 GROUP RULES\n\n"
        "✅ Allowed:\n"
        "• Respectful baat\n"
        "• Helpful discussion\n\n"
        "🚫 Not Allowed:\n"
        "• Gaali/abuse\n"
        "• Spam\n"
        "• Personal attacks\n\n"
        "⚠️ 3 warnings = 2 min mute!"
    )

async def detect_abuse(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            await update.message.delete()
        except:
            pass

        if warnings == 1:
            msg = f"⚠️ Warning 1/3\nHey {name}!\n🚫 Abuse: {', '.join(found_abuse)}\nPlease respect others! 🙏"
        elif warnings == 2:
            msg = f"🟠 Warning 2/3\nHey {name}!\n🚫 Abuse: {', '.join(found_abuse)}\n⚠️ Last warning! Next = Mute!"
        else:
            msg = f"🔴 MUTED!\nHey {name}!\n🚫 3 warnings complete!\n⏳ Muted for 2 minutes!\nThink about it! 🤔"
            user_warnings[user_id] = 0

        await update.message.reply_text(msg)

async def main():
    print("🤖 Abuse Detector Bot Starting...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detect_abuse))
    print("✅ Bot is running 24/7!")
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
