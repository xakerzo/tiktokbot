import logging
import os
import requests
import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config import BOT_TOKEN

# Log sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# TikTok video yuklab olish funksiyasi
def download_tiktok_video(url, chat_id, context):
    try:
        context.bot.send_chat_action(chat_id=chat_id, action="typing")
        
        # TikTok video ma'lumotlarini olish
        api_url = f"https://www.tikwm.com/api/?url={url}"
        
        response = requests.get(api_url)
        data = response.json()
        
        if data.get('code') == 0:
            video_url = data['data']['play']
            
            # Videoni yuborish
            context.bot.send_video(
                chat_id=chat_id,
                video=video_url,
                caption="🎵 Video muvaffaqiyatli yuklab olindi!\n\n" +
                       "🤖 @tiktokdan_yuklabot\n" +
                       "🎮 PUBG MOBILE uchun ARZON UC SERVICE @ZakirShaX"
            )
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text="❌ Video yuklab olinmadi. Iltimos, linkni tekshiring yoki boshqa video yuboring."
            )
            
    except Exception as e:
        logger.error(f"Xatolik: {str(e)}")
        context.bot.send_message(
            chat_id=chat_id,
            text="❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring."
        )

# Start komandasi
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    welcome_text = f"""
👋 Salom {user.first_name}!

Menga TikTokdan link tashlang, men uni original holida video qilib sizga yuboraman. VIDEOda xechqanday egasini nomi chiqmaydi!

📥 Botdan foydalanish uchun TikTok video linkini yuboring.

🎮 PUBG MOBILE uchun ARZON UC SERVICE: @ZakirShaX
    """
    update.message.reply_text(welcome_text)

# Yordam komandasi
def help_command(update: Update, context: CallbackContext):
    help_text = """
📖 **Botdan qanday foydalaniladi?**

1. TikTok ilovasidan video linkini nusxalang
2. Linkni shu yerga yuboring
3. Men video ni original holida yuklab beraman

🔗 Link nusxalash: 
   TikTok → Share → Copy Link

⚠️ Eslatma: Video larda hech qanday watermark yoki egasini nomi chiqmaydi!

🎮 PUBG MOBILE uchun ARZON UC SERVICE: @ZakirShaX
🤖 Bizning bot: @tiktokdan_yuklabot
    """
    update.message.reply_text(help_text)

# Xabarlarni qayta ishlash
def handle_message(update: Update, context: CallbackContext):
    message_text = update.message.text
    
    # TikTok linkini tekshirish
    tiktok_patterns = [
        r'https?://(?:www\.)?tiktok\.com/[@\w./-]+',
        r'https?://vm\.tiktok\.com/[\w+/]+',
        r'https?://vt\.tiktok\.com/[\w+/]+'
    ]
    
    is_tiktok_link = any(re.match(pattern, message_text) for pattern in tiktok_patterns)
    
    if is_tiktok_link:
        update.message.reply_text("⏳ Video yuklanmoqda... VIDEOda xechqanday egasini nomi chiqmaydi!")
        download_tiktok_video(message_text, update.message.chat_id, context)
    else:
        update.message.reply_text(
            "❌ Iltimos, faqat TikTok linkini yuboring!\n\n" +
            "📎 Namuna: https://vm.tiktok.com/xxxxxxxxx/\n" +
            "Yoki /help buyrug'i bilan yordam oling.\n\n" +
            "🎮 PUBG MOBILE uchun ARZON UC SERVICE: @ZakirShaX"
        )

# Xatolik handleri
def error(update: Update, context: CallbackContext):
    logger.warning(f'Update "{update}" caused error "{context.error}"')

# Asosiy funksiya
def main():
    # Botni yaratish (eski versiya uchun)
    updater = Updater(BOT_TOKEN, use_context=True)
    
    # Dispatcher
    dp = updater.dispatcher
    
    # Handlerlarni qo'shish
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Xatolik handleri
    dp.add_error_handler(error)
    
    # Botni ishga tushurish
    print("🤖 Bot ishga tushdi...")
    print("🤖 Bot username: @tiktokdan_yuklabot")
    print("🎮 PUBG UC: @ZakirShaX")
    
    # Polling ni boshlash
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
