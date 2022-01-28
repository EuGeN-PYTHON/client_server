import socket
import sys
import json
import logging
from log import server_log_config
from variables import MAX_CONNECTIONS, DEFAULT_PORT
from base_commands import get_message, send_message

app_log = logging.getLogger('server_app')


class Server:
    conn = MAX_CONNECTIONS
    port = DEFAULT_PORT

    def __init__(self, conn=conn, port=port):
        self.conn = conn
        self.port = port

    @staticmethod
    def check_data_client(msg):
        app_log.debug(f'проверка сообщения от клиента: {msg}')
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
        listen_server = int(sys.argv[sys.argv.index('-a') + 1])
        if '-p' in sys.argv:
            input_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            input_port = cls.port
        if input_port < 1024 or input_port > 65535:
            app_log.critical(f'Невозможно войти с'
                             f' номером порта: {input_port}. '
                             f'Допустимы порты с 1024 до 65535. Прервано.')
            sys.exit(1)
        app_log.info(f'Запущен сервер с порта: {input_port}, сообщения принимаются с адреса: {listen_server}')

        try:
            if '-a' in sys.argv:
                address_ip = listen_server
            else:
                address_ip = ''
        except IndexError:
            app_log.critical(
                'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
            sys.exit(1)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((address_ip, input_port))
        s.listen(MAX_CONNECTIONS)

        while True:
            client, client_address = s.accept()
            app_log.info(f'Установлено соедение с адресом: {client_address}')
            try:
                message_from_client = get_message(client)
                app_log.debug(f'Получено сообщение {message_from_client}')
                # print(message_from_client)
                response = cls.check_data_client(message_from_client)
                app_log.info(f'создан ответ {response}')
                send_message(client, response)
                client.close()
                app_log.debug(f'Соединение с {client_address} закрыто.')
            except (ValueError, json.JSONDecodeError):
                app_log.error(f'Принято некорретное сообщение от клиента:{client_address}')
                client.close()


if __name__ == '__main__':
    Server.base()
