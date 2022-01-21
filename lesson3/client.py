import sys
import json
import socket
import time
from variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT

from base_commands import get_message, send_message


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
        return data

    @staticmethod
    def response_analyze(msg):
        if 'response' in msg:
            if msg['response'] == 200:
                return '200 : OK'
            return f'400 : {msg["error"]}'
        raise ValueError

    @classmethod
    def base(cls):
        # client.py 192.168.1.2 8079
        try:
            server_address = sys.argv[1]
            server_port = int(sys.argv[2])
            if server_port < 1024 or server_port > 65535:
                raise ValueError
        except IndexError:
            server_address = cls.host
            server_port = cls.port
        except ValueError:
            print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
            sys.exit(1)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_address, server_port))
        message_to_server = cls.get_presence()
        send_message(s, message_to_server)
        try:
            answer = cls.response_analyze(get_message(s))
            print(answer)
        except (ValueError, json.JSONDecodeError):
            print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    Client.base()
