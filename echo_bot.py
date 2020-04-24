from config import API_KEY_MOVIE, TOKEN, URI_LOCAL, URI_ONLINE
from telebot import types
import telebot
import time
import requests

bot = telebot.TeleBot(TOKEN)

knownUsers = []

userStep = {}

last_cmd = []

commands = {  # Liste des Commandes
    'start'     :   'Affiche Un Message de Bienvenue et propose les choix',
    'help'      :   'Afficher l\'aide',
    'movies'    :   'Rechercher un film',
    'series'     :   'Rechercher une serie ou un anime',
    'stop'      :   'Stopper le bot'
}

class TeleBot:

    @bot.message_handler(commands=['start'])
    def command_start(message):
        chatId = message.chat.id
        ####################################################################
        last_cmd.append('start')
        ####################################################################
        bot.send_chat_action(chatId, 'typing')
        time.sleep(3)
        markup = types.ReplyKeyboardMarkup()
        itembtna = types.InlineKeyboardButton('/movies',)
        itembtnv = types.KeyboardButton('/series')

        markup.row(itembtna, itembtnv)
        bot.send_message(chat_id=message.chat.id, text="Bienvenue {}\n"
                                                       "Faite votre choix".format(message.from_user.first_name),
                         reply_markup=markup)

        #bot.reply_to(message, "Bienvenue {}".format(bot.get_me().first_name))

    @bot.message_handler(commands=['movies'])
    def command_movies(message):
        chatId = message.chat.id
        last_cmd.append('movies')
        bot.send_message(chat_id=chatId, text="Recherchez un film en saisissant son Titre")

    @bot.message_handler(commands=['series'])
    def command_series(message):
        chatId = message.chat.id
        last_cmd.append('series')
        bot.send_message(chat_id=chatId, text="Recherchez une serie ou un anime en saisissant son Titre")

    @bot.message_handler(func=lambda message: last_cmd[-1] == 'movies')
    def command_search_movie(message):
        chatId = message.chat.id
        last_cmd.append('')
        response_movie = requests.get(
            URI_ONLINE+'/fr/lechapi/search_movies/?query='+message.text)
        list_movie = response_movie.json()
        if len(list_movie) != 0:
            for movie in list_movie:
                bot.send_message(chat_id=chatId, text=movie['link_download'])
        else:
            bot.send_message(chat_id=chatId, text="Aucun élément trouvé !")

    @bot.message_handler(func=lambda message: last_cmd[-1] == 'series')
    def command_search_serie(message):
        chatId = message.chat.id
        last_cmd.append('')
        response_serie = requests.get(
            URI_ONLINE + '/fr/lechapi/search_series/?query=' + message.text)
        list_serie = response_serie.json()
        if len(list_serie) != 0:
            for serie in list_serie:
                markup = types.InlineKeyboardMarkup()
                response_tv = requests.get(
                    'https://api.themoviedb.org/3/tv/' + str(serie['id_tv']) + '?api_key=' + API_KEY_MOVIE + '&language=fr-FR')
                tv = response_tv.json()
                markup.add(types.InlineKeyboardButton('Episode Disponible', url=URI_ONLINE + '/fr/tv/details/' + str(serie['id_tv'])))
                bot.send_message(chat_id=chatId, text=tv['name'], reply_markup=markup)
        else:
            bot.send_message(chat_id=chatId, text="Aucun élément trouvé !")

    #def show_tv_episode(chatID, tvID):
    #    response_eps = requests.get(
    #        URI_LOCAL+ '/fr/lechapi/series/id/?id_tv=' + tvID)
    #    list_eps = response_eps.json()
    #    for eps in list_eps:
    #        bot.send_message(chat_id=chatID, text=eps['link_download'])

    @bot.message_handler(commands=['help'])
    def command_help(message):
        chatId = message.chat.id
        last_cmd.append('help')
        help_text = "L'ensemble des commandes suivantes sont valide : \n"
        for key in commands:
            help_text += "/" + key + ": "
            help_text += commands[key] + "\n"
        help_text += "\n Cet bot a été crée par @lechatong"
        bot.send_message(chatId, help_text)

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        chatId = message.chat.id
        bot.send_message(chat_id=chatId, text="Ceci n'est pas une commande.\n"
                                                       "Veuillez consulter la liste des commandes ici /help")

    bot.polling()