import pandas as pd
# import json
# from collections import Counter

# def count_languages(csv_path: str) -> dict:
#     df = pd.read_csv(csv_path)
#     # Split by comma, strip whitespace, drop empties, count frequencies
#     split_series = (
#         df['Hangi programlama dillerini kullanıyorsun']
#         .dropna()
#         .astype(str)
#         .str.split(',')
#     )

#     language_counter: Counter = Counter()
#     for languages in split_series:
#         for language in languages:
#             cleaned = language.strip()
#             if cleaned:
#                 language_counter[cleaned] += 1

#     return dict(language_counter)


# def count_one_hot_programming(csv_path: str) -> dict:
#     df = pd.read_csv(csv_path)
#     programming_columns = [c for c in df.columns if c.startswith('programming_')]

#     counts: dict = {}
#     for column_name in programming_columns:
#         # Coerce non-numeric to NaN, fill as 0, cast to int, then sum
#         column_sum = (
#             pd.to_numeric(df[column_name], errors='coerce')
#             .fillna(0)
#             .astype(int)
#             .sum()
#         )
#         counts[column_name] = int(column_sum)

#     return counts


# if __name__ == "__main__":
#     free_text_counts = count_languages('data/2025_maas_anket.csv')
#     one_hot_counts = count_one_hot_programming('data/2025_cleaned_data.csv')
#     print(json.dumps({
#         'free_text_counts': free_text_counts,
#         'one_hot_counts': one_hot_counts,
#     }, indent=4, ensure_ascii=False))


def print_calisma_sekli_for_yurtdisi_tr_hub(csv_path: str) -> None:
    df = pd.read_csv(csv_path, encoding='utf-8', encoding_errors='ignore')
    if 'Şirket lokasyon' not in df.columns or 'Çalışma şekli' not in df.columns:
        missing = [c for c in ['Şirket lokasyon', 'Çalışma şekli'] if c not in df.columns]
        raise KeyError(f"Eksik kolon(lar): {', '.join(missing)}. Dosya: {csv_path}")

    mask = df['Şirket lokasyon'] == 'Yurtdışı TR hub'
    values = df.loc[mask, 'Çalışma şekli']

    print('Filtre: Şirket lokasyon == "Yurtdışı TR hub"')
    print('\nÇalışma şekli değerleri:')
    if values.dropna().empty:
        print('(Kayıt bulunamadı)')
    else:
        print(values.dropna().to_string(index=False))

    print('\nDağılım (value_counts):')
    if values.dropna().empty:
        print('(Boş)')
    else:
        print(values.dropna().value_counts().to_string())


if __name__ == "__main__":
    print_calisma_sekli_for_yurtdisi_tr_hub('data/2025_maas_anket.csv')