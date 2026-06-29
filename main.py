import os
import telebot
import requests

TG_TOKEN = os.environ.get('TELEGRAM_TOKEN')
DIFY_KEY = os.environ.get('DIFY_API_KEY')
DIFY_URL = os.environ.get('DIFY_API_URL', 'https://api.dify.ai/v1/chat-messages')

bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    headers = {
        'Authorization': f'Bearer {DIFY_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "inputs": {},
        "query": message.text,
        "response_mode": "blocking",
        "user": str(message.from_user.id)
    }
    try:
        response = requests.post(DIFY_URL, json=payload, headers=headers)
        data = response.json()
        answer = data.get('answer', 'Ошибка: Dify не вернул текст.')
        bot.reply_to(message, answer)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")

if __name__ == '__main__':
    print("Басеке запущен и слушает Telegram...")
    bot.infinity_polling()
