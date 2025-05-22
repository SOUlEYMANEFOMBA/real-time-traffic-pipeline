import logging

class FormatDataTask:
    '''Cette tâche sert à mettre les données d'incident au bon format.'''

    def format_data(self, data_json):
        """
        Formate une liste de dictionnaires JSON en un format standardisé.

        Args:
            data_json (dict): Dictionnaire contenant une clé 'incidents' avec une liste d'incidents.

        Returns:
            list: Liste de dictionnaires formatés avec des clés spécifiques.

        Raises:
            KeyError: Si une clé attendue est absente (gérée avec .get pour éviter l'exception).
        """
        logging.info("Beginning of data format")

        incidents = data_json.get("incidents", [])
        
        if not incidents:
            logging.warning("Empty data received — no incident to process.")
            return []

        formatted_data = []

        for item in incidents:
            try:
                formatted = {
                    "type": item.get("type"),
                    "incident_id": item.get("properties", {}).get("id"),
                    "icon_category": item.get("properties", {}).get("iconCategory"),
                    "magnitude_of_delay": item.get("properties", {}).get("magnitudeOfDelay"),
                    "start_time": item.get("properties", {}).get("startTime"),
                    "end_time": item.get("properties", {}).get("endTime"),
                    "from_location": item.get("properties", {}).get("from"),
                    "to_location": item.get("properties", {}).get("to"),
                    "length_meters": item.get("properties", {}).get("length"),
                    "delay_seconds": item.get("properties", {}).get("delay"),
                    "time_validity": item.get("properties", {}).get("timeValidity"),
                    "geometry_type": item.get("geometry", {}).get("type"),
                    "coordinates": item.get("geometry", {}).get("coordinates")
                }
                formatted_data.append(formatted)
            except Exception as e:
                logging.error(f"Error while formatting item: {e}")

        logging.info(f"End of formatting. {len(formatted_data)} incidents formatted.")
        return formatted_data
