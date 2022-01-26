"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""
import yaml

data_for_yml = {'first': [1, 2, 3], 'second': 123, 'third': {'first': '123€'}}

with open('file.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(data_for_yml, file, allow_unicode=True, default_flow_style=False)

with open('file.yaml', 'r', encoding='utf-8') as file:
    data_from_yaml = yaml.load(file, Loader=yaml.SafeLoader)

print(data_for_yml==data_from_yaml)
