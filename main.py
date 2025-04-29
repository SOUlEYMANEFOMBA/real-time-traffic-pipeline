import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime, timezone
##je charge les fichiers d'environement
load_dotenv()
# Chargement des configs
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")
# REDPANDA_BOOTSTRAP_SERVERS = os.getenv("REDPANDA_BOOTSTRAP_SERVERS", "").split(",")
# REDPANDA_API_KEY = os.getenv("REDPANDA_API_KEY")
# REDPANDA_API_SECRET = os.getenv("REDPANDA_API_SECRET")
# TOPIC = os.getenv("REDPANDA_TOPIC", "traffic-france")

# Fonction pour récupérer les incidents
def fetch_traffic_incidents():
    print("on commence")
   
    base_url = 'api.tomtom.com'
    param_fields = '{incidents{type,geometry{type,coordinates},properties{id,iconCategory,magnitudeOfDelay,startTime,endTime,from,to,length,delay,timeValidity}}}'

    # Liste des bbox avec commentaires pour chaque zone

    bboxes = {
        "nord": "48.6,2.1,49.1,3.0",         # ≈ 8900 km² — Paris et sa région nord
        "sud_ouest": "44.5,-0.7,45.2,0.3",   # ≈ 9500 km² — Bordeaux et alentours
        "sud_est": "43.2,5.3,44.0,6.3",      # ≈ 8800 km² — Marseille, Toulon
        "ouest": "-2.0,47.0,-1.0,47.8"       # ≈ 8500 km² — Nantes, Saint-Nazaire, Ancenis
    }
    
    timestamps= int(datetime.now(timezone.utc).timestamp())
    print(timestamps)

    for zone_name, bbox in bboxes.items():
        print(f"\n--- Requête pour la zone : {zone_name.upper()} ---")
        
        api_url = (
            f'https://{base_url}/traffic/services/5/incidentDetails'
            f'?key={TOMTOM_API_KEY}'
            f'&bbox={bbox}'
            f'&fields={param_fields}'
            f'&language=fr-FR'
            f'&t={timestamps}'
            f'&categoryFilter=0,1,2,3,4,5,6,7,8,9,10,11,14'
            f'&timeValidityFilter=present,future'
        )
        
        response = requests.get(api_url)
        
        try:
            response = requests.get(api_url, params=param_fields)
            data = response.text
            parsed = json.loads(data)
            print(json.dumps(parsed, indent=4))
            # print(data)
            
        except requests.exceptions.HTTPError as err:
            print(f"Erreur HTTP: {err}")
            
        except Exception as e:
            print(f"Erreur générale: {e}")



if __name__=="__main__":
    fetch_traffic_incidents()