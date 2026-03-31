-- Mart model: monthly revenue summary
-- Answers: which months perform best and what are the seasonal patterns?

SELECT
    year,
    month,
    month_name,
    SUM(total_revenue)                                          AS total_revenue,
    SUM(cc_btx)                                                 AS btx_revenue,
    AVG(CASE WHEN total_revenue > 0 THEN total_revenue END)     AS avg_daily_revenue,
    COUNT(CASE WHEN total_revenue > 0 THEN 1 END)               AS active_days,
    ROUND(
        SUM(total_revenue) / 
        NULLIF(SUM(SUM(total_revenue)) OVER (PARTITION BY year), 0) * 100
    , 1)                                                        AS pct_of_year_revenue
FROM {{ ref('stg_clinic_revenue') }}
GROUP BY year, month, month_name
ORDER BY year, month
