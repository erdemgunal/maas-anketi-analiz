"""
XGBoost Maaş Tahmin CLI

Kullanım:
  - JSON ile bireysel tahmin:
      python -m src.predict --json '{"yas":27, "Toplam kaç yıllık iş deneyimin var?":3, "Frontend_React":1, ...}'

  - Eğitim feature şemasını gör:
      python -m src.predict --print-schema

Notlar:
  - Model, eğitimde `data/cleaned_data.csv` içindeki sayısal sütunlar ("salary_normalized" ve "Timestamp" hariç) ile eğitildi.
  - Eksik feature'lar 0 ile doldurulur.
  - Örnek JSON: {"yas":27, "Toplam kaç yıllık iş deneyimin var?":3, "Frontend_React":1, "Hangi_JavaScript":1, "Hangi seviyedesin?":2}
"""

from __future__ import annotations

import argparse
import json
import os
from typing import List

import joblib
import numpy as np
import pandas as pd


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")


def load_training_feature_names(cleaned_data_path: str) -> List[str]:
    """
    Eğitimde kullanılan feature isimlerini (sayısal sütunlar) çıkarır.
    """
    df = pd.read_csv(cleaned_data_path)
    numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    if "salary_normalized" in numerical_columns:
        numerical_columns.remove("salary_normalized")
    if "Timestamp" in numerical_columns:
        numerical_columns.remove("Timestamp")
    if "Aylık ortalama net kaç bin TL alıyorsun?" in numerical_columns:
        numerical_columns.remove("Aylık ortalama net kaç bin TL alıyorsun?")
    return numerical_columns


def align_features(df: pd.DataFrame, feature_names: List[str]) -> pd.DataFrame:
    """
    Giriş verisini eğitim şemasına uyarlar: sıra sabitlenir, eksikler 0 ile doldurulur.
    """
    aligned = df.copy()
    # Sadece eğitimdeki feature'lar
    aligned = aligned.reindex(columns=feature_names, fill_value=0)
    # Sayısala çevir (geçersizler NaN olur, sonra 0 ile doldur)
    aligned = aligned.apply(pd.to_numeric, errors="coerce").fillna(0)
    return aligned





def predict_from_json(model_path: str, json_str: str, cleaned_data_path: str) -> float:
    model = joblib.load(model_path)
    feature_names = load_training_feature_names(cleaned_data_path)

    try:
        payload = json.loads(json_str)
        if not isinstance(payload, dict):
            raise ValueError("JSON tek bir obje olmalı (dict)")
    except json.JSONDecodeError as e:
        raise ValueError(f"Geçersiz JSON: {e}")

    df_in = pd.DataFrame([payload])
    X = align_features(df_in, feature_names)
    pred = float(model.predict(X)[0])
    return pred


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="XGBoost maaş tahmin aracı")
    parser.add_argument("--model-path", default=os.path.join(MODELS_DIR, "xgboost.joblib"), help="Model dosya yolu")
    parser.add_argument("--cleaned-data", default=os.path.join(DATA_DIR, "cleaned_data.csv"), help="Eğitimdeki temiz veri yolu (şema için)")
    parser.add_argument("--print-schema", action="store_true", help="Eğitimde kullanılan feature isimlerini yazdır ve çık")
    parser.add_argument("--json", required=True, help="Bireysel tahmin için JSON girdi")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.print_schema:
        features = load_training_feature_names(args.cleaned_data)
        print("Eğitim feature'ları (sıralı):")
        for name in features:
            print(name)
        return

    pred = predict_from_json(
        model_path=args.model_path,
        json_str=args.json,
        cleaned_data_path=args.cleaned_data,
    )
    print(f"Tahmin edilen maaş (bin TL): {pred:.2f}")


if __name__ == "__main__":
    main()