# Image de base
FROM apache/airflow:2.6.0-python3.9

USER root

# Installer Java (exemple avec OpenJDK 11)
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean

# Définir JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"
COPY init_airflow.sh /opt/airflow/init_airflow.sh
RUN chmod +x /opt/airflow/init_airflow.sh

USER airflow
# Suite de ton Dockerfile
WORKDIR /opt/airflow

COPY requirements-airflow.txt /opt/airflow/requirements-airflow.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements-airflow.txt




