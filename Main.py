from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

# Telegram Bot token
telegram_token = 'YOUR_TELEGRAM_BOT_TOKEN'

# Only allow your own Telegram ID
allowed_user_id = YOUR_TELEGRAM_USER_ID

# Binance API URL
BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != allowed_user_id:
        await update.message.reply_text("You are not authorized to use this bot.")
        return
    
    welcome_message = (
        "ښه راغلاست! د کرنسي قیمت لپاره وپوښته، لکه: /price BTCUSDT یا /price ETHUSDT\n\n"
        "د استفادې لارښود:\n"
        "/price [TICKER] - د کرنسي قیمت وښياست لکه BTCUSDT"
    )
    await update.message.reply_text(welcome_message)

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != allowed_user_id:
        await update.message.reply_text("You are not authorized to use this bot.")
        return
    
    if not context.args:
        await update.message.reply_text("مهرباني وکړئ د کرنسي سمبول وښياست لکه: /price BTCUSDT")
        return
    
    symbol = context.args[0].upper()
    
    try:
        response = requests.get(f"{BINANCE_API_URL}?symbol={symbol}")
        data = response.json()
        
        if 'price' in data:
            price = float(data['price'])
            formatted_price = "{:,.2f}".format(price)
            await update.message.reply_text(f"د {symbol} قیمت: {formatted_price}$")
        else:
            await update.message.reply_text(f"د {symbol} معلومات ونه موندل شول. مهرباني وکړئ سمبول تایید کړئ.")
    
    except Exception as e:
        await update.message.reply_text(f"ستونزه پيدا شوه: {str(e)}")

def main() -> None:
    application = ApplicationBuilder().token(telegram_token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", get_price))
    
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Bot Error: {e}")
        print("بوت ونه چلېد. مهرباني وکړئ ټوکن یا کوډ وګورئ")
