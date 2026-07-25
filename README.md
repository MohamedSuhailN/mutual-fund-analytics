Mutual Fund Analytics

A data pipeline and analytics workspace for ingesting, processing, and analyzing Indian Mutual Fund datasets and live AMFI NAV historical data.



\--- Repository Structure



mutual-fund-analytics/

├── data/

│   ├── raw/          # Raw local CSV datasets \& live NAV downloads

│   └── processed/    # Cleaned \& transformed datasets

├── notebooks/        # Jupyter notebooks for exploratory data analysis

├── sql/              # Database schema \& SQL queries

├── dashboard/        # BI dashboard files \& assets

├── reports/          # Analysis reports \& summaries

├── .gitignore

├── README.md

├── requirements.txt

├── live\_nav\_fetch.py

└── data\_ingestion.py

