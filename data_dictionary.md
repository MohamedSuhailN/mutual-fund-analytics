# Mutual Fund Analytics — Data Dictionary

## 1. dim_fund
Master metadata for mutual fund schemes.
| Column | Data Type | Description | Source |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | Unique scheme identifier | `01_fund_master.csv` |
| `scheme_name` | TEXT | Name of the mutual fund scheme | `01_fund_master.csv` |
| `fund_house` | TEXT | Asset Management Company | `01_fund_master.csv` |
| `category` | TEXT | Asset Class (Equity, Debt, Hybrid) | `01_fund_master.csv` |
| `sub_category` | TEXT | Specific fund type | `01_fund_master.csv` |
| `risk_category`| TEXT | Risk rating level | `01_fund_master.csv` |

## 2. fact_nav
Historical daily Net Asset Value (NAV) records.
| Column | Data Type | Description | Source |
| :--- | :--- | :--- | :--- |
| `nav_id` | INTEGER | Auto-increment primary key | Generated |
| `amfi_code` | INTEGER | Foreign key referencing `dim_fund` | `02_nav_history.csv` |
| `date` | TEXT | Date of NAV (YYYY-MM-DD) | `02_nav_history.csv` |
| `nav` | REAL | Net Asset Value (NAV > 0) | `02_nav_history.csv` |

## 3. fact_transactions
Investor buying and selling transaction records.
| Column | Data Type | Description | Source |
| :--- | :--- | :--- | :--- |
| `transaction_id`| TEXT | Unique transaction identifier | `08_investor_transactions.csv` |
| `investor_id` | TEXT | Unique investor identifier | `08_investor_transactions.csv` |
| `amfi_code` | INTEGER | Foreign key referencing `dim_fund` | `08_investor_transactions.csv` |
| `transaction_type`| TEXT | Enum: (`SIP`, `Lumpsum`, `Redemption`) | `08_investor_transactions.csv` |
| `amount` | REAL | Value of transaction in INR | `08_investor_transactions.csv` |
| `transaction_date`| TEXT | Date of transaction | `08_investor_transactions.csv` |
| `kyc_status` | TEXT | Enum: (`Verified`, `Pending`, `Rejected`) | `08_investor_transactions.csv` |
| `state` | TEXT | State location of investor | `08_investor_transactions.csv` |

## 4. fact_performance
Performance and expense metrics per fund scheme.
| Column | Data Type | Description | Source |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | Foreign key referencing `dim_fund` | `07_scheme_performance.csv` |
| `return_1yr` | REAL | Annualized 1-year percentage return | `07_scheme_performance.csv` |
| `return_3yr` | REAL | Annualized 3-year percentage return | `07_scheme_performance.csv` |
| `return_5yr` | REAL | Annualized 5-year percentage return | `07_scheme_performance.csv` |
| `expense_ratio`| REAL | Annual management fee percentage | `07_scheme_performance.csv` |
