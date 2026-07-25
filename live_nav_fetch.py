import os
import requests
import pandas as pd

# List of mutual fund scheme codes required by the task
SCHEMES = {
    "125497": "HDFC_Top_100_Direct",
    "119551": "SBI_Bluechip",
    "120503": "ICICI_Bluechip",
    "118632": "Nippon_Large_Cap",
    "119092": "Axis_Bluechip",
    "120841": "Kotak_Bluechip",
}


def fetch_and_save_nav(scheme_code, fund_name):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        nav_data = data.get("data", [])

        # Convert JSON response to Pandas DataFrame
        df = pd.DataFrame(nav_data)
        df["scheme_code"] = scheme_code
        df["scheme_name"] = data.get("meta", {}).get("scheme_name", fund_name)

        # Save into data/raw/ directory
        os.makedirs("data/raw", exist_ok=True)
        file_path = f"data/raw/nav_{scheme_code}_{fund_name}.csv"
        df.to_csv(file_path, index=False)
        print(f"Successfully fetched and saved: {file_path}")
    else:
        print(
            f"Failed to fetch data for {scheme_code}: Status {response.status_code}"
        )


if __name__ == "__main__":
    for code, name in SCHEMES.items():
        fetch_and_save_nav(code, name)
