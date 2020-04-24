import requests

from config import TELEGRAM_SEND_MESSAGE_URL


class TelegramBot:
    def __init__(self):
        self.chat_id = None
        self.text = None
        self.first_name = None
        self.last_name = None

    def parse_webhook_data(self, data):

        message = data['message']

        self.chat_id = message['chat']['id']
        self.incoming_message_text = message['text'].lower()
        self.first_name = message['from']['first_name']
        self.last_name =  message['from']['username']

    def action(self):

        success = None

        if self.incoming_message_text == '/hello':
            self.outgoing_message_text = 'Hello {}'.format(self.first_name)
            success = self.send_message()

        if self.incoming_message_text == '/start':
            self.outgoing_message_text = 'Welcome to LeChatongUniverse ! \n' \
                                         'Contact me to @lechatong'
            success = self.send_message()

        if self.incoming_message_text == '/searchmovies':
            self.outgoing_message_text = 'Saisissez le Titre d\'un film'
            success = self.send_message()


        return success

    def send_message(self):

        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self.chat_id, self.outgoing_message_text))

        return True if res.status_code == 200 else False

    @staticmethod
    def init_webhook(url):
        requests.get(url)