from pyspark.sql import SparkSession

def transform_data():
    spark = SparkSession.builder.appName('Transform').getOrCreate()
    df = spark.read.csv('/opt/airflow/data/sample.csv', header=True, inferSchema=True)
    df = df.withColumn('value_doubled', df['value'] * 2)
    df.show()
    return df

if __name__ == "__main__":
    transform_data()
