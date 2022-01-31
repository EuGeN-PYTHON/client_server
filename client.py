import logging
import sys
import json
import socket
import time
import os

from variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT
from log_deco import Log
from base_commands import get_message, send_message

sys.path.append(os.path.join(os.getcwd(), '..'))
from log import client_log_config


client_log = logging.getLogger('client_app')


@Log()
class Client:
    host = DEFAULT_IP_ADDRESS
    port = DEFAULT_PORT

    def __init__(self, host=host, port=port):
        self.host = host
        self.port = port

    @staticmethod
    def get_presence(account_name='Guest'):
        data = {
            'action': 'presence',
            'time': time.time(),
            'user': {
                'account_name': account_name
            }
        }
        client_log.debug(f'Создано сообщение presence для пользователя: {account_name}')
        return data

    @staticmethod
    def response_analyze(msg):
        client_log.debug(f'Соответствие сообщения от сервера: {msg}')
        if 'response' in msg:
            if msg['response'] == 200:
                return '200 : OK'
            return f'400 : {msg["error"]}'
        raise ValueError

    @classmethod
    def base(cls):
        # client.py 192.168.1.2 8079

        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            client_log.critical(f'Невозможно войти с'
                                f' номером порта: {server_port}. '
                                f'Допустимы порты с 1024 до 65535. Прервано.')
            sys.exit(1)

        client_log.info(f'Запущен клиент с парам.: {server_address}, порт: {server_port}')

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server_address, server_port))
            message_to_server = cls.get_presence()
            send_message(s, message_to_server)
            answer = cls.response_analyze(get_message(s))
            client_log.info(f'Принят ответ от сервера {answer}')
            # print(answer)
        except (ValueError, json.JSONDecodeError):
            client_log.error('Не удалось декодировать полученную Json строку.')
            # print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    clnt = Client()
    clnt.base()
