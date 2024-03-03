import telebot
import requests
import json


API = 'your API key'
bot = telebot.TeleBot('your bot token')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет :)\nНапиши название города, погоду в котором хочешь узнать')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if weather.status_code == 200:
        data = json.loads(weather.text)
        bot.reply_to(message,
                     f'Сейчас в этом городе: \n{data["main"]["temp"]}C°\nОщущается как {data["main"]["feels_like"]}C°\nМинимальная температура: {data["main"]["temp_min"]}C°\nМаксимальная температура: {data["main"]["temp_max"]}C°\nСкорость ветра: {data["wind"]["speed"]}м/с\nВлажность воздуха: {data["main"]["humidity"]}%')
        temp = data["main"]["temp"]
        if temp > 9.0:
            image = 'sunny.jpg'
        elif 3.0 < temp < 9.0:
            image = 'osenb.jpg'
        else:
            image = 'snezhinka.jpg'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message,
                     f'{message.from_user.first_name}, Вы указали город неверно\nВведите корректное название города')

if __name__ == "__main__":
    bot.polling(none_stop=True, timeout = 123)

