{{
    config(
        materialized='table',
        tags=['marts', 'heavy_industry']
    )
}}

-- Final analytics-ready facilities dimension

WITH facilities AS (
    SELECT * FROM {{ ref('stg_facilities') }}
),

regions AS (
    SELECT * FROM {{ ref('stg_regions') }}
),

joined AS (
    SELECT
        f.facility_id,
        f.facility_code,
        f.facility_name,
        f.facility_type,

        -- Capacity metrics
        f.capacity_per_day,
        f.capacity_per_day * 365 AS capacity_per_year,

        -- Workforce
        f.workforce_size,

        -- Status
        f.status,
        CASE
            WHEN f.status = 'ACTIVE' THEN TRUE
            ELSE FALSE
        END AS is_active,

        -- Dates
        f.commissioned_date,
        DATE_DIFF('year', f.commissioned_date, CURRENT_DATE) AS years_operational,

        -- Region information
        f.region_name,
        r.region_type,
        r.region_code,

        -- Facility classification
        CASE
            WHEN f.facility_type = 'STEEL_MILL' THEN 'Steel Production'
            WHEN f.facility_type = 'MACHINERY_FACTORY' THEN 'Machinery Manufacturing'
            WHEN f.facility_type = 'TANK_PLANT' THEN 'Military Equipment'
            ELSE 'Other'
        END AS facility_category,

        -- Metadata
        CURRENT_TIMESTAMP AS last_updated

    FROM facilities f
    LEFT JOIN regions r ON f.region_name = r.region_name
)

SELECT * FROM joined