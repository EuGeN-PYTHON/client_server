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


# @Log()
class Client:
    host = DEFAULT_IP_ADDRESS
    port = DEFAULT_PORT

    def __init__(self, host=host, port=port):
        self.host = host
        self.port = port

    @staticmethod
    def message_from_server(message):
        if 'action' in message and message['action'] == 'message' and \
                'sender' in message and 'mess_text' in message:
            print(f"Получено сообщение от пользователя {message['sender']}:\n{message['mess_text']}")
            client_log.info(f"Получено сообщение от пользователя {message['sender']}:\n{message['mess_text']}")
        else:
            client_log.error(f'Получено некорректное сообщение с сервера: {message}')


    @staticmethod
    def create_message(sock, account_name='Guest'):
        message = input('Введите сообщение для отправки или \'q\' для завершения работы: ')
        if message == 'q':
            sock.close()
            client_log.info('Завершение работы по команде пользователя.')
            print('Спасибо за использование нашего сервиса!')
            sys.exit(0)
        message_dict = {
            'action': 'message',
            'time': time.time(),
            'account_name': account_name,
            'mess_text': message
        }
        client_log.debug(f'Сформирован словарь сообщения: {message_dict}')
        return message_dict

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
        # client.py -a 192.168.1.2 -p 8079 -m listen/send

        if '-a' in sys.argv:
            server_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            server_address = DEFAULT_IP_ADDRESS
        if '-p' in sys.argv:
            server_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            server_port = DEFAULT_PORT
        if '-m' in sys.argv:
            client_mode = sys.argv[sys.argv.index('-m') + 1]
        else:
            client_mode = 'listen'

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
        except json.JSONDecodeError:
            client_log.error('Не удалось декодировать полученную Json строку.')
            sys.exit(1)
        except ConnectionRefusedError:
            client_log.critical(
                f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                f'конечный компьютер отверг запрос на подключение.')
            sys.exit(1)
        else:
            if client_mode == 'send':
                print('Режим работы - отправка сообщений.')
            else:
                print('Режим работы - приём сообщений.')
            while True:
                if client_mode == 'send':
                    try:
                        send_message(s, cls.create_message(s))
                    except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                        client_log.error(f'Соединение с сервером {server_address} было потеряно.')
                        sys.exit(1)

                if client_mode == 'listen':
                    try:
                        cls.message_from_server(get_message(s))
                    except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                        client_log.error(f'Соединение с сервером {server_address} было потеряно.')
                        sys.exit(1)


if __name__ == '__main__':
    clnt = Client()
    clnt.base()
