import sys
import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from SCRIPT1_fetch_data import upload_images_from_folder
from SCRIPT2_remove_background import background_removal
from SCRIPT3_vectorize_images import vectorize_images_from_uuid

default_args = {
    'owner': 'airflow',
    'start_date': datetime.today().date(),
    'retries': 1,
}

# Define the DAG
with DAG('image_processing_pipeline',
         default_args=default_args,
         schedule_interval='@daily',  # Adjust according to your needs
         catchup=False) as dag:
    
    # Task 1: Fetch Data
    def fetch_data_task(**kwargs):
        # Replace with your actual folder path
        input_path = '../../data-local-test/new-faces-to-add'
        uuids = fetch_data(input_path)
        # Push the UUID list to XComs
        kwargs['ti'].xcom_push(key='uuids', value=uuids)

    fetch_data_op = PythonOperator(
        task_id='fetch_data[ext -> raw]',
        python_callable=fetch_data_task,
        provide_context=True
    )
    
    # Task 2: Remove Background
    def remove_background_task(**kwargs):
        # Pull UUIDs from XComs
        uuids = kwargs['ti'].xcom_pull(key='uuids', task_ids='fetch_data')
        background_removal(uuids)

    remove_background_op = PythonOperator(
        task_id='remove_background[raw -> staging]',
        python_callable=remove_background_task,
        provide_context=True
    )

    # Task 3: Vectorize Images
    def vectorize_images_task(**kwargs):
        # Pull UUIDs from XComs
        uuids = kwargs['ti'].xcom_pull(key='uuids', task_ids='fetch_data')
        vectorize_images_from_uuid(uuids)

    vectorize_images_op = PythonOperator(
        task_id='vectorize_images[staging -> curated]',
        python_callable=vectorize_images_task,
        provide_context=True
    )

    # Define task dependencies
    fetch_data_op >> remove_background_op >> vectorize_images_op