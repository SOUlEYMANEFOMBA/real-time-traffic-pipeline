import logging
from pyspark.sql import SparkSession

class BigQueyConnectionTask:
    """_summary_
    
    """
    def create_spark_connection(self):
        """
        Création d'une session Spark avec connexion à BigQuery
        """
        logging.info("Beginning of Spark connection to BigQuery...")

        spark_connect = None
        try:
            # SparkSession avec le connecteur BigQuery
            spark_connect = SparkSession.builder \
                .appName("KafkaToBigQuery") \
                .master('spark://spark-master:7077') \
                .config("spark.jars", "/opt/airflow/jars/spark-bigquery.jar",
                        "/opt/airflow/jars/spark-sql-kafka-0-10_2.12-3.3.2.jar",
                        "/opt/airflow/jars/kafka-clients-2.8.0.jar")\
                .config("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
                .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", "/opt/airflow/key/real-time-traffic-pipeline-30d152e38926.json") \
                .getOrCreate()
            
            spark_connect.sparkContext.setLogLevel("ERROR")
            logging.info("Spark session created successfully.")
        
        except Exception as e:
            logging.error(f"Couldn't create the Spark session due to exception: {e}")
        
        return spark_connect
