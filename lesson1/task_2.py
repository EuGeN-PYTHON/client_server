"""
Задание 2.

Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя!!! методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""

first_word = 'class'
second_word = 'function'
third_word = 'method'

for word in [first_word, second_word, third_word]:
    wordb = eval(f'b"{word}"')
    print('Тип = ', type(wordb), '; ', wordb, '; Длинна = ', len(wordb))