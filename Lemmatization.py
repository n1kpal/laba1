import pymorphy3
morph = pymorphy3.MorphAnalyzer()
def lemmatize_word(word: str) -> str:
    word = word.strip().lower()
    if not word:
        return ""
    parsed = morph.parse(word)[0]
    return parsed.normal_form
"""
Почему именно pymorphy? Всё просто
Я рассмотрел несколько вариантов решения задачи лемматизации и понял,
что варианта всего 3:
1) Использовать библиотеку pymorphy (Оптимально)
2) Вручную создать словарь и позже обращаться к нему (Требует большой подготовки, слишком затратен для поставленной задачи)
3) Написать скрипт по удалению стандартных окончаний (Возможны ошибки, что снизит качество обработки данных)

Ниже привожу пример скрипта 3:
def lemmatize_naive(word: str) -> str:
    word = word.strip().lower()
    
    # Грубые правила отсечения (для примера)
    if word.endswith("ами") or word.endswith("ями"):
        return word[:-3]# (очень упрощенно)
    if word.endswith("ой") or word.endswith("ей"):
        return word[:-2] + "ый"
    if word.endswith("ет") or word.endswith("ёт"):
        return word[:-2] + "еть"
    if word.endswith("ут") or word.endswith("ют"):
        return word[:-2] + "ть"
        
    return word # Если не подошло ни одно правило

print(lemmatize_naive("бежал")) # Вернет "бежал" (алгоритм слишком простой, не поймет)
print(lemmatize_naive("кошек")) # Вернет "кошек" 
print(lemmatize_naive("ноутбуками")) #Вернет "ноутбук", НО
print(lemmatize_naive("сами")) #Вернет "с", что не верно!

Как следствие было принято решение писать функцию через pymorphy
"""