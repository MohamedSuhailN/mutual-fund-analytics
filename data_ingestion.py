import glob
import os
import pandas as pd


def explore_all_raw_csvs():
    print("================ 1. CSV DATASETS OVERVIEW ================")
    csv_files = glob.glob("data/raw/*.csv")

    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        print(f"\n--- Checking File: {file_name} ---")
        try:
            df = pd.read_csv(file_path)
            print(f"Shape (Rows, Columns): {df.shape}")
            print("Data Types:\n", df.dtypes)
            print("First 2 Rows:\n", df.head(2))
            print("Missing Values:\n", df.isnull().sum())
        except Exception as e:
            print(f"Error reading {file_name}: {e}")


def validate_fund_master_and_amfi():
    print("\n================ 2. FUND MASTER & AMFI VALIDATION ================")

    # Handle prefixed file names (01_fund_master.csv, 02_nav_history.csv)
    master_path = (
        "data/raw/01_fund_master.csv"
        if os.path.exists("data/raw/01_fund_master.csv")
        else "data/raw/fund_master.csv"
    )
    history_path = (
        "data/raw/02_nav_history.csv"
        if os.path.exists("data/raw/02_nav_history.csv")
        else "data/raw/nav_history.csv"
    )

    if not os.path.exists(master_path) or not os.path.exists(history_path):
        print("Note: Could not find fund master or nav history CSV files.")
        return

    fund_master = pd.read_csv(master_path)
    nav_history = pd.read_csv(history_path)

    # Print unique master fields
    for col in ["fund_house", "category", "sub_category", "risk_grade"]:
        if col in fund_master.columns:
            print(f"Unique {col}: {fund_master[col].unique()}")

    # AMFI Code Validation
    if (
        "scheme_code" in fund_master.columns
        and "scheme_code" in nav_history.columns
    ):
        master_codes = set(fund_master["scheme_code"].unique())
        history_codes = set(nav_history["scheme_code"].unique())

        missing_codes = master_codes - history_codes

        print("\n--- DATA QUALITY SUMMARY ---")
        if missing_codes:
            print(
                f"WARNING: Found {len(missing_codes)} scheme codes in fund_master missing from nav_history."
            )
        else:
            print(
                "SUCCESS: All AMFI scheme codes in fund_master exist in nav_history!"
            )


if __name__ == "__main__":
    explore_all_raw_csvs()
    validate_fund_master_and_amfi()
