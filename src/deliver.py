
from pyspark.sql import SparkSession

def deliver_to_iceberg():
    spark = SparkSession.builder.appName('IcebergDelivery') \
        .config('spark.sql.catalog.demo', 'org.apache.iceberg.spark.SparkCatalog') \
        .config('spark.sql.catalog.demo.type', 'hadoop') \
    .config('spark.sql.catalog.demo.warehouse', '/opt/airflow/data/iceberg_warehouse') \
        .getOrCreate()
    # Read transformed data
    df = spark.read.csv('/opt/airflow/data/sample.csv', header=True, inferSchema=True)
    # Write to Iceberg table (demo.demo_table)
    df.writeTo('demo.demo_table').using('iceberg').createOrReplace()
    print('Delivered data to Iceberg table (actual Spark Iceberg integration).')

if __name__ == "__main__":
    deliver_to_iceberg()
