# Iceberg Spark runtime JAR download script
# Downloads iceberg-spark-runtime-3.3_2.12-1.4.2.jar to ./jars

curl -L -o ./jars/iceberg-spark-runtime-3.3_2.12-1.4.2.jar \
  https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.3_2.12/1.4.2/iceberg-spark-runtime-3.3_2.12-1.4.2.jar

echo "Downloaded iceberg-spark-runtime-3.3_2.12-1.4.2.jar to ./jars"
