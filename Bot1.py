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
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url(api)
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url


def dog(update,context):
    url = get_image_url('https://random.dog/woof.json')
    chat_id = update.message['chat']['id']
    context.bot.send_message(chat_id=chat_id, text='Вот тебе собачка')
    context.bot.send_photo(chat_id=chat_id, photo=url)


def cat(update,context):
    url = get_image_url('https://api.thecatapi.com/v1/images/search')
    chat_id = update.message['chat']['id']
    context.bot.send_message(chat_id=chat_id, text='Вот тебе котик')
    context.bot.send_photo(chat_id=chat_id, photo=url)


def listen(update, context):
    chat_id = update.message['chat']['id']
    context.bot.send_message(chat_id=chat_id, text=update.message['text'])
    context.bot.forward_message(chat_id=230512694, from_chat_id=chat_id, message_id=update.message['message_id'])


def food(update,context):
    recipe_link = []
    url = 'https://www.yummly.com/recipes'
    r = requests.get(url)

    recipe_link = []
    url = 'https://www.yummly.com/recipes'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features='lxml')
    recipe_list = soup.find_all(href=re.compile("/recipe/"))  # Поиск через регулярку
    for item in recipe_list:
        recipe_link.append(item.get('href'))

    url = 'https://www.yummly.com' + recipe_link[random.randint(0, len(recipe_link))]
    link_answ=url
    # url='https://www.yummly.com/recipe/Melt-In-Your-Mouth-Baked-Chicken-Breasts-9073095'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features='lxml')
    recipe_name_answ = soup.find('h1', {'class': 'recipe-title font-bold h2-text primary-dark'}).text  # Название рецепта
    ingredients_list = soup.find_all('li', {'class': 'IngredientLine'})  # Список ингредиентов
    ingredients_answ = ''
    for ingr in ingredients_list:
        ingredients_answ += (ingr.text+'\n')

    url += '?makeMode=true'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features='lxml')
    steps = soup.find_all('div', {'class': 'step-text h4-text'})  # Шаги приготовления
    steps_answ = ''
    for (offset, step) in enumerate(steps):
        steps_answ += ('Step ' + str(offset + 1) + ': ' + str(step.text) + '\n' + '\n')

    chat_id = update.message['chat']['id']
    context.bot.send_message(chat_id=chat_id, text='Вот тебе рецепт чего-то вкусненького')
    context.bot.send_message(chat_id=chat_id, text=recipe_name_answ)
    context.bot.send_message(chat_id=chat_id, text=link_answ)
    context.bot.send_message(chat_id=chat_id, text=ingredients_answ)
    context.bot.send_message(chat_id=chat_id, text=steps_answ)


def main():
    updater = Updater('869686653:AAGXT2cDZHEDpGZ0u67YOxag7pP0YmpvtWw', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('dog', dog))
    dp.add_handler(CommandHandler('cat', cat))
    dp.add_handler(CommandHandler('food', food))
    dp.add_handler(MessageHandler(Filters.text, listen))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
