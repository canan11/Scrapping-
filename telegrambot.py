import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_BOT_TOKEN = '8141614861:AAGknHH-PRaOhaFxPcC1UoOhpiR7Wm6RbTk'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salam, mən Canan terefinden yazilmis scrapping botuyam. "
        "Melumat elde etmek üçün 'menzil' yazın."
    )

async def telefon_cavabi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower() == 'menzil':
        url = "https://bina.az/baki/alqi-satqi/menziller/yeni-tikili/4-otaqli"
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            flats = soup.find_all("div", class_="items-i")
            message_lines = []

            for flat in flats[:20]:  
                title = flat.find("ul", class_="name")
                price = flat.find("div", class_="price")

                if title and price:
                    name = title.get_text(strip=True)
                    cost = price.get_text(strip=True)
                    message_lines.append(f"{name} — {cost}")

            if message_lines:
                await update.message.reply_text("menziller:\n\n" + "\n".join(message_lines))
            else:
                await update.message.reply_text("Saytdan melumat goture bilmedim.")
        except Exception as e:
            await update.message.reply_text(f"Xəta baş verdi: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, telefon_cavabi))

    print("Bot artiq işləyir.")
    app.run_polling()