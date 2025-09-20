
from pyspark.sql import SparkSession

def deliver_to_iceberg(path):
    spark = SparkSession.builder.appName('IcebergDelivery') \
        .config('spark.sql.catalog.demo', 'org.apache.iceberg.spark.SparkCatalog') \
        .config('spark.sql.catalog.demo.type', 'hadoop') \
        .config('spark.sql.catalog.demo.warehouse', '/opt/airflow/data/iceberg_warehouse') \
        .config('spark.jars', '/opt/airflow/jars/iceberg-spark-runtime-3.3_2.12-1.4.2.jar') \
        .getOrCreate()
    # Read transformed data
    transformed_path = path.replace('.csv', '_transformed.csv')
    df = spark.read.csv(transformed_path, header=True, inferSchema=True)
    # Drop the Iceberg table if it exists (to reset any bad metadata)
    spark.sql('DROP TABLE IF EXISTS demo.siri_interactions')
    # Create the Iceberg table with the correct warehouse path
    df.writeTo('demo.siri_interactions').using('iceberg').create()
    print('Delivered Siri data to Iceberg table (Spark Iceberg integration, table recreated).')

if __name__ == "__main__":
    deliver_to_iceberg()
