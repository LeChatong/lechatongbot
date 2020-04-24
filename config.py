TOKEN = '914995992:AAFPpnVKjnG6lFcmF5FUctkjN7HtKVQrugA'
NGROK_URL = 'https://da810a1c.ngrok.io'
BASE_TELEGRAM_URL = 'https://api.telegram.org/bot{}'.format(TOKEN)
LOCAL_WEBHOOK_ENDPOINT = '{}/webhook'.format(NGROK_URL)
TELEGRAM_INIT_WEBHOOK_URL = '{}/setWebhook?url={}'.format(BASE_TELEGRAM_URL, LOCAL_WEBHOOK_ENDPOINT)
TELEGRAM_SEND_MESSAGE_URL = BASE_TELEGRAM_URL + '/sendMessage?chat_id={}&text={}'
API_KEY_MOVIE = 'f972c58efb26ab0a5e82cda1f7352586'
URI_LOCAL = 'http://172.16.145.118:8000'
URI_ONLINE = 'https://lechatonguniverse.herokuapp.com'