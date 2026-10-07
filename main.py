from open_file import load_dataset, describe_dataset
from clean_text import lowercase_and_clean, delete_entities
from entity_extractor import find_entities
from Lemmatization import lemmatize_words
from text_analysis import get_tokens, show_top_20
from field_formation import field_formation
from save_file import save_records

data = load_dataset("04_bronirovanie_i_meropriyatiya.csv")
describe_dataset(data)

res: list[dict] = list()

print()
for i in range(len(data)):
    clean_text = lowercase_and_clean(data[i]["message"])
    _, entities, anonymized_text = find_entities(clean_text)
    clean_text = delete_entities(anonymized_text)

    print(data[i]["message_id"])
    show_top_20("TOP-20 befor clean: ", clean_text.split())
    tokens = get_tokens(clean_text)
    show_top_20("TOP-20 after clean: ", tokens)
    print()
    print()

    lemmas = lemmatize_words(tokens.copy())

    res.append(field_formation(
        data[i]["message"],
        anonymized_text,
        clean_text,
        tokens.copy(),
        lemmas.copy(),
        entities.copy()
    ))

save_records(res)