"""
Heavy Industry ETL Pipeline
Pyatiletka Project

Extracts data from Heavy Industry API → Writes to MinIO as Parquet
"""

from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import requests
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from minio import Minio
from io import BytesIO
import os

# Configuration
HEAVY_INDUSTRY_API_URL = os.getenv('HEAVY_INDUSTRY_API_URL', 'http://heavy-industry-api:8000')
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'minio:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minio_admin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minio_password')

# Default DAG arguments
default_args = {
    'owner': 'pyatiletka',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Initialize DAG
dag = DAG(
    'heavy_industry_to_bronze',
    default_args=default_args,
    description='Extract Heavy Industry data and load to MinIO bronze layer',
    schedule_interval='@daily',  # Run daily
    start_date=days_ago(1),
    catchup=False,
    tags=['heavy-industry', 'bronze', 'etl'],
)


def get_minio_client():
    """Create MinIO client"""
    return Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False  # Use HTTP (not HTTPS) for local development
    )


def extract_facilities(**context):
    """
    Extract facilities data from Heavy Industry API
    """
    print(f"Extracting facilities from {HEAVY_INDUSTRY_API_URL}/facilities")

    response = requests.get(f"{HEAVY_INDUSTRY_API_URL}/facilities")
    response.raise_for_status()

    data = response.json()
    print(f"Extracted {len(data)} facilities")

    # Push to XCom for next task
    context['task_instance'].xcom_push(key='facilities_data', value=data)
    return len(data)


def extract_products(**context):
    """
    Extract products data from Heavy Industry API
    """
    print(f"Extracting products from {HEAVY_INDUSTRY_API_URL}/products")

    response = requests.get(f"{HEAVY_INDUSTRY_API_URL}/products")
    response.raise_for_status()

    data = response.json()
    print(f"Extracted {len(data)} products")

    context['task_instance'].xcom_push(key='products_data', value=data)
    return len(data)


def extract_regions(**context):
    """
    Extract regions data from Heavy Industry API
    """
    print(f"Extracting regions from {HEAVY_INDUSTRY_API_URL}/regions")

    response = requests.get(f"{HEAVY_INDUSTRY_API_URL}/regions")
    response.raise_for_status()

    data = response.json()
    print(f"Extracted {len(data)} regions")

    context['task_instance'].xcom_push(key='regions_data', value=data)
    return len(data)


def load_to_bronze(**context):
    """
    Load extracted data to MinIO bronze bucket as Parquet files
    """
    ti = context['task_instance']
    execution_date = context['execution_date'].strftime('%Y-%m-%d')

    # Get data from XCom
    facilities = ti.xcom_pull(key='facilities_data', task_ids='extract_facilities')
    products = ti.xcom_pull(key='products_data', task_ids='extract_products')
    regions = ti.xcom_pull(key='regions_data', task_ids='extract_regions')

    # Initialize MinIO client
    minio_client = get_minio_client()

    # Helper function to write DataFrame to MinIO as Parquet
    def write_to_minio(df, object_name):
        # Convert DataFrame to Parquet in memory
        buffer = BytesIO()
        table = pa.Table.from_pandas(df)
        pq.write_table(table, buffer)
        buffer.seek(0)

        # Upload to MinIO
        minio_client.put_object(
            bucket_name='bronze',
            object_name=object_name,
            data=buffer,
            length=buffer.getbuffer().nbytes,
            content_type='application/octet-stream'
        )
        print(f"Uploaded {object_name} to bronze bucket")

    # Write facilities
    if facilities:
        df_facilities = pd.DataFrame(facilities)
        write_to_minio(df_facilities, f'heavy_industry/facilities/{execution_date}/facilities.parquet')

    # Write products
    if products:
        df_products = pd.DataFrame(products)
        write_to_minio(df_products, f'heavy_industry/products/{execution_date}/products.parquet')

    # Write regions
    if regions:
        df_regions = pd.DataFrame(regions)
        write_to_minio(df_regions, f'heavy_industry/regions/{execution_date}/regions.parquet')

    print(f"Successfully loaded all data to bronze layer for {execution_date}")


# Define tasks
extract_facilities_task = PythonOperator(
    task_id='extract_facilities',
    python_callable=extract_facilities,
    dag=dag,
)

extract_products_task = PythonOperator(
    task_id='extract_products',
    python_callable=extract_products,
    dag=dag,
)

extract_regions_task = PythonOperator(
    task_id='extract_regions',
    python_callable=extract_regions,
    dag=dag,
)

load_to_bronze_task = PythonOperator(
    task_id='load_to_bronze',
    python_callable=load_to_bronze,
    dag=dag,
)

# Set task dependencies
[extract_facilities_task, extract_products_task, extract_regions_task] >> load_to_bronze_task