FROM apache/airflow:2.8.1-python3.8

USER root

# Install OpenJDK 17 (compatible with ARM64)
RUN apt-get update && apt-get install -y openjdk-17-jdk && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH="$JAVA_HOME/bin:$PATH"

USER airflow

# ...existing Airflow image setup...
