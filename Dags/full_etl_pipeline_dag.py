import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from tasks.kafka.doawload_data_task import DoawloadDataTask
from tasks.spark.spark_create_dataframe_task import SparkCreateDataFrameTask
from tasks.kafka.format_data_task import FormatDataTask
from tasks.kafka.kafka_publisher_task import KafkaDataPublisher
from tasks.bigQuery.create_bigquery_connection_task import BigQueyConnectionTask
from tasks.bigQuery.load_to_bigQuery_table import LoadBigQueryTable
from tasks.spark.spark_streaming_reader_task import SparkKafkaStreamingReader
import json

TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")
param_fields = '{incidents{type,geometry{type,coordinates},properties{id,iconCategory,magnitudeOfDelay,startTime,endTime,from,to,length,delay,timeValidity}}}'

# Zones géographiques
f=open('/workspace/Dags/config/zones.json')
ZONES =json.load(f)

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
    max_active_runs=1,            # nombre de DAGs actifs simultanément
    concurrency=32,               # max de tâches en parallèle dans ce DAG
    catchup=False
)

format_data_task = FormatDataTask()
create_dataframe_task = SparkCreateDataFrameTask()
bigquery_loader = LoadBigQueryTable()
spark_conn = BigQueyConnectionTask().create_spark_connection()

def create_streaming_tasks(zone_name, bbox,topic_name, dag):
    # topic_name = f"users_{zone_name}_created"
    table_name = f"{zone_name}_trafic_table"

    # Télécharger les données
    download_task = DoawloadDataTask(TOMTOM_API_KEY, {zone_name: bbox})

    kafka_publisher = KafkaDataPublisher(topic_name=topic_name)
    stream_task = PythonOperator(
        task_id=f"streaming_data_from_{zone_name}_data_trafic",
        python_callable=kafka_publisher.publish_streaming_data,
        op_args=[download_task, format_data_task],
        dag=dag
    )

    # Spark Streaming depuis Kafka
    spark_streaming = SparkKafkaStreamingReader(topic=topic_name)
    kafka_stream_df = spark_streaming.read_stream(spark_conn)

    # Transformation des données
    formatted_df = create_dataframe_task.create_selection_df_from_kafka(kafka_stream_df)

    spark_task = PythonOperator(
        task_id=f"spark_{zone_name}_streaming_task",
        python_callable=bigquery_loader.load_to_bigquery_table,
        op_args=[table_name, formatted_df],
        dag=dag
    )

    return {stream_task, spark_task}

# Générer dynamiquement les tasks pour chaque zone
tasks = []

for zone, bbox in ZONES.items():
    tasks_dict= create_streaming_tasks(zone, bbox["bbox"],bbox["topic"], dag)
    tasks.append(tasks_dict)

# Définir les dépendances
for task in tasks :
   task["stream_task"]>> task["spark_task"]
