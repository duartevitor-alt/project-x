from datetime import datetime

from airflow.operators.empty import EmptyOperator
from airflow.providers.airbyte.operators.airbyte import \
    AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor
from airflow.providers.ssh.operators.ssh import SSHOperator

from airflow import DAG

with DAG(
    dag_id='project-x',
    start_date=datetime(2023, 5, 10),
    schedule_interval=None,
    catchup=False
) as dag:
    
    task1 = EmptyOperator(
        task_id='Start'
    )

    task2 = EmptyOperator(
        task_id='Elastic-GCS'
    )

    async_airbyte_transfer = AirbyteTriggerSyncOperator(
        task_id='Airbyte-transfer-raw-data',
        airbyte_conn_id='airbyte_conn_example',
        connection_id='657fc801-dd72-4b7f-90e1-38669161add1'
        asynchronous=True,
    )
    
    airbyte_sensor = AirbyteJobSensor(
        task_id='airbyte_senso',
        airbyte_conn_id='airbyte_conn_example',
        airbyte_job_id=async_airbyte_transfer.output
    )

    task5 = EmptyOperator(
        task_id='Transform-and-Write'
    )

    spark_submit = SSHOperator(
        task_id='spark_submit',
        ssh_conn_id='ssh_conn',
        command='''PATH=/opt/bitnami/python/bin:/opt/bitnami/java/bin:/opt/bitnami/spark/bin:/opt/bitnami/spark/sbin:/opt/bitnami/common/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin && pip install delta-spark==2.3.0 && export GOOGLE_APPLICATION_CREDENTIALS=/opt/bitnami/spark/secrets/gcp-credentials.json && cd /src && spark-submit --packages io.delta:delta-core_2.12:2.1.0 --master spark://spark:7077 first-app.py'''
    )

    task1 >> task2 >> async_airbyte_transfer >> airbyte_sensor
    task5 >> spark_submit
