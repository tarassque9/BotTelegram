from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
import requests
import json
import re

#Bot hosted on pythonanywhere.com he's name: TarasRumbambarchikxxx
#Bot have comands: /bitcoin and /etherium
#You can use this commands in any context. Example: Price /bitcoin?

app = Flask(__name__)
sslify = SSLify(app)

URL = 'https://api.telegram.org/bot<token TgBot>/'
cmc_token = '<token Coinmarkets>'



def write_json(data, filename='answer.json'):
     with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def send_message(chat_id, text='KU KU KU KU KU'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


def parse_text(text):
    pattern = r'/\w+'
    crypto = re.search(pattern, text).group()
    if crypto == '/bitcoin':
        crypto = 'BTC'
    elif crypto == '/etherium':
        crypto = 'ETH'
    return crypto


def get_price(crypto):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {'symbol': crypto, 'convert': 'USD'}
    headers = {'X-CMC_PRO_API_KEY': cmc_token }
    r = requests.get(url, headers=headers, params=params).json()
    price = r['data'][crypto]['quote']['USD']['price']
    return price


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        pattern = r'/\w+'

        if re.search(pattern, message):
                price = get_price(parse_text(message))
                send_message(chat_id, text=price)
        return jsonify(r)
    return '<h1> ku ku ku ku ku</h1>'

if __name__ == '__main__':
        app.run()
