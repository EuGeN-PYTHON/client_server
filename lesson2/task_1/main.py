"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений или другого инструмента извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""

import glob
import re
import csv
from copy import deepcopy

list_row = []
list_files_txt = []
data_list = []
headers = ['Изготовитель системы:', 'Windows ', 'Код продукта:', 'Тип системы:']

def get_file_txt():
    for file in glob.glob("*.txt"):
        list_files_txt.append(file)

def get_data():
    data_list.append(deepcopy(headers))
    for i in range(len(list_files_txt)):
        file = open(list_files_txt[i])
        data = file.read()
        list_row = []
        for j in range(len(headers)):
            reg_exp = fr'{headers[j]}\s*\S*'
            re_string = re.compile(reg_exp)
            compile_text = re_string.findall(data)[0]
            last_prob = len(compile_text) - compile_text[::-1].find(' ')
            list_row.append(compile_text[last_prob:])
            if i == 0:
                data_list[0][j] = data_list[0][j][:len(headers[j])-1]
        data_list.append(list_row)
    return data_list


def write_to_csv():
    get_file_txt()

    with open('data_report.csv', 'w') as f_n:
        F_N_WRITER = csv.writer(f_n, quoting=csv.QUOTE_NONNUMERIC)
        data_for_csv = get_data()
        for row in data_for_csv:
            F_N_WRITER.writerow(row)


write_to_csv()