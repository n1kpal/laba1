import re

Entity_patterns = {

# \d - это цифра. \d+ - одна или более цифр. \d{4} - четыре цифры
# - - дефис. [a-zA-Z0-9._%+-]+ - штуки этого формата в размере одного и более символа
# (?:\+7|8) - или +7, или 8. [\s().-]* - здесь разрешаются пробелы, скобки, точки и дефис.


    "URL": ( # Ссылки
        r'\b(?:https?://|www\.)'
        r'[^\s|]+'
    ),
    "EMAIL": ( # Электронная почта
        r'[a-zA-Z0-9._%+-]+'
        r'@'
        r'[a-zA-Z0-9.-]+'
        r'\.'
        r'[a-zA-Z]{2,}'
    ),
    "PHONE": ( # Телефонные номера
        r'(?<!\d)(?:\+7|8)'
        r'(?:[\s().-]*\d){10}'
        r'(?!\d)' #после этого ещё цифр быть не должно
    ),
    "DATE": ( # Даты
        r'\b(?:'
        r'\d{4}-\d{2}-\d{2}' # XXXX-XX-XX
        r'|' # ИЛИ
        r'\d{2}[./-]\d{2}[./-]\d{2,4}' # XX(./-)XX(./-)XX[XX]. () - что-то из этого, [] - необязательно
        r')\b'
    ),
    "PRICE": ( # Цены
        r'(?<!\w)' # \w - слово. ?<! - Перед числом не должно быть символа слова.
        r'\d+(?:[ \u00a0]\d{3})*' #число цены. (?:[ \u00a0]\d{3})*. разрешены пробел и \u00a0(неразрывный пробел). между ними могут быть ровно три цифры. * - значит блок может вообще не выполниться
        r'(?:[.,]\d+)?' # копейки. ? в конце - этот кусок может выполниться 1 или 0 раз
        r'\s*' # необязательный пробел между числом и валютой
        r'(?:₽|RUB|руб(?:\.|лей|ля|ль)?|р\b)' #валюта
    )
}

Entity_regex = re.compile (
    "|".join(
        f"(?P<{name}>{pattern})"
        for name, pattern in Entity_patterns.items()
    ),
    re.IGNORECASE
)

def find_entities(text):
    tokens = []
    entities = {
        "URL": [],
        "EMAIL": [],
        "PHONE": [],
        "DATE": [],
        "PRICE": []
    }

    replacements = []

    for match in Entity_regex.finditer(text):
        entity_type = match.lastgroup
        value = match.group(entity_type)

        if entity_type == "URL":
            value = value.rstrip(".,;:!?)]}*")

        start = match.start()
        end = start + len(value)

        tokens.append({
            "type": entity_type,
            "value": value,
            "start": start,
            "end": end
        })

        entities[entity_type].append(value)

        replacements.append(
            (start, end, f"[{entity_type}]")
        )

    result = []
    position = 0
    for start, end, replacement in replacements:
        result.append(text[position:start])
        result.append(replacement)
        position = end
    result.append(text[position:])
    new_text = "".join(result)

    return tokens, entities, new_text


if __name__ == "__main__":
    text = """
        🙂 ЦЕНА номера ИЗМЕНИЛАСЬ после подтверждения брони. цена: 1 290 руб. / нужно на 2026-08-26 / URL= https://www.event-book.ru/support/8?from=mail
    """

    tokens, entities, new_text = find_entities(text)

    print("=== ТОКЕНЫ ===")
    for token in tokens:
        print(token)

    print("=== СЛОВАРЬ ===")
    print(entities)

    print("=== ИЗМЕНЁННЫЙ ТЕКСТ ===")
    print(new_text)