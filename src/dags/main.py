import sys
sys.path.append('/opt/airflow/src')


import datetime
from airflow import DAG
from airflow.operators.sql import SQLCheckOperator

with DAG(
    dag_id = "teste_pratico",
    start_date = datetime.now(),
    schedule = "@once", # */10 * * * *
):
    test_dw_conn = SQLCheckOperator(
        sql = 'SELECT CURRENT_TIMESTAMP;',
        conn_id = 'data_warehouse',
        task_id = 'check_data_warehouse_connection'
    )
    


test_dw_conn
