#!/bin/bash
set -e
echo "Initialisation de la base de données Airflow..."
# Vérifier si le fichier airflow.db n'existe pas
if [ ! -f "/opt/airflow/airflow.db" ]; then
    # Initialiser la base de données Airflow
    airflow db init && \
    # Créer un utilisateur administrateur
    airflow users create \
        --username admin \
        --firstname admin \
        --lastname user \
        --role Admin \
        --email admin@example.com \
        --password admin
fi

