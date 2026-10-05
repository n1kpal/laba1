import csv
from pathlib import Path

# Столбцы, которые по условию есть в каждом файле датасета
REQUIRED_COLUMNS = ["message_id", "channel", "created_at", "message"]


def load_dataset(path):
    """
    Загружает датасет сообщений из CSV-файла.

    Принимает:
        path (str | Path): путь к CSV-файлу. Может быть относительным
            ("data/04_bronirovanie_i_meropriyatiya.csv") или абсолютным
            ("C:/lab1/04_bronirovanie_i_meropriyatiya.csv").

    Делает:
        - превращает путь в абсолютный (относительный считается от
          текущей рабочей папки);
        - проверяет, что файл существует;
        - читает файл в кодировке utf-8-sig (она убирает BOM, с которым
          сохранены файлы), разделитель - запятая;
        - проверяет, что в файле есть все ожидаемые столбцы.

    Возвращает:
        list[dict]: список записей. Одна запись = одно сообщение, словарь
            {"message_id": ..., "channel": ..., "created_at": ...,
             "message": ...}. Все значения - строки (так читает csv).

    Бросает:
        FileNotFoundError: если файла нет.
        ValueError: если в файле не хватает нужных столбцов.
    """
    # Path понимает оба вида путей; resolve() делает путь абсолютным
    file_path = Path(path).expanduser().resolve()

    if not file_path.is_file():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    # newline="" нужен модулю csv, чтобы переносы строк внутри
    # сообщений не ломали разбор
    with open(file_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=",")
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"В файле нет столбцов: {missing}")
        return list(reader)


def describe_dataset(rows):
    """
    Первичный анализ датасета (критерий 1: столбцы, типы, пропуски, объём).

    Принимает:
        rows (list[dict]): результат load_dataset.

    Делает:
        - считает число записей и уникальных message_id;
        - для каждого столбца определяет тип значений и число пустых;
        - печатает отчёт в консоль.

    Возвращает:
        dict: {"rows": число записей, "columns": список столбцов,
               "types": {столбец: тип}, "missing": {столбец: число пустых},
               "unique_ids": число уникальных message_id}
    """
    columns = list(rows[0].keys()) if rows else []

    # Пустым считаем None или строку из одних пробелов
    missing = {c: sum(1 for r in rows if not (r[c] or "").strip()) for c in columns}
    # csv отдаёт всё строками, поэтому у всех столбцов будет тип str
    types = {c: type(rows[0][c]).name for c in columns}

    info = {
        "rows": len(rows),
        "columns": columns,
        "types": types,
        "missing": missing,
        "unique_ids": len({r["message_id"] for r in rows}),
    }

    print(f"Записей: {info['rows']} (уникальных message_id: {info['unique_ids']})")
    print(f"Столбцы: {columns}")
    print(f"Типы: {types}")
    print(f"Пропуски: {missing}")
    return info


if __name__ == "__main__":
    #Запуск
    data = load_dataset("04_bronirovanie_i_meropriyatiya.csv")
    describe_dataset(data)
    print(data[0])