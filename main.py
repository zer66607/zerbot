import requests

from config import help_msg, start_msg
from settings import token


class zerBot:

    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)
        self.api_coin_url = 'https://api.cryptonator.com/api/ticker'
        self.commands = {
            'start': '/start',
            'help': '/help',
            'btc': '/btc',
            'eth': '/eth'
        }

    def get_all_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, message):
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': message}
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_coin(self, ticker):
        tick = requests.get(self.api_coin_url + ticker + '-usd')
        tick_json = tick.json()['ticker']
        return tick_json

    def parse_last_update(self, last_update, msg):
        last_chat_id = last_update[msg]['chat']['id']
        last_chat_name = last_update[msg]['chat']['first_name']

        if 'text' in last_update[msg]:
            last_chat_text = last_update[msg]['text']
        else:
            last_chat_text = self.commands['help']
        resp = {'id': last_chat_id,
                'name': last_chat_name, 'text': last_chat_text}
        # logs
        print('user: ' + last_chat_name)
        print('message: ' + last_chat_text)
        return resp

    def create_message(self, last_chat):
        if last_chat['text'] == self.commands['start']:
            msg = 'Приветствую тебя, ' + last_chat['name'] + start_msg

        elif last_chat['text'] == self.commands['btc']:
            coin = float(bot.get_coin('/btc')['price'])
            coin = "${0:.3f}".format(coin)
            msg = last_chat['name'] + ', курс Биткойна равен ' + coin

        elif last_chat['text'] == self.commands['eth']:
            coin = float(bot.get_coin('/eth')['price'])
            coin = "${0:.3f}".format(coin)
            msg = last_chat['name'] + ', курс Эфириума равен ' + coin

        elif last_chat['text'] == self.commands['help']:
            msg = help_msg

        else:
            msg = last_chat['name'] + \
                ', к сожалению, таких команд я не понимаю!'

        return msg


bot = zerBot(token)


def main():
    new_offset = None

    while True:
        all_update = bot.get_all_updates(new_offset)

        if all_update != []:

            for last_update in all_update:

                last_update_id = last_update['update_id']

                if 'message' in last_update:
                    last_chat = bot.parse_last_update(
                        last_update, 'message')

                elif 'edited_message' in last_update:
                    last_chat = bot.parse_last_update(
                        last_update, 'edited_message')
                # print(last_chat)

                message = bot.create_message(last_chat)
                bot.send_message(last_chat['id'], message)

            new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
