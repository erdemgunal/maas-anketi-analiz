import pandas as pd
import json


CSV_PATH = "/Users/erdemgunal/Desktop/salary_analysis_project/data/2025_cleaned_data.csv"


def compute_avg_salary_by_level_and_location() -> dict:
    df = pd.read_csv(CSV_PATH)

    # Seniority name from ordinal
    level_map = {1: "Junior", 2: "Mid", 3: "Senior", 4: "Staff", 5: "Team Lead", 6: "Architect"}
    if "seniority_level_ic" not in df.columns:
        raise KeyError("'seniority_level_ic' column not found in cleaned dataset")
    df["level_name"] = df["seniority_level_ic"].map(level_map)

    # Infer company location label from one-hot columns
    def infer_loc(row):
        if row.get("company_location_Turkiye", 0) == 1:
            return "Türkiye"
        if row.get("company_location_Avrupa", 0) == 1:
            return "Avrupa"
        if row.get("company_location_Amerika", 0) == 1:
            return "Amerika"
        return None

    df["company_location_label"] = df.apply(infer_loc, axis=1)

    # Filter is_manager == 0 and target levels
    if "is_manager" not in df.columns:
        raise KeyError("'is_manager' column not found in cleaned dataset")
    target_levels = ["Junior", "Mid", "Senior"]
    target_locs = ["Türkiye", "Avrupa", "Amerika"]

    filtered = df[(df["is_manager"] == 0) & (df["level_name"].isin(target_levels))]

    result = {}
    for lvl in target_levels:
        lvl_dict = {}
        for loc in target_locs:
            mask = (filtered["level_name"] == lvl) & (filtered["company_location_label"] == loc)
            series = filtered.loc[mask, "salary_numeric"]
            lvl_dict[loc] = float(series.mean()) if not series.empty else None
        result[lvl] = lvl_dict
    return result


def main() -> None:
    res = compute_avg_salary_by_level_and_location()
    # print(json.dumps(res, indent=4))
    # {
    #     "Junior": {
    #         "Türkiye": 52.42908827785818,
    #         "Avrupa": 112.16666666666667,
    #         "Amerika": 102.72222222222223
    #     },
    #     "Mid": {
    #         "Türkiye": 80.60634146341464,
    #         "Avrupa": 130.7325581395349,
    #         "Amerika": 130.5
    #     },
    #     "Senior": {
    #         "Türkiye": 124.60147058823529,
    #         "Avrupa": 194.3372093023256,
    #         "Amerika": 180.9
    #     }
    # }

if __name__ == "__main__":
    main()