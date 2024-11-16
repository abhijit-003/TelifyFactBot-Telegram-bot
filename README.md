# Fun Fact & Trivia Bot [@TelifyFactBot](https://t.me/TelifyFactBot) 🤖🎉

## Overview
The **Fun Fact & Trivia Bot** is a versatile Telegram bot designed to engage users with fun facts, motivational quotes, trivia questions, and historical events. The bot supports scheduled tasks to send daily facts to subscribed users and uses SQLite for managing subscriptions.

## Features
- **Random Facts**: Get a random trivia or general fact.
- **Historical Events**: Discover interesting historical events that happened on today's date.
- **Number Facts**: Learn trivia about any number (e.g., `/number 42`).
- **Motivational Quotes**: Receive a motivational quote to brighten your day.
- **Fun Quiz**: Test your knowledge with trivia questions.
- **Daily Facts Subscription**: Subscribe to receive daily facts.
- **General Text Handling**: The bot responds to general text messages with a default reply.
- **Scheduled Daily Fact Delivery**: Uses a scheduler to send daily facts at a specified time.

## Commands

| Command               | Description                                                        |
|-----------------------|--------------------------------------------------------------------|
| `/start`             | Welcomes the user and provides a list of available commands.       |
| `/fact`              | Sends a random fun fact.                                           |
| `/today`             | Sends a historical fact related to today's date.                   |
| `/number [number]`   | Provides trivia for the specified number.                          |
| `/quote`             | Sends a motivational quote.                                        |
| `/quiz`              | Sends a fun quiz question.                                         |
| `/subscribe`         | Subscribes the user to receive daily facts.                        |
| `/unsubscribe`       | Unsubscribes the user from daily facts.                            |


## Python Script
View Fun Fact bot source code on [**TelifyFactBot**](https://github.com/abhijit-003/Fun-Fact-TelifyMeBot-bot/blob/main/Fun_fact_and_trivia_bot.py)

## How It Works
### 1. Bot Initialization
- The bot is initialized using the `ApplicationBuilder()` method from the `python-telegram-bot` library.
- Logging is configured to capture information and errors.
- SQLite database (`subscriptions.db`) is used to manage user subscriptions.

### 2. Command Handling
- **Command Handlers** are set up for each command to respond to user inputs.
- **Message Handlers** catch all other general text messages that are not commands.

### 3. Fact Fetching APIs
The bot fetches content from several APIs:
- **Numbers API**: Provides trivia related to numbers.
- **Open Trivia Database API**: Supplies quiz questions.
- **Quotable API**: Fetches motivational quotes.
- **Byabbe API**: Shares historical events for the current date.
- **API Ninjas**: Provides random general facts.

### 4. Subscription Management
- Users can subscribe or unsubscribe using the `/subscribe` and `/unsubscribe` commands.
- Subscriptions are stored in an SQLite database to send daily facts.

### 5. Scheduled Tasks
- The bot uses the `APScheduler` library to schedule the sending of daily facts to all subscribed users at 9:00 AM (Asia/Kolkata timezone).
- The scheduler runs in the background and handles the timely delivery of content.

## Example Usage
### 1. Starting the Bot
```
User: /start
Bot: 🤖 Welcome to the Fun Fact & Trivia Bot! 🎉
     Use /fact for a random fact.
     Use /today for historical facts.
     Use /number [number] for number trivia.
     Use /quote - for motivational quote.
     Use /quiz for a fun quiz.
     Use /subscribe to get daily facts.
     Use /unsubscribe to stop receiving daily facts.
```

### 2. Fetching a Random Fact
```
User: /fact
Bot: 💡 The average person walks the equivalent of three times around the world in a lifetime.
```

### 3. Getting Today's Historical Fact
```
User: /today
Bot: 📅 On this day in 1989, the Berlin Wall fell, marking the end of the Cold War.
```

### 4. Subscribing to Daily Facts
```
User: /subscribe
Bot: You've subscribed to daily facts! 🎉
```

### 5. Unsubscribing
```
User: /unsubscribe
Bot: You've unsubscribed from daily facts. 😢
```

## Create Telegram Bot
- To Get detailded infomation about starting creating [**Telegram**](https://telegram.org/) Bot visit [**Create Telegram Bot**](https://github.com/abhijit-003/How-to-Create-Telegram-Bot)
## Installation & Deployment

### Prerequisites
- Python 3.x
- Telegram Bot Token (create one using [@BotFather](https://t.me/BotFather))
- [Railway](https://railway.app/) or any other deployment platform
- necessary [requirements](https://github.com/abhijit-003/Fun-Fact-TelifyMeBot-bot/blob/main/requirements.txt)

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file with the following content:
```
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

### 4. Run the Bot Locally
```bash
python bot.py
```

### 5. Deploy on Railway
- Push your code to GitHub.
- Connect your GitHub repository to [Railway](https://railway.app/).
- Add your environment variable (`TELEGRAM_BOT_TOKEN`) in the Railway dashboard.
- Deploy your project.

## Future Improvements
- Add support for inline queries.
- Expand the database to store user preferences.
- Implement additional categories for trivia and facts.
- Add support for multimedia content to enhance user engagement.

## Contributing
Feel free to contribute to the project by opening issues or submitting pull requests.

## License
This project is licensed under the MIT License.

## Acknowledgements
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/en/stable/)
- [Numbers API](http://numbersapi.com)
- [Open Trivia Database](https://opentdb.com/)
- [Quotable API](http://api.quotable.io/)
- [Byabbe API](https://byabbe.se/on-this-day/)

---

Happy chatting with your new Telegram bot! 🎉
