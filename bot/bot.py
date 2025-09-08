import logging
import random
import sqlite3
from pathlib import Path

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# Конфигурация
BOT_TOKEN = "YOUR_TOKEN"
DB_FILE = "quotes.db"
ADMIN_IDS = [123456789]

# Настройка логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

class QuoteDatabase:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self._init_db()

    def _init_db(self):
        """Инициализирует базу данных"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quotes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    author TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def get_random_quote(self) -> dict:
        """Возвращает случайную цитату"""
        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1")
            row = cursor.fetchone()
            return dict(row) if row else {"text": "Цитаты пока не добавлены!", "author": "Бот"}

    def add_quote(self, text: str, author: str = "Неизвестный автор") -> bool:
        """Добавляет новую цитату"""
        if not text.strip(): return False
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO quotes (text, author) VALUES (?, ?)", (text.strip(), author.strip()))
            conn.commit()
            return cursor.rowcount > 0

    def get_stats(self) -> dict:
        """Возвращает статистику по цитатам"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM quotes")
            total = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(DISTINCT author) as authors FROM quotes")
            authors = cursor.fetchone()[0]
            return {"total": total, "authors": authors}

# Инициализация базы данных
db = QuoteDatabase(DB_FILE)

def format_quote(quote: dict) -> str:
    """Форматирует цитату"""
    return f"📜 *{quote['text']}*\n\n— _{quote['author']}_"

def create_main_keyboard():
    """Создает основную клавиатуру"""
    keyboard = [
        [InlineKeyboardButton("🎲 Случайная цитата", callback_data="random_quote")],
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Обработчики команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ *Добро пожаловать в Цитатник!* ✨\n\nЯ помогу тебе найти вдохновение в мудрых словах.",
        reply_markup=create_main_keyboard(),
        parse_mode='Markdown'
    )

async def random_quote_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quote = db.get_random_quote()
    await update.message.reply_text(format_quote(quote), parse_mode='Markdown', reply_markup=create_main_keyboard())

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = db.get_stats()
    stats_text = f"📊 *Статистика:*\n\nЦитат: {stats['total']}\nАвторов: {stats['authors']}"
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def add_quote_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("❌ Только для администраторов")
        return
    if not context.args:
        await update.message.reply_text("Использование: /addquote \"Текст цитаты\" Автор")
        return
    
    text = " ".join(context.args)
    if '"' in text:
        parts = text.split('"')
        quote_text = parts[1].strip()
        author = " ".join(parts[2:]).strip() if len(parts) > 2 else "Неизвестный автор"
    else:
        quote_text, author = text, "Неизвестный автор"

    if db.add_quote(quote_text, author):
        await update.message.reply_text("✅ Цитата добавлена!")
    else:
        await update.message.reply_text("❌ Ошибка добавления")

# Обработчик кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "random_quote":
        quote = db.get_random_quote()
        await query.edit_message_text(format_quote(quote), parse_mode='Markdown', reply_markup=create_main_keyboard())
    elif data == "stats":
        stats = db.get_stats()
        stats_text = f"📊 *Статистика:*\n\nЦитат: {stats['total']}\nАвторов: {stats['authors']}"
        await query.edit_message_text(stats_text, parse_mode='Markdown', reply_markup=create_main_keyboard())

def main():
    """Запуск бота"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quote", random_quote_cmd))
    application.add_handler(CommandHandler("stats", stats_cmd))
    application.add_handler(CommandHandler("addquote", add_quote_cmd))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    logger.info("Бот запущен!")
    application.run_polling()

if __name__ == "__main__":

    main()
