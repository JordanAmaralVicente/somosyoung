import requests
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.sql import SQLCheckOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.exceptions import AirflowSkipException


NO_RECORDS_FOUND_MESSAGE = 'Não foram encontrados valores!'
DEFAULT_ID_AHOY = 1811657

def get_max_id_ahoy(ti):
    cursor = PostgresHook(postgres_conn_id = 'data_warehouse').get_conn().cursor()
    cursor.execute('SELECT MAX(id_email_sending) FROM ft_email_sending;')
    
    result = [v for v in cursor][0][0]
    max_id_ahoy = result + 1 if result else DEFAULT_ID_AHOY
    
    ti.xcom_push(key = 'max_id_ahoy', value = max_id_ahoy)


def fetch_ahoy_viewer_ti_api(ti, **kwargs):
    res = requests.post(
        kwargs['templates_dict']['url'],
        kwargs['templates_dict']['body'],
        kwargs['templates_dict']['headers']
    ).json()
    ti.xcom_push(key = 'ahoy_viewer_ti_data', value = res)


def mount_ft_email_sending_query(item):
   return [
            'INSERT INTO ft_email_sending VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id_email_sending) DO NOTHING',
            (
                int(item['id']),
                int(item['id_campaign']),
                bool(item['opened_at']),
                bool(item['clicked_at']),
                item['sent_at']
            )
        ]


def mount_dm_email_sending_query(item):
    return [
        'INSERT INTO dm_email_sending VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (
                int(item['id']),
                item['to'],
                item['user_type'],
                item['token'],
                item['mailer'],
                item['opened_at'],
                item['clicked_at']
            )
    ] 


def mount_dm_email_campaign_query(item):
    return [
        'INSERT INTO dm_email_campaign VALUES (%s, %s, %s) ON CONFLICT (id_campaign) DO NOTHING',
            (
                int(item['id_campaign']),
                item['company'],
                item['subject'],
            )
    ]


def load_data_into_data_warehouse(ti, mount_query_function):
    data = ti.xcom_pull(task_ids='fetch_api_data', key='ahoy_viewer_ti_data')

    if 'response' in data and 'message' in data['response'] and NO_RECORDS_FOUND_MESSAGE in data['response']['message']:
        raise AirflowSkipException


    conn = PostgresHook(postgres_conn_id = 'data_warehouse').get_conn()
    cursor = conn.cursor()

    for item in data:
        cursor.execute(*mount_query_function(item))

    conn.commit()
    cursor.close()
    conn.close()


with DAG(
    dag_id = 'teste_pratico',
    start_date = datetime.now() - timedelta(minutes = 15),
    schedule_interval = '*/10 * * * *', # 
    default_args = {
        'retries': 5,
        'retry_delay': timedelta(minutes=1),
        'email_on_failure': True,
        'email_on_retry': False,
        'email': ['jordanamaralvicente@gmail.com']
    },
):
    task_test_dw_connection = SQLCheckOperator(
        sql = 'SELECT CURRENT_TIMESTAMP;',
        conn_id = 'data_warehouse',
        task_id = 'check_data_warehouse_connection'
    )

    task_get_max_idahoy = PythonOperator(
        task_id = 'get_max_idahoy',
        python_callable = get_max_id_ahoy,
        provide_context = True
    )

    task_fetch_api_data = PythonOperator(
        task_id = 'fetch_api_data',
        python_callable = fetch_ahoy_viewer_ti_api,
        templates_dict = {
            'url': 'https://{{ conn.ahoy_viewer_ti.host }}/api/ahoy_viewer_ti',
            'headers': { 'Content-Type': 'application/json' },
            'body': {
                'token': '{{ conn.ahoy_viewer_ti.extra_dejson.token }}',
                'idahoy': '{{ task_instance.xcom_pull(task_ids="get_max_idahoy", key="max_id_ahoy")}}'
            }
        }
    )

    task_ft_es = PythonOperator(
        task_id = 'load_ft_email_sending_data',
        python_callable = lambda ti: load_data_into_data_warehouse(ti, mount_ft_email_sending_query),
    )

    task_dm_es = PythonOperator(
        task_id = 'load_dm_email_sending',
        python_callable = lambda ti: load_data_into_data_warehouse(ti, mount_dm_email_sending_query),
    )

    task_dm_ec = PythonOperator(
        task_id = 'load_dm_email_campaign',
        python_callable = lambda ti: load_data_into_data_warehouse(ti, mount_dm_email_campaign_query),
    )
    

task_test_dw_connection >> task_get_max_idahoy

task_get_max_idahoy >> task_fetch_api_data >> [task_ft_es, task_dm_ec, task_dm_es]
