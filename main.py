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
        "nord": "1.9,48.6,3.2,49.4",         # ≈ 9 900 km² – Paris, Meaux, Évry, Roissy  - couvre Paris, banlieue, A1, A6, A3, A4 — trafic dense assuré
        "sud_ouest": "-1.2,44.4,0.6,45.4",   # ≈ 9 600 km² – Couvre Bordeaux, Libourne, Langon, autoroutes A10 / A62 / A63
        "sud_est": "4.8,43.0,6.5,44.3" ,     # ≈ 9 900 km² – Marseille, Toulon, Aix, autoroutes A7 / A8 / A50
        "ouest": "-2.5,46.8,-0.5,48.2"       # ≈ 9 800 km² – Couvre Nantes, Rennes, Angers, et autoroutes A11 / A83
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
        
        # response = requests.get(api_url)
        
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