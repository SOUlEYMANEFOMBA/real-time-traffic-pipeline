FROM apache/airflow:2.6.0-python3.9

# Définir le répertoire de travail
WORKDIR /opt/airflow

# ## Copie le fichier requierements.txt
COPY requirements.txt /opt/airflow/requirements.txt
##Installer les dependances 
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
##Copie le scipt init_airflow dans le container

COPY init_airflow.sh /opt/airflow/init_airflow.sh
USER root
RUN chmod +x /opt/airflow/init_airflow.sh
# Revir à user airflow

USER airflow