-- Staging model: Clean view of raw clinic revenue data
-- SELECT all columns wiht explicit naming for clarity
SELECT
    full_date::date         AS date,
    year::int               AS year,
    month::int              AS month,
    month_name,
    day_of_week,
    day_of_month::int       AS day_of_month,
    quarter::int            AS quarter,
    cc_btx::numeric         AS cc_btx,
    cc_supp::numeric        AS cc_supp,
    cc_wl::numeric          AS cc_wl,
    cash_btx::numeric        AS cash_btx,
    cash_supp::numeric       AS cash_supp,
    cash_wl::numeric         AS cash_wl,
    check_btx::numeric       AS check_btx,
    check_supp::numeric      AS check_supp,
    check_wl::numeric        AS check_wl,
    total_revenue::numeric   AS total_revenue
FROM {{ source('clinic', 'clinic_revenue')}}
