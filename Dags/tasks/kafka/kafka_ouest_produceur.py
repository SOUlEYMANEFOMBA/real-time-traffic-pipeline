from kafka import KafkaProducer
import json
import logging

class KafkaDataOuestPublisherTask:
    """
    Cette classe publie des données formatées dans un topic Kafka - topic ouest.

    Attributes:
        None
    """
    
    def streaming_data_ouest(self, doawloaddata, formatData):
        """
        Cette méthode envoie des données téléchargées et formatées au topic Kafka 'users_ouest_created'.

        Args:
            doawloaddata: Instance ou objet pour télécharger les données à partir d'une source.
            formatData: Instance ou objet pour formater les données dans le bon format avant l'envoi à Kafka.

        Returns:
            None

        Raises:
            Exception: En cas d'erreur pendant la production des données dans Kafka.
        """
        logging.info(f"Started trafic ouest france data streaming into Kafka")

        # Initialise le producteur Kafka pour envoyer des messages au broker Kafka
        producer = KafkaProducer(bootstrap_servers='broker:29092', max_block_ms=5000)
        
        try:
            # Télécharger les données à partir de la source spécifiée
            data_raw =doawloaddata.get_data() 
                
            # Formater les données avant de les envoyer à Kafka
            format_data = formatData.format_data(data_raw)
            logging.info(f"Voici les données envoyées à Kafka: {format_data}")
                
            # Envoyer les données formatées au topic Kafka 'users_nord_created'
            producer.send('users_ouest_created', json.dumps(format_data).encode('utf-8'))
                
            # S'assurer que les messages sont bien envoyés
            producer.flush()
            logging.info(f"Data sent successfully")
            
        except Exception as e:
            # Enregistrer les erreurs éventuelles pendant l'envoi
            logging.error(f"Erreur lors de la production de données Kafka: {e}")
  
            