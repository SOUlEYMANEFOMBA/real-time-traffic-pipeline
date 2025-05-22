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

    def __init__(self, topic_name: str, bootstrap_servers: str = 'broker:29029'):
        self.topic_name = topic_name
        self.bootstrap_servers = bootstrap_servers

        # Utilisation d'un value_serializer pour encoder automatiquement les objets Python en JSON
        logging.info(f"this a broker : {self.bootstrap_servers}")
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
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
        """
        logging.info(f"Started data streaming into Kafka topic: {self.topic_name}")

        try:
            # Télécharger les données
            raw_data = data_downloader.get_data()

            if not raw_data:
                logging.warning("Aucune donnée téléchargée. Rien à publier.")
                return

            # Formater les données
            formatted_data = data_formatter.format_data(raw_data)
            if not formatted_data:
                logging.warning("Données formatées vides. Rien à publier.")
                return

            logging.info(f"{len(formatted_data)} incidents à publier dans Kafka.")

            # Envoi dans Kafka (un par un)
            for record in formatted_data:
                logging.info(f"this is a record: {record}")
                kafka_topic = self.topic_name.decode('utf-8') if isinstance(self.topic_name, bytes) else self.topic_name
                logging.info(f"type(kafka_topic): {type(kafka_topic)}, value: {kafka_topic}")
                logging.info(f"kafka producer : {self.producer}, type_producer : {type(self.producer)}")
                
                for  broker in self.producer._metadata.brokers()  :
                    logging.info(f"Broker node_id: {broker.nodeId}, host: {broker.host}, port: {broker.port}")

                self.producer.send(kafka_topic, value=record)

            self.producer.flush()
            logging.info("Tous les incidents ont été publiés avec succès.")

        except Exception as e:
            logging.error(f"Erreur lors de la production de données Kafka: {e}")
