- 1. Total transactions per agency
SELECT a.agency_name, SUM(t.amount) AS total_amount
FROM transactions t
JOIN agencies a ON t.agency_id = a.agency_id
GROUP BY a.agency_name
ORDER BY total_amount DESC;

- 2. Average transaction per product
SELECT p.product_name, AVG(t.amount) AS avg_amount
FROM transactions t
JOIN products p ON t.product_id = p.product_id
GROUP BY p.product_name
ORDER BY avg_amount DESC;

-3. Monthly transactions
SELECT DATE_TRUNC('month', transaction_date) AS month,
       SUM(amount) AS total
FROM transactions
GROUP BY month
ORDER BY month;

-- 4. Clients with average transaction below global average
SELECT client_id
FROM accounts
WHERE account_id IN (
    SELECT account_id
    FROM transactions
    GROUP BY account_id
    HAVING AVG(amount) < (
        SELECT AVG(amount) FROM transactions
    )
);

- 5. Risk segmentation
SELECT c.segment,
       COUNT(t.transaction_id) AS total_transactions,
       SUM(CASE WHEN t.status = 'Rejete' THEN 1 ELSE 0 END) AS rejected_transactions,
       ROUND(
           SUM(CASE WHEN t.status = 'Rejete' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
           2
       ) AS rejection_rate
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
JOIN clients c ON a.client_id = c.client_id
GROUP BY c.segment;