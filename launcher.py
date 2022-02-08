import subprocess
import time

PROCESS = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen('python3 server.py', shell=True))
        for i in range(2):
            time.sleep(0.5)
            PROCESS.append(subprocess.Popen('gnome-terminal -- python3 client.py -m send', shell=True))
        for i in range(2):
            time.sleep(0.5)
            PROCESS.append(subprocess.Popen('gnome-terminal -- python3 client.py -m listen', shell=True))
    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
