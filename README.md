# Pyatiletka
Soviet Union 5 year plan economic data collection pipeline

A data mesh implementation inspired by Soviet economic planning, built as a learning project for modern data engineering concepts.

This project reimagines the USSR's State Planning Committee using contemporary data architecture. I'm building a distributed data platform where different "ministries" (Heavy Industry, Agriculture, Transport, Energy) own their data domains while a central platform provides governance, orchestration, and cross-domain analytics. Each ministry manages its own databases and APIs, publishes data products with quality guarantees, and contributes to centralized dashboards tracking plan vs. actual metrics across the economy.

![](https://github.com/git-fahad/Pyatiletka/blob/main/USSR%20Pictures%20on%20X.jpeg)

The goal is hands-on experience with data mesh architecture, ETL pipelines (Airflow + dbt), data governance frameworks, audit systems, RBAC implementation, and data quality monitoring (Great Expectations). 

The Soviet planning theme provides natural domain boundaries, realistic challenges around data quality and interdependencies, and built-in requirements for strict auditing and governance.
##
**Tech Stack:** Python, PostgreSQL, TimescaleDB, Apache Airflow, dbt, FastAPI, Docker
**Status:** Work in progress. Building incrementally as I learn.

**"План - это закон" ("The plan is law")**
