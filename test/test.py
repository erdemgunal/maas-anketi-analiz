import pandas as pd
import json
from collections import Counter

def count_languages(csv_path: str) -> dict:
    df = pd.read_csv(csv_path)
    # Split by comma, strip whitespace, drop empties, count frequencies
    split_series = (
        df['Hangi programlama dillerini kullanıyorsun']
        .dropna()
        .astype(str)
        .str.split(',')
    )

    language_counter: Counter = Counter()
    for languages in split_series:
        for language in languages:
            cleaned = language.strip()
            if cleaned:
                language_counter[cleaned] += 1

    return dict(language_counter)


def count_one_hot_programming(csv_path: str) -> dict:
    df = pd.read_csv(csv_path)
    programming_columns = [c for c in df.columns if c.startswith('programming_')]

    counts: dict = {}
    for column_name in programming_columns:
        # Coerce non-numeric to NaN, fill as 0, cast to int, then sum
        column_sum = (
            pd.to_numeric(df[column_name], errors='coerce')
            .fillna(0)
            .astype(int)
            .sum()
        )
        counts[column_name] = int(column_sum)

    return counts


if __name__ == "__main__":
    free_text_counts = count_languages('data/2025_maas_anket.csv')
    one_hot_counts = count_one_hot_programming('data/2025_cleaned_data.csv')
    print(json.dumps({
        'free_text_counts': free_text_counts,
        'one_hot_counts': one_hot_counts,
    }, indent=4, ensure_ascii=False))