# 🤖 Telegram Quote Bot

Простой Telegram-бот на Python, который умеет:
- Отправлять случайную цитату по команде `/quote`.
- Добавлять новые цитаты по команде `/addquote`.
- Посмотреть статистику по команде `/stats`.
- Отвечать приветствием на `/start`.

## 🚀 Технологии
- [Python 3.9+](https://www.python.org/downloads/)
- [aiogram](https://docs.aiogram.dev/)

## 📦 Установка
1. Клонировать репозиторий:
   git clone https://github.com/322coder/Telegram-Quote-Bot

2. Установить зависимости:
    Введите в консоль:
    pip install aiogram

3. Создать бота через @BotFather в Telegram и получить токен.

4. Вставить токен в bot.py:
    TOKEN = "Ваш_токен"

## ▶️ Запуск
    python bot.py
  После запуска откройте Telegram и напишите своему боту команды:
    /start — приветствие
    /quote — случайная цитата
    /addquote — добавить свою цитату
    /stats - посмотреть статистику

