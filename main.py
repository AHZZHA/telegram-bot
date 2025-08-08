from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

TOKEN = "7979487842:AAGf-nOiI1_yZ6Nh--S1FnqyvttJTwOR4KA"

# مراحل گفتگو
(SELECT_ROLE, SKIN_TYPE, GENDER, AGE, SKIN_ISSUE,
 MEDICAL_CONDITION, LOCATION) = range(7)

# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["زیباجو"], ["فیشیالیست"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "سلام خوش‌اومدی عزیز دلم 💖\n\n"
        "برای شروع لطفاً نقش خودت رو انتخاب کن:", reply_markup=reply_markup)
    return SELECT_ROLE

# مرحله انتخاب نقش
async def handle_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    role = update.message.text
    context.user_data['role'] = role

    if role == "زیباجو":
        await update.message.reply_text(
            "🌸 برای اینکه بتونی نوع پوستت رو دقیق‌تر انتخاب کنی، این راهنمای کوچولو رو ببین:\n\n"
            "💦 **پوست چرب:** براقه، جوش‌داره، منافذش بازه.\n"
            "🌵 **پوست خشک:** زود پوسته‌پوسته میشه، احساس کشیدگی داره.\n"
            "🌗 **پوست مختلط:** بینی و پیشونی چربه، گونه‌ها خشکن.\n"
            "🌈 **پوست نرمال:** تعادل داره، بدون مشکل خاص.\n"
            "🔥 **پوست حساس:** سریع قرمز میشه یا واکنش نشون میده.\n\n"
            "حالا نوع پوستت رو انتخاب کن عزیزم 👇"
        )
        keyboard = [
            ["پوست چرب"], ["پوست خشک"],
            ["پوست مختلط"], ["پوست نرمال"],
            ["پوست حساس"]
        ]
        return await send_question(update, keyboard, "❔ نوع پوستت رو انتخاب کن:", SKIN_TYPE)

    elif role == "فیشیالیست":
        await update.message.reply_text("🧖‍♀️ حالت فیشیالیست به زودی اضافه میشه 💅")
        return ConversationHandler.END

    else:
        await update.message.reply_text("لطفاً فقط از دکمه‌ها استفاده کن 💬")
        return SELECT_ROLE

# نوع پوست
async def handle_skin_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['skin_type'] = update.message.text
    keyboard = [["زن"], ["مرد"], ["غیره / ترجیح نمی‌دم بگم"]]
    return await send_question(update, keyboard,
        "🌟 حالا لطفاً جنسیتت رو مشخص کن تا بهتر راهنمایی‌ت کنیم 👇", GENDER)

# جنسیت
async def handle_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['gender'] = update.message.text
    keyboard = [
        ["۱۵-۲۰"], ["۲۱-۲۵"], ["۲۶-۳۰"],
        ["۳۱-۳۵"], ["۳۶-۴۵"], ["۴۶+"]
    ]
    return await send_question(update, keyboard,
        "🎂 سن تقریبی‌ت رو انتخاب کن عزیزم:", AGE)

# سن
async def handle_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['age'] = update.message.text
    await update.message.reply_text(
        "🔍 دغدغه‌ی پوستیت چیه؟\n\n"
        "کمکت می‌کنم راحت‌تر انتخاب کنی:\n"
        "🔴 جوش: التهاب، آکنه، جای جوش\n"
        "🟤 لک: تیرگی، آفتاب‌سوختگی، جای زخم\n"
        "🔘 خشکی یا حساسیت: قرمزی، خارش، کشیدگی\n"
        "⚪️ چربی و منافذ: پوست براق، دانه‌های سرسیاه\n"
        "🔵 چروک یا افتادگی: خطوط، شل‌شدگی"
    )
    keyboard = [
        ["جوش / آکنه"], ["لک / تیرگی"],
        ["خشکی / حساسیت"], ["چربی / منافذ"],
        ["چروک / افتادگی"]
    ]
    return await send_question(update, keyboard,
        "👇 دغدغه‌ی اصلی پوستت رو انتخاب کن:", SKIN_ISSUE)

# مشکل پوستی
async def handle_skin_issue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['skin_issue'] = update.message.text
    keyboard = [["ندارم"], ["دارم (دارو یا بیماری خاص)"]]
    await update.message.reply_text(
        "💊 اگه بیماری یا داروی خاصی داری، می‌تونیم روتین مناسب‌تر پیشنهاد بدیم.\n"
        "لطفاً وضعیتت رو مشخص کن:")
    return await send_question(update, keyboard, "", MEDICAL_CONDITION)

# دارو یا بیماری
async def handle_medical(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['medical'] = update.message.text
    await update.message.reply_text(
        "🏞 محل زندگی‌ت هم مهمه چون آب‌وهوا روی پوست خیلی تأثیر داره:\n"
        "🌞 گرم و خشک → احتمال خشکی یا لک بیشتر\n"
        "🌧 مرطوب و شرجی → بیشتر چربی و جوش\n"
        "🏔 سرد و خشک → نیاز به رطوبت و محافظت بالا"
    )
    keyboard = [
        ["شمال ایران"], ["جنوب ایران"],
        ["مرکز ایران"], ["شرق ایران"],
        ["غرب ایران"]
    ]
    return await send_question(update, keyboard, "📍 منطقه زندگی‌ت رو انتخاب کن:", LOCATION)

# محل زندگی
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['location'] = update.message.text

    # خلاصه اطلاعات
    data = context.user_data
    await update.message.reply_text(
        f"✨ اطلاعاتی که ازت گرفتیم:\n\n"
        f"🌿 نوع پوست: {data['skin_type']}\n"
        f"👤 جنسیت: {data['gender']}\n"
        f"🎂 سن: {data['age']}\n"
        f"🔍 دغدغه پوستی: {data['skin_issue']}\n"
        f"💊 وضعیت پزشکی: {data['medical']}\n"
        f"📍 محل زندگی: {data['location']}\n\n"
        "💫 بزودی بر اساس این اطلاعات، روتین‌های شخصی‌سازی‌شده برات آماده می‌کنم!\n"
        "صبر کن تا تحلیل بشه... 🤖🧴"
    )
    return ConversationHandler.END

# تابع کمکی برای ارسال سؤال با کیبورد
async def send_question(update, keyboard, message, next_state):
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(message, reply_markup=reply_markup)
    return next_state

# اجرای اپ
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_role)],
            SKIN_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_skin_type)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gender)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_age)],
            SKIN_ISSUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_skin_issue)],
            MEDICAL_CONDITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_medical)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_location)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    print("🤖 Bot is running...")
    app.run_polling()
