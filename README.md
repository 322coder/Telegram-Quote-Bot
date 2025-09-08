# 🤖 Telegram Quote Bot

Простой Telegram-бот на Python, который умеет:
- Отправлять случайную цитату по команде `/quote`.
- Добавлять новые цитаты по команде `/addquote`(только для админов).
- Посмотреть статистику по команде `/stats`.
- Отвечать приветствием на `/start`.
- Также доступны Inline кнопки для данных команд.

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
    BOT_TOKEN = "YOUR_TOKEN"
5. Вставить ID для прав администратора в bot.py:
    ADMIN_IDS = [IDs]
   (не обязательно, можно закоментировать)

## ▶️ Запуск
    python bot.py
## После запуска откройте Telegram и напишите своему боту команды:
    /start — приветствие
    /quote — случайная цитата
    /addquote — добавить свою цитату (для админов)
    /stats - посмотреть статистику

## 🖼️ Пример работы
![5330031234853764434](https://github.com/user-attachments/assets/c09cc881-79a6-40a2-b662-f40915f50a23)
![5330031234853764432](https://github.com/user-attachments/assets/d13a4194-8b1d-49a9-ab9c-8c601bf87f98)
![5330031234853764433](https://github.com/user-attachments/assets/25652d4d-2c8e-417d-b739-b519bf4c236d)

