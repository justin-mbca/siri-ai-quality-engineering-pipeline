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

## 6. Troubleshooting Pipeline Task Failures

- **Path Issues:**
  - Always use container paths (e.g., `/opt/airflow/data/...`) in your code, not host paths (e.g., `/Users/justin/...`).
  - Check that all volume mounts in `docker-compose.yml` match your code expectations.

- **Permissions:**
  - Ensure the Airflow container user (`airflow`) can write to all mounted directories.
  - Use `ls -ld` inside the container to verify directory ownership and permissions.

- **Iceberg Table Errors:**
  - If Spark/Iceberg fails to create files, clean up old/corrupted files in the warehouse directory.
  - Drop and recreate Iceberg tables using the correct container path.

- **Code Changes:**
  - Python code changes in mounted volumes are reflected immediately; no need to rebuild or restart Docker unless you change the image or mounts.

- **Debugging Output:**
  - Check Airflow task logs in the UI or via CLI for print statements and errors.
  - Inspect output files in the `data/` directory for each step (profile, SQL, ML, Iceberg).

- **General Tips:**
  - Restart Docker containers only if you change environment variables, mounts, or the Docker image.
  - Use Airflow CLI to trigger DAGs and check task states:
    ```bash
    docker compose exec airflow airflow dags trigger sample_pipeline
    docker compose exec airflow airflow tasks states-for-dag-run sample_pipeline <run_id>
    ```

- **Mac M2 Specifics:**
  - Always use ARM64-compatible images and dependencies.
  - If you see architecture errors, rebuild with `platform: linux/arm64` and check all dependencies.

---

For more details, see the main `README.md` and source code in `src/` and `dags/`.
