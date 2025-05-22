import logging

class SparkKafkaStreamingReader:
    """
    Classe générique pour lire un topic Kafka en continu avec Spark.
    """

    def __init__(self, kafka_bootstrap_servers='broker:29092', topic='users_north', starting_offsets='earliest'):
        """
        Initialise le lecteur Kafka Spark.

        :param kafka_bootstrap_servers: Adresse des serveurs Kafka (par ex. 'broker:29092')
        :param topic: Nom du topic Kafka à lire (par ex. 'users_nord')
        :param starting_offsets: Position de départ dans le topic ('latest' ou 'earliest')
        """
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.topic = topic
        self.starting_offsets = starting_offsets

    def read_stream(self, spark_session):
        """
        Crée un DataFrame Spark structuré à partir du flux Kafka.

        :param spark_session: La session Spark active
        :return: Un DataFrame Spark structuré ou None en cas d'erreur
        """
        logging.info(f"Lecture du topic Kafka '{self.topic}'...")

        try:
            return spark_session.readStream \
                .format('kafka') \
                .option('kafka.bootstrap.servers', self.kafka_bootstrap_servers) \
                .option('subscribe', self.topic) \
                .option('startingOffsets', self.starting_offsets) \
                .load()
        except Exception as e:
            logging.error(f"Erreur lors de la lecture du flux Kafka : {e}")
            return None
