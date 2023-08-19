from typing import Final
from telegram import Update
from os import environ as env_variable
from telegram.error import TimedOut as TOerror
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELGRAM_TOKEN: Final =  env_variable.get("TELGRAM_TOKEN")  # Token
BOT_USERNAME: Final =  env_variable.get("BOT_USERNAME")  # Bot Username

# COMMANDS 
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, Welcome to the BETA version of our Base Blockchan bot")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("How may i be of help at the moment?")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Your custom command goes here.")


# RESPONSES

def handle_response(text: str) -> str:
    text: str = text.lower()
    if "base" in text: 
        return "The word 'Base' can be found from the string sent to the bot."
    else: return "You need to add the word 'Base' to what you're typing/sending to us."


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat.id}) in {message_type}: {text}")

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else: return
    else: response: str = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if TOerror == True: print("The request timed out.")
    else: print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Starting BOT...")
    app = Application.builder().token(TELGRAM_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error
    app.add_error_handler(error)

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=1)

