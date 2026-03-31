-- Mart model: annual revenue summary with YoY Growth
-- Answers: how did revenue change year over year?

WITH yearly AS (
    SELECT
        year,
        SUM(total_revenue)  AS total_revenue,
        SUM(cc_btx)         AS btx_revenue,
        SUM(cc_supp)        AS supp_revenue,
        SUM(cc_wl)          AS wl_revenue,
        AVG(CASE WHEN total_revenue > 0 THEN total_revenue END) AS avg_daily_revenue,
        COUNT(CASE WHEN  total_revenue > 0 THEN 1 END) AS active_days
    FROM {{ ref('stg_clinic_revenue') }}
    GROUP BY year
),

with_growth AS (
    SELECT
        year,
        total_revenue,
        btx_revenue,
        supp_revenue,
        wl_revenue,
        avg_daily_revenue,
        active_days,
        LAG(total_revenue) OVER (ORDER BY year) AS prior_year_revenue,
        ROUND(
            (total_revenue - LAG(total_revenue) OVER (ORDER BY year))
            / NULLIF(LAG(total_revenue) OVER (ORDER BY year), 0) * 100, 
            1) AS yoy_growth_pct
    FROM yearly
)

SELECT * FROM with_growth
ORDER BY year