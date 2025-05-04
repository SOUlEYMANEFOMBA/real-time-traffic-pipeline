import logging


class SparkSudEstStreamingTask():
    
    """_summary_
    """
    def connect_to_kafka_topic_users_sud_est_created(self, spark_connect):
        """
        Crée un DataFrame Spark en consommant les données depuis Kafka.

        :param spark_connect: La session Spark active
        :return: Un DataFrame Spark, ou None en cas d'erreur
        """
        logging.info("Beginning of Kafka DataFrame creation...")
        spark_df = None
        try:
            spark_df = spark_connect.readStream \
                .format('kafka') \
                .option('kafka.bootstrap.servers', 'broker:29092') \
                .option('subscribe', 'users_sud_est_created') \
                .option('startingOffsets', 'earliest') \
                .load()
            logging.info("Kafka DataFrame created successfully!")
        except Exception as e:
            logging.warning(f"Kafka DataFrame could not be created due to: {e}")

        return spark_df
