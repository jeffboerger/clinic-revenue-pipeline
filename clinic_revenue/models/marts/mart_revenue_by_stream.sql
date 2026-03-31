-- Mart model: revenue broken out by stream over time
-- Answers: how did BTX, Supplements, and Weight Loss perform each year?

SELECT
    year,
    SUM(cc_btx + cash_btx + check_btx)     AS btx_revenue,
    SUM(cc_supp + cash_supp + check_supp)   AS supp_revenue,
    SUM(cc_wl + cash_wl + check_wl)         AS wl_revenue,
    SUM(total_revenue)                       AS total_revenue,
    ROUND(
        SUM(cc_btx + cash_btx + check_btx) /
        NULLIF(SUM(total_revenue), 0) * 100
    , 1)                                     AS btx_pct,
    ROUND(
        SUM(cc_supp + cash_supp + check_supp) /
        NULLIF(SUM(total_revenue), 0) * 100
    , 1)                                     AS supp_pct,
    ROUND(
        SUM(cc_wl + cash_wl + check_wl) /
        NULLIF(SUM(total_revenue), 0) * 100
    , 1)                                     AS wl_pct
FROM {{ ref('stg_clinic_revenue') }}
GROUP BY year
ORDER BY year