import re

# Принемает str отчищает от спецсимволов (но не ломает URL адреса) и делает все буквы строчными
# Возвращает строку
def lowercase_and_clean(text: str) -> str:
    text = text.lower().split()
    LETTERS_AND_DIGITS = set("abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789")

    words = list()

    for i in range(len(text)):
        flag = True
        for j in range(len(text[i])):
            if text[i][j] in LETTERS_AND_DIGITS:
                flag = False
                break

        if text[i][:2] == "+7":
            words.append(text[i])
            continue

        if flag:
            continue
        
        for k in range(len(text[i]) - 1, -1, -1):
            if text[i][k] in LETTERS_AND_DIGITS:
                break
        
        words.append(text[i][j:k+1])

    return ' '.join(words)

# принимет строку и возвращает строку без [PHONE] и т. п.
def delete_entities(text: str) -> str:
    text = re.sub(r"\[[^\]]*\]", "", text)
    text = re.sub(r" +", ' ', text)

    return text
