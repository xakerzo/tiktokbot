import os
import logging
import requests
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Log sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot tokenini environment variable dan olish
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable topilmadi!")
    exit(1)

# TikTok video yuklab olish funksiyasi
async def download_tiktok_video(url: str, update: Update, context: CallbackContext):
    try:
        await update.message.reply_text("⏳ Video yuklanmoqda... VIDEOda xechqanday egasini nomi chiqmaydi!")
        
        # TikTok video ma'lumotlarini olish
        api_url = f"https://www.tikwm.com/api/?url={url}"
        
        response = requests.get(api_url)
        data = response.json()
        
        if data.get('code') == 0:
            video_url = data['data']['play']
            
            # Videoni yuborish
            await update.message.reply_video(
                video=video_url,
                caption="🎵 Video muvaffaqiyatli yuklab olindi!\n\n" +
                       "🤖 @tiktokdan_yuklabot\n" +
                       "🎮 PUBG MOBILE uchun ARZON UC SERVICE @ZakirShaX"
            )
        else:
            await update.message.reply_text(
                "❌ Video yuklab olinmadi. Iltimos, linkni tekshiring yoki boshqa video yuboring."
            )
            
    except Exception as e:
        logger.error(f"Xatolik: {str(e)}")
        await update.message.reply_text(
            "❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring."
        )

# Start komandasi
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    welcome_text = f"""
👋 Salom {user.first_name}!

Menga TikTokdan link tashlang, men uni original holida video qilib sizga yuboraman. VIDEOda xechqanday egasini nomi chiqmaydi!

📥 Botdan foydalanish uchun TikTok video linkini yuboring.

🎮 PUBG MOBILE uchun ARZON UC SERVICE: @ZakirShaX
    """
    await update.message.reply_text(welcome_text)

# Yordam komandasi
async def help_command(update: Update, context: CallbackContext):
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
    await update.message.reply_text(help_text)

# Xabarlarni qayta ishlash
async def handle_message(update: Update, context: CallbackContext):
    message_text = update.message.text
    
    # TikTok linkini tekshirish
    tiktok_patterns = [
        r'https?://(?:www\.)?tiktok\.com/[@\w./-]+',
        r'https?://vm\.tiktok\.com/[\w+/]+',
        r'https?://vt\.tiktok\.com/[\w+/]+'
    ]
    
    is_tiktok_link = any(re.match(pattern, message_text) for pattern in tiktok_patterns)
    
    if is_tiktok_link:
        await download_tiktok_video(message_text, update, context)
    else:
        await update.message.reply_text(
            "❌ Iltimos, faqat TikTok linkini yuboring!\n\n" +
            "📎 Namuna: https://vm.tiktok.com/xxxxxxxxx/\n" +
            "Yoki /help buyrug'i bilan yordam oling.\n\n" +
            "🎮 PUBG MOBILE uchun ARZON UC SERVICE: @ZakirShaX"
        )

# Xatolik handleri
async def error_handler(update: Update, context: CallbackContext):
    logger.error(f'Xatolik: {context.error}')

# Asosiy funksiya
def main():
    # Botni yaratish
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Xatolik handleri
    application.add_error_handler(error_handler)
    
    # Botni ishga tushurish
    logger.info("🤖 Bot ishga tushdi...")
    logger.info("🤖 Bot username: @tiktokdan_yuklabot")
    logger.info("🎮 PUBG UC: @ZakirShaX")
    
    # Polling ni boshlash
    application.run_polling()

if __name__ == '__main__':
    main()
