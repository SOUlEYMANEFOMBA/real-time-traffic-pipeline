import logging
from pyspark.sql import SparkSession

class BigQueyConnectionTask:
    """_summary_
    
    """
    
    def create_spark_connection(self):
        """_summary_
         Creation d'une session spark avec la connection à BigQuery
        """
        logging.info(f"beggining of spark connection to BigQuery ...")
        
        spark_connect= None 
        try :    
        # 1. SparkSession avec le connecteur BigQuery
                                
            spark_connect = SparkSession.builder \
                .appName("KafkaToBigQuery") \
                .config("spark.jars", "/path/to/spark-bigquery-with-dependencies_2.12-0.32.2.jar") \
                .config("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
                .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", "/workspace/key/real-time-traffic-pipeline-30d152e38926.json") \
                .getOrCreate()
            spark_connect.sparkConext.setLogLev("ERROR")
            logging.info(f"spark session created sussesfully ..")
        except Exception as e :
            logging.error(f"Couldn't create the Spark session due to exception: {e}")
        return spark_connect