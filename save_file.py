# Задание 9. Сохранение результата в clean_messages.csv


import json
import csv


def save_records(records, output_path="clean_messages.csv"):
    '''
    Принимает список словарей (по одному на каждое сообщение),
    которые вернула функция field_formation() из задания 7,
    и сохраняет их в CSV-файл clean_messages.csv.

    :param records: список словарей с полями original_text, urls,
                    phones, emails, dates, prices, anonymized_text,
                    clean_text, tokens, lemmas
    :param output_path: путь к выходному файлу (по умолчанию
                        clean_messages.csv в текущей папке)
    '''
    # порядок колонок в CSV — как в примере из методички
    fieldnames = [
        "original_text",
        "urls",
        "phones",
        "emails",
        "dates",
        "prices",
        "anonymized_text",
        "clean_text",
        "tokens",
        "lemmas",
    ]

    ''' 
    открываем файл на запись:
    "w"             — перезаписываем, если файл уже есть
    "utf-8-sig"     — UTF-8 с BOM, чтобы Excel показал русский текст
    newline=""      — чтобы не было пустых строк между записями на Windows
    '''
    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()  # первая строка — названия колонок

        for rec in records:
            row = {}
            for key in fieldnames:
                value = rec.get(key, "")
                '''
                CSV не умеет хранить списки/словари,
                поэтому упаковываем их в JSON-строку.
                ensure_ascii=False — чтобы кириллица не превратилась
                в \u043a\u0443... и читалась глазами
                '''
                if isinstance(value, (list, dict)):
                    row[key] = json.dumps(value, ensure_ascii=False)
                else:
                    row[key] = value
            writer.writerow(row)

    print(f"[save_records] Сохранено {len(records)} записей в {output_path}")


'''
Как вызывать (из общего main()):
records = []
   for row in df["text"].fillna(""):
       # ... вызовы функций других этапов ...
       field = field_formation(original_text, anonymized_text,
                              clean_text, tokens, lemmas, entities_dict)
      records.append(field)

   save_records(records, "clean_messages.csv")
'''