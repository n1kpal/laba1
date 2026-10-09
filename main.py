from open_file import load_dataset, describe_dataset
from clean_text import lowercase_and_clean, delete_entities
from entity_extractor import find_entities
from Lemmatization import lemmatize_words
from text_analysis import get_tokens, count_words
from field_formation import field_formation
from save_file import save_records

# Массив содержащий исходный датасет
data: list[dict] = load_dataset("04_bronirovanie_i_meropriyatiya.csv")
describe_dataset(data)
print()

# Массив содержащий обработанный датасет
res: list[dict] = list()

# Словари со статистикой слов до и после удаления стоп слов
words_dict_befor: dict[str: int] = dict()
words_dict_after: dict[str: int] = dict()

# Подсчет до удаления стоп слов
for i in range(len(data)):
    clean_text = lemmatize_words(lowercase_and_clean(data[i]["message"]).split())
    count_words(words_dict_befor, set(clean_text))
a = sorted(words_dict_befor.keys(), key=lambda x: words_dict_befor[x], reverse=True)

for i in range(len(data)):
    # Приведение к нижнему регистру и удаление спец сиволы
    clean_text = lowercase_and_clean(data[i]["message"])
    # Нахождение сущностей и обезличивание
    _, entities, anonymized_text = find_entities(clean_text)
    # Удаление [PHONE], [PRICE] и т. д.
    clean_text = delete_entities(anonymized_text)
    # Токенизация и подсчет
    tokens = get_tokens(clean_text)
    count_words(words_dict_after, set(lemmatize_words(tokens)))
    # Леммматизация
    lemmas = lemmatize_words(tokens.copy())
    # Формирование резултирующего датасета
    res.append(field_formation(
        data[i]["message"],
        anonymized_text,
        clean_text,
        tokens.copy(),
        lemmas.copy(),
        entities.copy()
    ))

# Вывод 20 самых частовстречаемых слов после удаления стоп слов
b = sorted(words_dict_after.keys(), key=lambda x: words_dict_after[x], reverse=True)[:20]

print("top 20 before")
for i in range(20):
    print(f"    {i + 1}) {a[i]}: {words_dict_befor[a[i]]}")
print()

print("top 20 after")
for i in range(20):
    print(f"    {i + 1}) {b[i]}: {words_dict_after[b[i]]}")

# Сохранение датасета в csv файл
save_records(res)