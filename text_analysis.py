import re
from collections import Counter
from Lemmatization import lemmatize_word
file_name = '04_bronirovanie_i_meropriyatiya.csv'

stops = {
    'и', 'в', 'во', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'весь', 'она',
    'так', 'тот', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только',
    'она', 'мы', 'быть', 'вот', 'от', 'я', 'ещё', 'нет', 'о', 'из', 'он', 'теперь',
    'когда', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'не', 'ни', 'до', 'вы',
    'нибудь', 'опять', 'уж', 'ведь', 'там', 'потом', 'себя', 'ничего', 'мочь', 'они',
    'тут', 'где', 'есть', 'надо', 'для', 'ты', 'их', 'чем', 'сам', 'чтобы', 'без',
    'будто', 'что', 'раз', 'тоже', 'под', 'ж', 'тогда', 'кто', 'этот', 'потому', 'какой',
    'мой', 'это', 'очень', 'просто', 'из-за', 'хотя', 'страница', 'смотреть', 'номер',
    'телефон', 'звонить', 'почта', 'ссылка', 'ответить', 'подсказать', 'хотеть',
    'можно', 'один', 'мы', 'нужно', 'после', 'привет', 'здравствуйте', 'email', 'mail',
    'yandex', 'gmail', 'ru', 'com', 'url', 'https', 'http', 'www', 'hotel', 'demo',
    'tickets', 'example', 'event', 'book', 'сумма', 'стоимость', 'цена', 'рубль',
    'rub', 'дата', 'оформить', 'списать'
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
        if lemmatize_word(w) not in stops and len(w) > 1:
            final_tokens.append(w)

    return final_tokens

# подсчет слов
def count_words(dict, words_set):
    for word in words_set:
        if not word.isalpha():
            continue
        if word in dict:
            dict[word] += 1
        else:
            dict[word] = 1

# вывод топ 20 до и после отчистки
def show_top_20(title, words_list):
    top_data = Counter(words_list).most_common(20)

    print(title)
    for num, (w, count) in enumerate(top_data, 1):
        print(f"{num}. {w}: {count}")
    print()


if __name__ == "__main__":
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