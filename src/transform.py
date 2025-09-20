from pyspark.sql import SparkSession


def transform_data(path):
    spark = SparkSession.builder.appName('Transform').getOrCreate()
    df = spark.read.csv(path, header=True, inferSchema=True)
    # Normalize device_type
    from pyspark.sql.functions import lower, trim, when, col
    df = df.withColumn('device_type_norm', lower(trim(col('device_type'))))
    # Add latency bucket
    df = df.withColumn('latency_bucket',
        when(col('response_time_ms') < 300, 'fast')
        .when(col('response_time_ms') < 500, 'medium')
        .otherwise('slow'))
    # Add intent flag (e.g., is_weather_query)
    df = df.withColumn('is_weather_query',
        when(col('parsed_intent') == 'get_weather', 1).otherwise(0))
    df.show()
    # Save transformed data for downstream steps
    df.write.mode('overwrite').csv(path.replace('.csv', '_transformed.csv'), header=True)
    return df

if __name__ == "__main__":
    transform_data()
