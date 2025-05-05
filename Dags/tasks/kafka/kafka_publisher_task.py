from kafka import KafkaProducer
import json
import logging

class KafkaDataPublisher:
    """
    Cette classe permet de publier des données formatées dans un topic Kafka spécifié.
    
    Attributes:
        topic_name (str): Le nom du topic Kafka cible.
        bootstrap_servers (str): Adresse du broker Kafka.
    """

    def __init__(self, topic_name: str, bootstrap_servers: str = 'broker:29092'):
        self.topic_name = topic_name
        self.bootstrap_servers = bootstrap_servers
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            max_block_ms=5000
        )

    def publish_streaming_data(self, data_downloader, data_formatter):
        """
        Télécharge, formate et publie les données dans le topic Kafka spécifié.

        Args:
            data_downloader: Instance ou objet ayant une méthode `get_data()` pour récupérer les données brutes.
            data_formatter: Instance ou objet ayant une méthode `format_data(data)` pour formater les données.

        Returns:
            None

        Raises:
            Exception: En cas d'erreur lors de la production des données dans Kafka.
        """
        logging.info(f"Started data streaming into Kafka topic: {self.topic_name}")

        try:
            # Télécharger les données
            raw_data = data_downloader.get_data()

            # Formater les données
            formatted_data = data_formatter.format_data(raw_data)
            logging.info(f"Données envoyées à Kafka : {formatted_data}")

            # Envoi dans Kafka
            self.producer.send(
                self.topic_name,
                json.dumps(formatted_data).encode('utf-8')
            )
            self.producer.flush()
            logging.info("Data sent successfully to Kafka topic")

        except Exception as e:
            logging.error(f"Erreur lors de la production de données Kafka: {e}")
