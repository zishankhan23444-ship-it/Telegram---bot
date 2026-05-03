import os
import telebot
import json
import time
from telebot.apihelper import ApiTelegramException
from datetime import datetime, timedelta

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# ========== DATA STORAGE ==========
def load_data():
    try:
        with open('bot_data.json', 'r') as f:
            return json.load(f)
    except:
        return {"warnings": {}, "muted_users": {}, "stats": {}}

def save_data(data):
    with open('bot_data.json', 'w') as f:
        json.dump(data, f)

bot_data = load_data()
user_warnings = bot_data.get("warnings", {})
muted_users = bot_data.get("muted_users", {})
stats = bot_data.get("stats", {})

# ========== ABUSE WORDS ==========
ABUSE_WORDS = [
    'mc', 'bc', 'chutiya', 'bhosdike', 'madarchod', 'behenchod',
    'gandu', 'laude', 'bsdk', 'randi', 'chutiye', 'bhosdi',
    'gand', 'lund', 'chod', 'fuck', 'shit', 'bitch', 'asshole',
    'bastard', 'damn', 'crap', 'stupid', 'chut', 'loda', 'behen',
    'maa', 'rand', 'bhadwa', 'chakka', 'hijda', 'kutta', 'kutiya'
]

# ========== ADMIN CHECK ==========
def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

# ========== COMMANDS ==========
@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.reply_to(message,
            f"🤖 *Hello {message.from_user.first_name}!*\n\n"
            f"Main *Abuse Detector Bot* hoon! 🛡️\n"
            f"Group mein gaali detect karke delete karta hoon!\n\n"
            f"⚠️ *3 Warnings = Auto Mute*\n\n"
            f"📱 *Commands:*\n"
            f"/help - Sab commands\n"
            f"/status - Apna status\n"
            f"/rules - Group rules\n"
            f"/stats - Abuse stats\n\n"
            f"Stay respectful! ✅",
            parse_mode='Markdown'
        )
    except:
        bot.send_message(message.chat.id, "🤖 Bot ready! Use /help")

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "📋 *ABUSE BOT - HELP MENU*\n\n"
        "👤 *User Commands:*\n"
        "• /start - Bot start\n"
        "• /help - Ye menu\n"
        "• /status - Apna warning status\n"
        "• /rules - Group rules\n"
        "• /stats - Group abuse stats\n\n"
        "👮 *Admin Commands:*\n"
        "• /warn @user - Manual warning\n"
        "• /unwarn @user - Warning hatao\n"
        "• /mute @user - User mute karo\n"
        "• /unmute @user - User unmute karo\n"
        "• /ban @user - User ban karo\n"
        "• /reset - Sab warnings reset\n\n"
        "🛡️ *Auto Features:*\n"
        "• Gaali auto-detect\n"
        "• Auto delete message\n"
        "• 3 warnings = mute\n\n"
        "Stay respectful! ✅"
    )
    try:
        bot.reply_to(message, help_text, parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    warnings = user_warnings.get(str(user_id), 0)

    if warnings == 0:
        status_msg = "🟢 Safe"
    elif warnings == 1:
        status_msg = "🟡 Caution"
    elif warnings == 2:
        status_msg = "🟠 Danger"
    else:
        status_msg = "🔴 Muted"

    try:
        bot.reply_to(message,
            f"📊 *{name}'s Status*\n\n"
            f"Status: {status_msg}\n"
            f"Warnings: {warnings}/3\n\n"
            f"Be respectful! 🙏",
            parse_mode='Markdown'
        )
    except:
        pass

@bot.message_handler(commands=['rules'])
def rules(message):
    try:
        bot.reply_to(message,
            "📋 *GROUP RULES*\n\n"
            "✅ *Allowed:*\n"
            "• Respectful baat\n"
            "• Helpful discussion\n"
            "• Friendly jokes\n\n"
            "🚫 *Not Allowed:*\n"
            "• Gaali / Abuse\n"
            "• Spam\n"
            "• Personal attacks\n"
            "• NSFW content\n\n"
            "⚠️ *3 warnings = Mute!*\n"
            "⚠️ *Serious abuse = Direct Ban!*\n\n"
            "Respect everyone! ✅",
            parse_mode='Markdown'
        )
    except:
        pass

@bot.message_handler(commands=['stats'])
def show_stats(message):
    total_warnings = sum(user_warnings.values())
    total_muted = len(muted_users)
    
    # Top offenders
    top_users = sorted(user_warnings.items(), key=lambda x: x[1], reverse=True)[:5]
    top_text = ""
    for uid, count in top_users:
        if count > 0:
            top_text += f"• User `{uid}`: {count} warnings\n"
    
    stats_text = (
        f"📊 *GROUP STATS*\n\n"
        f"Total Warnings Given: {total_warnings}\n"
        f"Currently Muted: {total_muted}\n\n"
        f"🔴 *Top Offenders:*\n"
        f"{top_text if top_text else 'Sab acchhe hain! ✅'}\n\n"
        f"Keep it clean! 🧹"
    )
    
    try:
        bot.reply_to(message, stats_text, parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')

# ========== ADMIN COMMANDS ==========
@bot.message_handler(commands=['warn'])
def warn_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ Sirf admin kar sakta hai!")
        return
    
    try:
        target = message.reply_to_message.from_user.id if message.reply_to_message else None
        if not target:
            bot.reply_to(message, "❌ Kisiko reply karke /warn karo!")
            return
        
        user_warnings[str(target)] = user_warnings.get(str(target), 0) + 1
        save_data({"warnings": user_warnings, "muted_users": muted_users, "stats": stats})
        
        bot.reply_to(message, f"⚠️ User ko warning di gayi! ({user_warnings[str(target)]}/3)")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

@bot.message_handler(commands=['mute'])
def mute_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ Sirf admin kar sakta hai!")
        return
    
    try:
        target = message.reply_to_message.from_user.id if message.reply_to_message else None
        if not target:
            bot.reply_to(message, "❌ Kisiko reply karke /mute karo!")
            return
        
        bot.restrict_chat_member(message.chat.id, target, can_send_messages=False)
        muted_users[str(target)] = True
        save_data({"warnings": user_warnings, "muted_users": muted_users, "stats": stats})
        
        bot.reply_to(message, "🔇 User muted successfully!")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ Sirf admin kar sakta hai!")
        return
    
    try:
        target = message.reply_to_message.from_user.id if message.reply_to_message else None
        if not target:
            bot.reply_to(message, "❌ Kisiko reply karke /unmute karo!")
            return
        
        bot.restrict_chat_member(message.chat.id, target, can_send_messages=True)
        muted_users.pop(str(target), None)
        save_data({"warnings": user_warnings, "muted_users": muted_users, "stats": stats})
        
        bot.reply_to(message, "🔊 User unmuted!")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ Sirf admin kar sakta hai!")
        return
    
    try:
        target = message.reply_to_message.from_user.id if message.reply_to_message else None
        if not target:
            bot.reply_to(message, "❌ Kisiko reply karke /ban karo!")
            return
        
        bot.ban_chat_member(message.chat.id, target)
        bot.reply_to(message, "🚫 User banned!")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

@bot.message_handler(commands=['reset'])
def reset_warnings(message):
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ Sirf admin kar sakta hai!")
        return
    
    global user_warnings, muted_users
    user_warnings = {}
    muted_users = {}
    save_data({"warnings": {}, "muted_users": {}, "stats": stats})
    bot.reply_to(message, "✅ Sab warnings aur mutes reset ho gaye!")

# ========== ABUSE DETECTION ==========
@bot.message_handler(func=lambda message: True)
def detect_abuse(message):
    if not message.text:
        return
    
    # Ignore commands
    if message.text.startswith('/'):
        return
    
    user_id = message.from_user.id
    name = message.from_user.first_name
    text = message.text.lower()
    chat_id = message.chat.id

    # Check if muted
    if str(user_id) in muted_users:
        try:
            bot.delete_message(chat_id, message.message_id)
        except:
            pass
        return

    # Detect abuse
    found_abuse = [word for word in ABUSE_WORDS if word in text]
    
    if found_abuse:
        # Delete message
        try:
            bot.delete_message(chat_id, message.message_id)
        except:
            pass
        
        # Update warnings
        user_warnings[str(user_id)] = user_warnings.get(str(user_id), 0) + 1
        warnings = user_warnings[str(user_id)]
        
        # Save data
        save_data({"warnings": user_warnings, "muted_users": muted_users, "stats": stats})
        
        # Send warning
        if warnings == 1:
            msg = f"⚠️ *Warning 1/3*\nHey {name}!\n🚫 Gaali mat karo: `{', '.join(found_abuse)}`\nPlease respect others! 🙏"
        elif warnings == 2:
            msg = f"🟠 *Warning 2/3*\nHey {name}!\n⚠️ Last warning! Next = *MUTE*!"
        else:
            # Auto mute on 3rd warning
            msg = f"🔴 *MUTED!*\nHey {name}!\n3 warnings complete!\nAb sirf admin unmute kar sakta hai! 🤔"
            try:
                bot.restrict_chat_member(chat_id, user_id, can_send_messages=False)
                muted_users[str(user_id)] = True
                save_data({"warnings": user_warnings, "muted_users": muted_users, "stats": stats})
            except:
                msg += "\n\n⚠️ (Mute failed - admin permissions check karo)"
            user_warnings[str(user_id)] = 0  # Reset after mute

        try:
            bot.send_message(chat_id, msg, parse_mode='Markdown')
        except:
            bot.send_message(chat_id, msg)

print("🤖 Abuse Detector Bot Starting...")
print("✅ Bot is running 24/7!")
bot.polling(none_stop=True)
                
