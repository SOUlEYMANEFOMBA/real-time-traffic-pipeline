FROM bitnami/spark:latest

# Installer les outils nécessaires
USER root
# #Créer un utilisateur dédié
# RUN groupadd -r spark && useradd -r -g spark spark

# # Changer les permissions sur le répertoire Spark
# RUN chown -R spark:spark /opt/bitnami/spark

# # Créer le répertoire /home/spark avec les bonnes permissions
# RUN mkdir -p /home/spark && chown spark:spark /home/spark

RUN apt-get update && \
    apt-get install -y wget python3 python3-pip git && \
    mkdir -p /usr/lib/jvm && \
    wget https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.14%2B9/OpenJDK11U-jdk_x64_linux_hotspot_11.0.14_9.tar.gz && \
    tar xzf OpenJDK11U-jdk_x64_linux_hotspot_11.0.14_9.tar.gz -C /usr/lib/jvm/ && \
    rm OpenJDK11U-jdk_x64_linux_hotspot_11.0.14_9.tar.gz && \
    ln -s /usr/lib/jvm/jdk-11.0.14+9 /usr/lib/jvm/java-11-openjdk-amd64

# Définir JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Configurer le PATH
ENV PATH="${JAVA_HOME}/bin:${PATH}"


# Créer un répertoire pour Ivy
RUN mkdir -p /root/.ivy2
# copier le requirement 
COPY requirements-spark.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements-spark.txt
# # Définir le répertoire de travail
# WORKDIR /app

# Commencer un shell interactif par défaut
CMD ["bash"]