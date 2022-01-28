"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

first_word = 'разработка'
second_word = 'администрирование'
third_word = 'protocol'
fourth_word = 'standard'

list_bites = []
for word in [first_word, second_word, third_word, fourth_word]:
    list_bites.append(word.encode('utf-8'))

print(list_bites)

list_str = []
for wordb in list_bites:
    list_str.append(wordb.decode('utf-8'))

print(list_str)
