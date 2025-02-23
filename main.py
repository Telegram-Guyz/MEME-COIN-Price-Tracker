import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Replace with your Telegram bot token
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# CoinGecko API URL for fetching cryptocurrency data
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the Memecoin Trading Bot! Use /price <coin_id> to check the price of a memecoin."
    )

# Command to fetch the price of a memecoin
async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Get the coin ID from the user's message
        coin_id = context.args[0].lower()  # e.g., "dogecoin" or "shiba-inu"

        # Fetch the price from CoinGecko API
        params = {
            "ids": coin_id,
            "vs_currencies": "usd"
        }
        response = requests.get(COINGECKO_API_URL, params=params)
        data = response.json()

        if coin_id in data:
            price = data[coin_id]["usd"]
            await update.message.reply_text(f"The current price of {coin_id.capitalize()} is ${price:.6f} USD.")
        else:
            await update.message.reply_text(f"Sorry, I couldn't find data for {coin_id}. Please check the coin ID.")

    except (IndexError, KeyError):
        await update.message.reply_text("Usage: /price <coin_id>")
    except Exception as e:
        logger.error(f"Error fetching price: {e}")
        await update.message.reply_text("An error occurred while fetching the price. Please try again later.")

# Main function to run the bot
def main():
    # Create the Application and pass it your bot's token
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", get_price))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
