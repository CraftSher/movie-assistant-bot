![Project Banner](data/banner.jpg)

![demo gif](data/MovieAssistantBot.gif)


# 🎬 Movie Assistant Telegram Bot

A Telegram bot that helps users find movies based on title, genre, rating, or keywords.  
Built with **Python 3.11**, **Aiogram 3.x**, and local movie data (JSON).

## 🔍 Features

- 🔤 Search by full or partial movie title
- 🎭 Filter by genre (e.g., Action, Comedy, Sci-Fi)
- ⭐ Filter by rating (e.g., 8.0+)
- 🧠 Keyword matching for intelligent search
- 📩 Clean, user-friendly Telegram interface
- 💬 `/start` and `/help` commands with usage instructions

## 🛠 Tech Stack

- **Python 3.11**
- **Aiogram 3.x** (Telegram bot framework)
- **JSON** for local movie database
- **Asyncio** for non-blocking execution

## 📦 Installation

```bash
git clone https://github.com/CraftSher/movie-assistant-bot.git
cd movie-assistant-bot
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

⚙️ Environment Setup
Create a .env file with your Telegram bot token:

```bash
BOT_TOKEN=your_telegram_bot_token
```

## ▶️ Usage

```bash
python bot/main.py
```

## 📁 Project Structure

```
MovieAssistantBot/
├── bot/                 # Main bot logic (handlers, routing, states)
├── data/                # JSON/movie dataset
├── database/            # (Optional) persistent storage if needed
├── screenshots/         # Screenshots for portfolio/README
├── .env                 # Environment variables (TOKEN, etc.)
├── .gitignore
├── README.md
├── requirements.txt
└── __init__.py
```

## 🔗 Demo
You can try the bot here (replace with your bot link):
https://github.com/CraftSher/movie-assistant-bot

## 📜 License
MIT License

## 👨‍💻 Author
Created by CraftSher
Portfolio-ready bot built for freelancing and real-world use.