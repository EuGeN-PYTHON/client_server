import socket
import sys
import json
from variables import MAX_CONNECTIONS, DEFAULT_PORT
from base_commands import get_message, send_message


class Server:
    conn = MAX_CONNECTIONS
    port = DEFAULT_PORT

    def __init__(self, conn=conn, port=port):
        self.conn = conn
        self.port = port

    @staticmethod
    def check_data_client(msg):

        if 'action' in msg and msg['action'] == 'presence' and 'time' in msg and \
                'user' in msg and msg['user']['account_name'] == 'Guest':
            return {'response': 200}
        return {
            'response': 400,
            'error': 'Bad Request'
        }

    @classmethod
    def base(cls):
        # server.py -p 8079 -a 192.168.1.2
        try:
            if '-p' in sys.argv:
                input_port = int(sys.argv[sys.argv.index('-p') + 1])
            else:
                input_port = cls.port
            if input_port < 1024 or input_port > 65535:
                raise ValueError
        except IndexError:
            print('После параметра -\'p\' необходимо указать номер порта.')
            sys.exit(1)
        except ValueError:
            print(
                'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
            sys.exit(1)

        try:
            if '-a' in sys.argv:
                address_ip = sys.argv[sys.argv.index('-a') + 1]
            else:
                address_ip = ''
        except IndexError:
            print(
                'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
            sys.exit(1)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((address_ip, input_port))
        s.listen(MAX_CONNECTIONS)

        while True:
            client, client_address = s.accept()
            try:
                message_from_client = get_message(client)
                print(message_from_client)
                response = cls.check_data_client(message_from_client)
                send_message(client, response)
                client.close()
            except (ValueError, json.JSONDecodeError):
                print('Принято некорретное сообщение от клиента.')
                client.close()


if __name__ == '__main__':
    Server.base()
