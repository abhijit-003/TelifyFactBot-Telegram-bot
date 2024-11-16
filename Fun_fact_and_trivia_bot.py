import pytz
import logging
import requests
import random
import datetime
import sqlite3
from telegram import Update, InlineKeyboardButton,  InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,MessageHandler, filters,CallbackContext,
    ContextTypes, InlineQueryHandler
)
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os


TOKEN = 'YOUR_TELEGRAM_BOT_API_CODE'  # Replace with your actual token
# Setup logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# APIs
NUMBERS_API = "http://numbersapi.com"
TRIVIA_API = "https://opentdb.com/api.php?amount=1"
HISTORY_API = "https://byabbe.se/on-this-day/"
QUOTABLE_API = "http://api.quotable.io/random"

# Database setup
conn = sqlite3.connect('subscriptions.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS subscribers (user_id INTEGER PRIMARY KEY)''')
conn.commit()

# Helper Functions
def fetch_number_fact(number):
    response = requests.get(f"{NUMBERS_API}/{number}/trivia")
    return response.text if response.ok else "No fact available for this number."

def fetch_random_fact():
    # Fetch a random trivia fact
    response = requests.get(TRIVIA_API)
    data = response.json()
    #return data['results'][0]['question'] if response.ok else "No fact available."

    # Fetch a random fact (not a question)
    response = requests.get("https://api.api-ninjas.com/v1/facts", headers={"X-Api-Key": "ylUNQ5L+d9b8XtrBuLa9gg==5sbvXtE5GaazQu1J"})
    if response.ok:
        data = response.json()
        return data[0]['fact']  # Assuming the fact is inside 'fact' key
    else:
        return "No fact available."

     

def fetch_quote():
    # Fetch a random quote
    try:
        response = requests.get(QUOTABLE_API)
        response.raise_for_status()  # This will raise an exception for 4xx/5xx responses
        if response.ok:
            data = response.json()
            return data.get('content', "No fact available.")
        else:
            return "No fact available."
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching random fact: {e}")
        return "Sorry, I couldn't fetch a fact at the moment."
    
def fetch_today_fact():
    today = datetime.datetime.now()
    response = requests.get(f"{HISTORY_API}/{today.month}/{today.day}.json")
    if response.ok:
        events = response.json().get("events")
        return random.choice(events).get("description") if events else "No events found."
    return "No historical events found."

def subscribe_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO subscribers (user_id) VALUES (?)", (user_id,))
    conn.commit()

def unsubscribe_user(user_id):
    cursor.execute("DELETE FROM subscribers WHERE user_id = ?", (user_id,))
    conn.commit()

def get_subscribers():
    cursor.execute("SELECT user_id FROM subscribers")
    return [user_id[0] for user_id in cursor.fetchall()]


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply =  "sorry, currently i am unable to processed your text!!"
    await update.message.reply_text(reply)

async def send_daily_fact(context: CallbackContext):
    fact = fetch_random_fact()
    subscribers = get_subscribers()
    for user_id in subscribers:
        try:
            await context.bot.send_message(chat_id=user_id, text=f"📅 Daily Fact: {fact}")
        except Exception as e:
            logging.error(f"Error sending message to {user_id}: {e}")

# Command Handlers
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "🤖 Welcome to the Fun Fact & Trivia Bot! 🎉\n"
        "Use /fact for a random fact.\n"
        "Use /today for historical facts.\n"
        "Use /number [number] for number trivia.\n"
        "use /quote - for motivational quote. \n"
        "Use /quiz for a fun quiz.\n"
        "Use /subscribe to get daily facts.\n"
        "Use /unsubscribe to stop receiving daily facts."
    )

async def random_fact(update: Update, context: CallbackContext) -> None:
    fact = fetch_random_fact()  # Corrected to fetch a random fact instead of a question
    await update.message.reply_text(f"💡 {fact}")

async def random_quote(update: Update, context: CallbackContext) -> None:
    quote = fetch_quote()
    await update.message.reply_text(quote)

async def today_fact(update: Update, context: CallbackContext) -> None:
    fact = fetch_today_fact()
    await update.message.reply_text(f"📅 {fact}")

async def number_fact(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        await update.message.reply_text("Please provide a number. E.g., /number 42")
        return
    number = context.args[0]
    fact = fetch_number_fact(number)
    await update.message.reply_text(f"🔢 {fact}")

async def quiz(update: Update, context: CallbackContext) -> None:
    response = requests.get(TRIVIA_API)
    question = response.json()['results'][0]
    await update.message.reply_poll(
        question=question['question'],
        options=question['incorrect_answers'] + [question['correct_answer']],
        type='quiz',
        correct_option_id=len(question['incorrect_answers'])
    )

async def subscribe(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    subscribe_user(user_id)
    await update.message.reply_text("You've subscribed to daily facts! 🎉")

async def unsubscribe(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    unsubscribe_user(user_id)
    await update.message.reply_text("You've unsubscribed from daily facts. 😢")

# Main Function
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fact", random_fact))
    app.add_handler(CommandHandler("quote", random_quote))
    app.add_handler(CommandHandler("today", today_fact))
    app.add_handler(CommandHandler("number", number_fact))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    # Schedule daily fact
    scheduler = BackgroundScheduler()
    
    # Define the timezone (e.g., Asia/Kolkata for India)
    timezone = pytz.timezone('Asia/Kolkata')

    # Schedule daily fact with the correct timezone
    scheduler.add_job(
        send_daily_fact, 
        'cron', 
        hour=9, 
        minute=0, 
        args=[app.bot], 
        timezone=timezone
    )

    scheduler.start()

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
