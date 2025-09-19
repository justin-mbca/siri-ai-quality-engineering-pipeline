# Airflow + PySpark on Mac M2 (ARM64) Troubleshooting Guide

## 1. Docker Compose & Airflow Setup
- Use the official `apache/airflow:2.8.1-python3.8` image.
- Create a custom `Dockerfile` to install OpenJDK 17 for ARM64 compatibility:
  ```Dockerfile
  FROM apache/airflow:2.8.1-python3.8
  USER root
  RUN apt-get update && apt-get install -y openjdk-17-jdk && rm -rf /var/lib/apt/lists/*
  ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
  ENV PATH="$JAVA_HOME/bin:$PATH"
  USER airflow
  ```
- In `docker-compose.yml`, set:
  ```yaml
  platform: linux/arm64
  build: .
  environment:
    JAVA_HOME: /usr/lib/jvm/java-17-openjdk-arm64
    # ...other Airflow/PySpark variables...
  ```

## 2. Permissions & Docker Login
- Ensure your user owns the Docker config directory:
  ```bash
  sudo chown -R $USER ~/.docker
  ```
- Log in to Docker Hub with your Docker Desktop credentials:
  ```bash
  docker login
  ```

## 3. Building & Running
- Use these commands to build and start containers:
  ```bash
  docker compose down
  docker compose build
  docker compose up -d
  ```

## 4. Common Issues & Fixes
- **Java not found:** Use OpenJDK 17 and set `JAVA_HOME` to `/usr/lib/jvm/java-17-openjdk-arm64`.
- **Permission denied:** Fix with `sudo chown -R $USER ~/.docker`.
- **Docker credential errors:** Always log in as your regular user, not with `sudo`.
- **YAML errors:** Ensure all keys in `docker-compose.yml` are properly indented and environment variables use key-value mapping.

## 5. Airflow DAGs
- Mount your DAGs, source, and data directories in the container.
- Set `PYTHONPATH` and other environment variables as needed.
