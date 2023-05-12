from datetime import datetime

from airflow.providers.ssh.operators.ssh import SSHOperator

from airflow import DAG

with DAG(
    dag_id='debugman',
    start_date=datetime(2023, 5, 10),
    schedule_interval=None,
    catchup=False
) as dag:
    
    spark_submit = SSHOperator(
        task_id='spark_submit',
        ssh_conn_id='ssh_conn',
        command='''PATH=/opt/bitnami/python/bin:/opt/bitnami/java/bin:/opt/bitnami/spark/bin:/opt/bitnami/spark/sbin:/opt/bitnami/common/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin && pip install delta-spark==2.3.0 && export GOOGLE_APPLICATION_CREDENTIALS=/opt/bitnami/spark/secrets/gcp-credentials.json && cd /src && spark-submit --packages io.delta:delta-core_2.12:2.1.0 --master spark://spark:7077 first-app.py'''
    )

    spark_submit
