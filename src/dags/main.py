from datetime import datetime
from airflow import DAG
from airflow.operators.sql import SQLCheckOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

import requests


def fetch_ahoy_viewer_ti_api(**kwargs):
    template = kwargs['templates_dict']
    data = template['body']
    url = template['url']
    headers = template['headers']

    res = requests.post(url, data, headers)
    kwargs['ti'].xcom_push(key = 'ahoy_viewer_ti_data', value = res.text)


with DAG(
    dag_id = "teste_pratico",
    start_date = datetime.now(),
    schedule = "@once", # */10 * * * *
):
    task_test_dw_connection = SQLCheckOperator(
        sql = 'SELECT CURRENT_TIMESTAMP;',
        conn_id = 'data_warehouse',
        task_id = 'check_data_warehouse_connection'
    )

    task_fetch_api_data = PythonOperator(
        task_id = 'fetch_api_data',
        python_callable = fetch_ahoy_viewer_ti_api,
        templates_dict = {
            'url': 'https://{{ conn.ahoy_viewer_ti.host }}/api/ahoy_viewer_ti',
            'headers': { 'Content-Type': 'application/json' },
            'body': {
                'token': '{{ conn.ahoy_viewer_ti.extra_dejson.token }}',
                'idahoy': 1811657
            }
        }
    )

    
    task = EmptyOperator(task_id = 'task')

task_test_dw_connection >> task_fetch_api_data >> task
