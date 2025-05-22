import os
import json
import logging
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv
from tasks.kafka.doawload_data_task import DoawloadDataTask
from tasks.spark.spark_create_dataframe_task import SparkCreateDataFrameTask
from tasks.kafka.format_data_task import FormatDataTask
from tasks.kafka.kafka_publisher_task import KafkaDataPublisher
from tasks.bigQuery.create_bigquery_connection_task import BigQueyConnectionTask
from tasks.bigQuery.load_to_bigQuery_table import LoadBigQueryTable
from tasks.spark.spark_streaming_reader_task import SparkKafkaStreamingReader

load_dotenv(dotenv_path="/opt/airflow/.env")  # ← chemin dans le conteneur


TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")
if not TOMTOM_API_KEY :
    logging.error("API NOT FOUND")
else :
    logging.info(f"API KEY LOADED SUCCESSFULLY : {TOMTOM_API_KEY}")
param_fields = '{incidents{type,geometry{type,coordinates},properties{id,iconCategory,magnitudeOfDelay,startTime,endTime,from,to,length,delay,timeValidity}}}'

# Charger les zones géographiques
with open('/opt/airflow/dags/config/zones.json') as f:
    ZONES = json.load(f)

default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2024, 9, 12, 10, 0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'Tomtom_trafic_automate',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    max_active_runs=1,
    concurrency=32,
    catchup=False
)

format_data_task = FormatDataTask()
create_dataframe_task = SparkCreateDataFrameTask()
bigquery_loader = LoadBigQueryTable()

def create_streaming_tasks(zone_name, topic_name, dag):
    table_name = f"{zone_name}_trafic_table"
    # download_task = DoawloadDataTask(TOMTOM_API_KEY, bbox)
    # kafka_publisher = KafkaDataPublisher(topic_name=topic_name)

    # # Task : publier dans Kafka
    # stream_task = PythonOperator(
    #     task_id=f"streaming_data_from_{zone_name}_data_trafic",
    #     python_callable=kafka_publisher.publish_streaming_data,
    #     op_args=[download_task, format_data_task],
    #     dag=dag
    # )

    # Task : lire depuis Kafka avec Spark et charger dans BigQuery
    def run_spark_streaming():
        spark_conn = BigQueyConnectionTask().create_spark_connection()
        spark_streaming = SparkKafkaStreamingReader(topic=topic_name)
        kafka_stream_df = spark_streaming.read_stream(spark_conn)
        formatted_df = create_dataframe_task.create_selection_df_from_kafka(kafka_stream_df)
        bigquery_loader.load_to_bigquery_table(table_name, formatted_df)

    spark_task = PythonOperator(
        task_id=f"spark_{zone_name}_streaming_task",
        python_callable=run_spark_streaming,
        dag=dag
    )

    return { "spark_task": spark_task}

# Générer dynamiquement les tasks pour chaque zone
tasks = []
for zone, bbox in ZONES.items():
    task_dict = create_streaming_tasks(zone, bbox["topic"], dag)
    tasks.append(task_dict)

# Définir les dépendances
for task in tasks:
     task["spark_task"]
