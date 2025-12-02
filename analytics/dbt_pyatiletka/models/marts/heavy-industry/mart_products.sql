{{
    config(
        materialized='table',
        tags=['marts', 'heavy_industry']
    )
}}

-- Final analytics-ready products dimension

WITH products AS (
    SELECT * FROM {{ ref('stg_products') }}
),

enriched AS (
    SELECT
        product_id,
        product_code,
        product_name,
        product_category,
        unit_of_measure,
        description,

        -- Category groupings
        CASE
            WHEN product_category = 'STEEL' THEN 'Raw Materials'
            WHEN product_category = 'MACHINERY' THEN 'Equipment'
            WHEN product_category = 'ARMAMENTS' THEN 'Defense'
            ELSE 'Other'
        END AS product_group,

        -- Measurement classification
        CASE
            WHEN unit_of_measure = 'TONS' THEN 'Weight-based'
            WHEN unit_of_measure = 'UNITS' THEN 'Count-based'
            ELSE 'Other'
        END AS measurement_type,

        -- Metadata
        CURRENT_TIMESTAMP AS last_updated

    FROM products
)

SELECT * FROM enriched