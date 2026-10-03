import re
from collections import Counter
file_name = '04_bronirovanie_i_meropriyatiya.csv'

stops = {
    'и', 'в', 'во', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она',
    'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только',
    'ее', 'мне', 'было', 'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему', 'теперь',
    'когда', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни', 'быть', 'был',
    'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом', 'себя',
    'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы',
    'тебя', 'их', 'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже',
    'себе', 'под', 'будет', 'ж', 'тогда', 'кто', 'этот', 'того', 'потому', 'этого', 'какой',
    'не', 'были', 'мой', 'ценой', 'это', 'очень', 'просто', 'из-за', 'чтобы', 'хотя'
}

# очищает текст от урлов, почт и прочей ебени
def get_tokens(text):
    txt_clean = text.lower()

    txt_clean = re.sub(r'https?://\S+|www\.\S+', '', txt_clean)
    txt_clean = re.sub(r'\S+@\S+', '', txt_clean)
    txt_clean = re.sub(r'\d+[:.-]\d+[:.-]\d+|\d+[:.-]\d+', '', txt_clean)

    clean_words = re.findall(r'[а-яА-Яa-zA-Z_]+', txt_clean)

    final_tokens = []
    for w in clean_words:
        if w not in stops and len(w) > 1:
            final_tokens.append(w)

    return final_tokens

# вывод топ 20 до и после отчистки
def show_top_20(title, words_list):
    top_data = Counter(words_list).most_common(20)

    print(title)
    for num, (w, count) in enumerate(top_data, 1):
        print(f"{num}. {w}: {count}")
    print()

words_1 = []
words_2 = []

with open(file_name, mode='r', encoding='utf-8-sig') as f:
    for line in f:
        txt = line.strip()
        if not txt:
            continue

        raw_words = re.findall(r'\w+', txt.lower())
        for w in raw_words:
            words_1.append(w)

        tokens = get_tokens(txt)
        for w in tokens:
            words_2.append(w)

show_top_20("до отчистки:", words_1)
show_top_20("после:", words_2)