-- 1. Top 5 Funds by Highest 3-Year Return
SELECT amfi_code, return_3yr, expense_ratio 
FROM fact_performance 
ORDER BY return_3yr DESC 
LIMIT 5;

-- 2. Average NAV per Month
SELECT amfi_code, strftime('%Y-%m', date) AS month, AVG(nav) AS avg_nav 
FROM fact_nav 
GROUP BY amfi_code, month;

-- 3. Total Transaction Volume by Type
SELECT transaction_type, COUNT(*) AS total_count, SUM(amount) AS total_amount 
FROM fact_transactions 
GROUP BY transaction_type;

-- 4. Transactions Grouped by State
SELECT state, COUNT(*) AS txn_count, SUM(amount) AS state_volume 
FROM fact_transactions 
GROUP BY state 
ORDER BY state_volume DESC;

-- 5. Schemes with Expense Ratio < 1.0%
SELECT amfi_code, expense_ratio 
FROM fact_performance 
WHERE expense_ratio < 1.0;

-- 6. Total Monthly SIP Inflows
SELECT strftime('%Y-%m', transaction_date) AS month, SUM(amount) AS total_sip 
FROM fact_transactions 
WHERE transaction_type = 'SIP' 
GROUP BY month;

-- 7. Distribution of KYC Status
SELECT kyc_status, COUNT(*) AS investor_count 
FROM fact_transactions 
GROUP BY kyc_status;

-- 8. Top 5 Single Highest Transactions
SELECT transaction_id, investor_id, amfi_code, amount, transaction_type 
FROM fact_transactions 
ORDER BY amount DESC 
LIMIT 5;

-- 9. Latest NAV for Each Scheme
SELECT amfi_code, nav, MAX(date) AS latest_date 
FROM fact_nav 
GROUP BY amfi_code;

-- 10. Summary Metrics
SELECT 
    COUNT(DISTINCT investor_id) AS total_investors,
    COUNT(transaction_id) AS total_transactions,
    SUM(amount) AS total_volume,
    AVG(amount) AS avg_transaction_value
FROM fact_transactions;
