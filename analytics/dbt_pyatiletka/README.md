# Pyatiletka dbt Project

## Overview

This dbt project transforms data from the Pyatiletka (Five-Year Plan) Heavy Industry domain, implementing a modern data lakehouse architecture using DuckDB and MinIO.

## Architecture

```
MinIO Bronze (Parquet files)
    ↓
dbt Staging Models (cleaned views)
    ↓
dbt Mart Models (analytics tables)
    ↓
DuckDB Warehouse
    ↓
Grafana/Superset Dashboards
```

## Project Structure

```
dbt_pyatiletka/
├── models/
│   ├── staging/           # Clean raw data from bronze layer
│   │   ├── stg_facilities.sql
│   │   ├── stg_products.sql
│   │   └── stg_regions.sql
│   ├── intermediate/      # Business logic transformations (future)
│   └── marts/            # Analytics-ready tables
│       └── heavy_industry/
│           ├── mart_facilities.sql
│           ├── mart_products.sql
│           └── schema.yml
├── tests/                # Custom data tests
├── macros/               # Reusable SQL macros
└── seeds/                # Static reference data (CSV)
```

## Data Models

### Staging Layer
- **stg_facilities**: Cleaned facility master data
- **stg_products**: Cleaned product catalog
- **stg_regions**: Geographic hierarchy

### Marts Layer
- **mart_facilities**: Analytics-ready facilities with enriched attributes
- **mart_products**: Product dimension with classifications

## Running dbt

### Setup

```bash
# Install dbt with DuckDB adapter
pip install dbt-duckdb

# Install dbt packages
dbt deps

# Test connection
dbt debug
```

### Development

```bash
# Run all models
dbt run

# Run specific model
dbt run --select stg_facilities

# Run tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

### Common Commands

```bash
# Full refresh (rebuild all tables)
dbt run --full-refresh

# Run only changed models
dbt run --select state:modified+

# Run models by tag
dbt run --select tag:heavy_industry

# Test specific model
dbt test --select stg_facilities
```

## Testing Strategy

- **Uniqueness**: Primary keys must be unique
- **Not Null**: Critical fields cannot be null
- **Referential Integrity**: Foreign keys must exist
- **Accepted Values**: Enums match expected values
- **Data Freshness**: Bronze data updated within 2 days

## Data Quality

Tests are defined in `schema.yml` files and include:
- Primary key uniqueness
- Required field validation
- Categorical value constraints
- Data freshness checks

## Materialization Strategy

| Layer | Materialization | Reason |
|-------|----------------|--------|
| Staging | View | Always fresh, no storage overhead |
| Intermediate | View | Temporary transformations |
| Marts | Table | Fast query performance |

## DuckDB Configuration

This project uses DuckDB with:
- **httpfs extension**: Read from S3/MinIO
- **parquet extension**: Native Parquet support
- **In-memory processing**: Fast analytics

Connection configured in `profiles.yml`:
- MinIO endpoint: `minio:9000`
- Reads directly from Parquet files
- No data copying required

## Future Enhancements

- [ ] Add production fact tables (actual_production)
- [ ] Create plan vs actual comparison models
- [ ] Implement incremental models for large datasets
- [ ] Add data quality dashboards
- [ ] Create metrics layer with dbt metrics
- [ ] Add snapshot models for SCD Type 2

## Documentation

Generate and view docs:
```bash
dbt docs generate
dbt docs serve --port 8080
```

Visit: http://localhost:8080


---

**Project**: Pyatiletka (Five-Year Plan Data Mesh)  
**Owner**: Fahad     
**Last Updated**: Dec 2025