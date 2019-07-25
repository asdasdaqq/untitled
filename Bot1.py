from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import requests
import re
import random
from lxml import html
from bs4 import BeautifulSoup


def get_url(api):
    if 'woof' in api:
        contents = requests.get(api).json()
        url = contents['url']
    else:
        contents = requests.get(api).json()[0]
        url = contents['url']
    return url


def get_image_url(api):
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url(api)
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url


def dog(bot, update):
    url = get_image_url('https://random.dog/woof.json')
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='Вот тебе собачка')
    bot.send_photo(chat_id=chat_id, photo=url)


def cat(bot, update):
    url = get_image_url('https://api.thecatapi.com/v1/images/search')
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='Вот тебе котик')
    bot.send_photo(chat_id=chat_id, photo=url)


def listen(bot,update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=update.message.text)
    bot.forward_message(chat_id=230512694,from_chat_id=chat_id,message_id=update.message.message_id)

def food(bot,update):
    recipe_link = []
    url = 'https://www.yummly.com/recipes'
    r = requests.get(url)
    with open('test.html', 'w', encoding='utf-8') as output_file:
        output_file.write(r.text)

    with open('test.html', encoding='utf-8') as input_file:
        text = input_file.read()

    soup = BeautifulSoup(text, features='lxml')
    recipe_list = soup.find_all('div', {'class': 'recipe-card-img'})
    for item in recipe_list:
        recipe_link.append(item.get('data-pin-url'))

    answ=recipe_link[random.randint(0, len(recipe_link))]
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='Вот тебе рецепт чего-то вкусненького')
    bot.send_message(chat_id=chat_id, text=answ)


def main():
    updater = Updater('869686653:AAGXT2cDZHEDpGZ0u67YOxag7pP0YmpvtWw')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('dog', dog))
    dp.add_handler(CommandHandler('cat', cat))
    dp.add_handler(CommandHandler('food', food))
    dp.add_handler(MessageHandler(Filters.text,listen))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
