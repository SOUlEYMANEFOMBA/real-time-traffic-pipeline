FROM bitnami/spark:latest

# Passer en root pour installer les dépendances
USER root

# Installer les outils nécessaires + git
RUN apt-get update && \
    apt-get install -y wget python3 python3-pip git && \
    mkdir -p /usr/lib/jvm && \
    wget https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.14%2B9/OpenJDK11U-jdk_x64_linux_hotspot_11.0.14_9.tar.gz && \
    tar xzf OpenJDK11U-jdk_x64_linux_hotspot_11.0.14_9.tar.gz -C /usr/lib/jvm/ && \
    rm OpenJDK11U-jdk_x64_linux_hotspot_11.0.14_9.tar.gz && \
    ln -s /usr/lib/jvm/jdk-11.0.14+9 /usr/lib/jvm/java-11-openjdk-amd64

# Définir JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"





# Créer un répertoire pour Ivy, en tant qu'utilisateur patrick
RUN mkdir -p /root/.ivy2



# Démarrer avec un shell interactif
CMD ["bash"]

