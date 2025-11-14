import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import re
import os
from config import BOT_TOKEN, DOWNLOAD_PATH, MAX_FILE_SIZE

# Log sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Yuklab olish papkasini yaratish
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

# TikTok video yuklab olish funksiyasi
async def download_tiktok_video(url, chat_id, context):
    try:
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")
        
        # TikTok video ma'lumotlarini olish
        api_url = f"https://www.tikwm.com/api/?url={url}"
        
        response = requests.get(api_url)
        data = response.json()
        
        if data.get('code') == 0:
            video_url = data['data']['play']
            
            # Videoni yuborish (caption siz)
            await context.bot.send_video(
                chat_id=chat_id,
                video=video_url,
                caption="🎵 Video muvaffaqiyatli yuklab olindi!\n\n" +
                       "🤖 @tiktokdan_yuklabot\n" +
                       "🎮 PUBG MOBILE uchun ARZON UC SERVICE @ZakirShaX"
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ Video yuklab olinmadi. Iltimos, linkni tekshiring yoki boshqa video yuboring."
            )
            
    except Exception as e:
        logging.error(f"Xatolik: {str(e)}")
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring."
        )

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    welcome_text = f"""
👋 Salom {user.first_name}!

Menga TikTokdan link tashlang, men uni original holida video qilib sizga yuboraman. VIDEOda xechqanday egasini nomi chiqmaydi!

📥 Botdan foydalanish uchun TikTok video linkini yuboring.

🎮 PUBG MOBILE uchun ARZON UC SERVICE: @ZakirShaX
    """
    await update.message.reply_text(welcome_text)

# Yordam komandasi
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    
    # TikTok linkini tekshirish
    tiktok_patterns = [
        r'https?://(?:www\.)?tiktok\.com/[@\w./-]+',
        r'https?://vm\.tiktok\.com/[\w+/]+',
        r'https?://vt\.tiktok\.com/[\w+/]+'
    ]
    
    is_tiktok_link = any(re.match(pattern, message_text) for pattern in tiktok_patterns)
    
    if is_tiktok_link:
        await update.message.reply_text("⏳ Video yuklanmoqda... VIDEOda xechqanday egasini nomi chiqmaydi!")
        await download_tiktok_video(message_text, update.message.chat_id, context)
    else:
        await update.message.reply_text(
            "❌ Iltimos, faqat TikTok linkini yuboring!\n\n" +
            "📎 Namuna: https://vm.tiktok.com/xxxxxxxxx/\n" +
            "Yoki /help buyrug'i bilan yordam oling.\n\n" +
            "🎮 PUBG MOBILE uchun ARZON UC SERVICE: @ZakirShaX"
        )

# Asosiy funksiya
def main():
    # Botni yaratish
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Botni ishga tushurish
    print("🤖 Bot ishga tushdi...")
    print("🤖 Bot username: @tiktokdan_yuklabot")
    print("🎮 PUBG UC: @ZakirShaX")
    application.run_polling()

if __name__ == '__main__':
    main()