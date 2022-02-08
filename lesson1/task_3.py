"""
Задание 3.

Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b'' (без encode decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- обязательно!!! усложните задачу, "отловив" и обработав исключение,
придумайте как это сделать
"""

first_word = 'attribute'
second_word = 'класс'
third_word = 'функция'
fourth_word = 'type'

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

for word in [first_word, second_word, third_word, fourth_word]:
    if is_ascii(word):
        # wordb = bytes(word, 'ascii')
        wordb = eval(f'b"{word}"')
        print(type(wordb), word)
    else:
        print(f'{word} - Невозможно без декодирования/кодирования записать в байтовом типе')
