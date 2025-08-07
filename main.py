from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# توکن باتت رو اینجا بذار (از BotFather بگیر)
TOKEN = "7979487842:AAGf-nOiI1_yZ6Nh--S1FnqyvttJTwOR4KA"

# مرحله‌ها برای گفتگو
SELECT_ROLE = 0

# استارت بات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["زیباجو"], ["فیشیالیست"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("سلام 🌸 لطفاً نقش خودت رو انتخاب کن:", reply_markup=reply_markup)
    return SELECT_ROLE

# واکنش به انتخاب نقش
async def handle_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    role = update.message.text
    await update.message.reply_text(f"نقش انتخاب‌شده: {role}")
    return ConversationHandler.END

# ساخت اپ و اجرای بات
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={SELECT_ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_role)]},
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    print("🤖 Bot is running...")
    app.run_polling()
