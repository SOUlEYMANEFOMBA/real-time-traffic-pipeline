import json
import requests
import logging
from datetime import datetime, timezone
from urllib.parse import urlencode
class DoawloadDataTask():
    """
    Cette classe est responsable de l'importation des données en utilisant l'API TOMTOM des incidents routiers dans certains zone de la france
    
    "nord": "1.9,48.6,3.2,49.4",         # ≈ 9 900 km² - Paris, Meaux, Évry, Roissy  - couvre Paris, banlieue, A1, A6, A3, A4 — trafic dense assuré
    "sud_ouest": "-1.2,44.4,0.6,45.4",   # ≈ 9 600 km² - Couvre Bordeaux, Libourne, Langon, autoroutes A10 / A62 / A63
    "sud_est": "4.8,43.0,6.5,44.3" ,     # ≈ 9 900 km² - Marseille, Toulon, Aix, autoroutes A7 / A8 / A50
    "ouest": "-2.5,46.8,-0.5,48.2"       # ≈ 9 800 km² - Couvre Nantes, Rennes, Angers, et autoroutes A11 / A83
    
    Attributes:
        api_key (str): clé d'API personnelle pour accéder à TomTom
        bbox (str): zone géographique de recherche (format : lon_min,lat_min,lon_max,lat_max).
        base_url (str): domaine de l'API (valeur par défaut).
        language (str): langue pour les libellés des incidents (fr-FR par défaut).
    """
    def __init__(self,api_key : str, bbox: str , base_url: str ="api.tomtom.com", language : str ="fr-FR"):
            self.api_key = api_key
            self.bbox= bbox
            self.base_url = base_url
            self.language = language
            self.fields = '{incidents{type,geometry{type,coordinates},properties{id,iconCategory,magnitudeOfDelay,startTime,endTime,from,to,length,delay,timeValidity}}}'
    
    def __build_url(self) -> str:
        timestamp = int(datetime.now(timezone.utc).timestamp())
        params = {
            "key": self.api_key,
            "bbox": self.bbox,
            "fields": self.fields,
            "language": self.language,
            "t": timestamp,
            "categoryFilter": "0,1,2,3,4,5,6,7,8,9,10,11,14",
            "timeValidityFilter": "present,future"
        }
        query_string = urlencode(params)
        
        return f"https://{self.base_url}/traffic/services/5/incidentDetails?{query_string}"
    def get_data(self) -> dict:
        """
        Effectue un appel GET à l'API TomTom et retourne les données JSON sous forme de dictionnaire Python.

        Returns:
            dict: Données d'incidents routiers (ou None si erreur).
        """
        logging.info("Début de la récupération des données TomTom Traffic API")
        
        logging.info(f"beginning of doawload data from TOM TOM TRAFIC API ")
        
        url=self.__build_url()
        
        try :
            response= requests.get(url)
            response.raise_for_status()    #Lève une exception en cas de statut HTTP >= 400

            data_text= response.text       # Données brutes au format texte JSON
            
            data_parsed=json.loads(data_text) # On transforme en dictionnaire Python
            
            logging.info(f"Structure des données récupérées : {type(data_parsed)}")

            logging.info(f"Données récupérées avec succès")
            return data_parsed
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Erreur HTTP : {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Erreur de requête : {req_err}")
        except Exception as e:
            logging.error(f"Erreur générale : {e}")
        
        return None