from flask import Flask, request
import os
from config import API_KEY_MOVIE, TOKEN, WEBHOOK_URL, URI_ONLINE

from telebot import types
import telebot
import time
import requests

last_cmd = []
knownUsers = []
userStep = {}
commands = {  # Liste des Commandes
    'start'     :   'Affiche Un Message de Bienvenue et propose les choix',
    'help'      :   'Afficher l\'aide',
    'movies'    :   'Rechercher un film',
    'series'     :   'Rechercher une serie ou un anime',
    'stop'      :   'Stopper le bot'
}

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL+TOKEN)
    return 'ok', 200

@app.route('/'+TOKEN, methods=['POST'])
def getMessage():
    udapte = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([udapte])
    return 'ok', 200

@bot.message_handler(commands=['start'])
def command_start(message):
    chatId = message.chat.id
    last_cmd.insert(0, '')

    bot.send_chat_action(chatId, 'typing')
    time.sleep(1)

    markup = types.ReplyKeyboardMarkup()
    itembtna = types.InlineKeyboardButton('/movies',)
    itembtnv = types.KeyboardButton('/series')
    markup.row(itembtna, itembtnv)
    if chatId not in knownUsers:
        knownUsers.append(chatId)
        userStep[chatId] = 0
        bot.send_message(chat_id=message.chat.id, text="Bienvenue {}\n"
                                                   "Faite votre choix".format(message.from_user.first_name),
                     reply_markup=markup)
    else:
        bot.send_message(chat_id=message.chat.id, text="Ravie de vous revoir {}\n"
                                                       "Faite votre choix".format(message.from_user.first_name),
                         reply_markup=markup)

    #bot.reply_to(message, "Bienvenue {}".format(bot.get_me().first_name))

@bot.message_handler(commands=['help'])
def command_help(message):
    chatId = message.chat.id
    last_cmd.insert(0, '')
    bot.send_chat_action(chatId, 'typing')
    time.sleep(1)
    help_text = "L'ensemble des commandes suivantes sont valide : \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    help_text += "\n Cet bot a été crée par @lechatong"
    bot.send_message(chatId, help_text)

@bot.message_handler(commands=['stop'])
def command_stop(message):
    chatId = message.chat.id
    last_cmd.insert(0, '')
    bot.send_message(chat_id=chatId, text="Merci d'avoir utilisé ce bot ! \n"
                                          "Au revoir !")
    #bot.stop_bot()

@bot.message_handler(commands=['movies'])
def command_movies(message):
    chatId = message.chat.id
    last_cmd.insert(0, '')
    last_cmd.insert(0,'movies')
    bot.send_chat_action(chatId, 'typing')
    time.sleep(1)
    bot.send_message(chat_id=chatId, text="Recherchez un film en saisissant son Titre")

@bot.message_handler(commands=['series'])
def command_series(message):
    chatId = message.chat.id
    last_cmd.insert(0,'')
    last_cmd.insert(0,'series')
    bot.send_chat_action(chatId, 'typing')
    time.sleep(1)
    bot.send_message(chat_id=chatId, text="Recherchez une serie ou un anime en saisissant son Titre")

@bot.message_handler(func=lambda message:  last_cmd[0] == 'movies')
def command_search_movie(message):
    chatId = message.chat.id
    bot.send_chat_action(chatId, 'typing')
    time.sleep(1)
    response_movie = requests.get(
        URI_ONLINE+'/fr/lechapi/search_movies/?query='+message.text)
    list_movie = response_movie.json()
    if len(list_movie) != 0:
        for movie in list_movie:
            bot.send_message(chat_id=chatId, text=movie['link_download'])
        bot.send_message(chat_id=chatId, text="Saisissez de nouveau un titre pour trouver un film")
    else:
        bot.send_message(chat_id=chatId, text="Aucun élément trouvé !"
                                              "\n"
                                              "\n"
                                              "Veuillez saisir un autre titre")
    #last_cmd.clear()

@bot.message_handler(func=lambda message: last_cmd[0] == 'series')
def command_search_serie(message):
    chatId = message.chat.id
    response_serie = requests.get(
        URI_ONLINE + '/fr/lechapi/search_series/?query=' + message.text)
    list_serie = response_serie.json()
    if len(list_serie) != 0:
        for serie in list_serie:
            markup = types.InlineKeyboardMarkup()
            response_tv = requests.get(
                'https://api.themoviedb.org/3/tv/' + str(serie['id_tv']) + '?api_key=' + API_KEY_MOVIE + '&language=fr-FR')
            tv = response_tv.json()
            markup.add(types.InlineKeyboardButton('EPISODE DISPONIBLE', url=URI_ONLINE + '/fr/tv/details/' + str(serie['id_tv'])))
            bot.send_message(chat_id=chatId, text=tv['name'], reply_markup=markup)
        bot.send_message(chat_id=chatId, text="Saisissez de nouveau un titre pour trouver une série ou un anime")
    else:
        bot.send_message(chat_id=chatId, text="Aucun élément trouvé !"
                                              "\n"
                                              "\n"
                                              "Veuillez saisir un autre titre")
    #last_cmd.clear()

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    chatId = message.chat.id
    bot.send_message(chat_id=chatId, text="Ceci n'est pas une commande.\n"
                                                   "Veuillez consulter la liste des commandes ici /help")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
