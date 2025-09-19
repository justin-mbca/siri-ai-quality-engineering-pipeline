from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

def run_structured_streaming():
    spark = SparkSession.builder.appName('StructuredStreaming').getOrCreate()
    # Example: Read streaming data from a directory (file source)
    input_dir = '/opt/airflow/data/stream_input'
    from pyspark.sql.types import StructType, StructField, IntegerType, StringType
    schema = StructType([
        StructField('id', IntegerType(), True),
        StructField('value', StringType(), True)
    ])
    df = spark.readStream.option('header', True).schema(schema).csv(input_dir)
    # Windowed aggregation: count per value every 10 seconds
    from pyspark.sql.functions import col, count, length, avg, window
    from pyspark.sql.types import TimestampType
    import pyspark.sql.functions as F
    # Simulate event time by adding a timestamp column
    transformed_df = df.filter(col('id') > 3)\
        .withColumn('value_length', length(col('value')))\
        .withColumn('event_time', F.current_timestamp())

    # Deduplicate by id and value
    dedup_df = transformed_df.dropDuplicates(['id', 'value'])

    # Add watermark for event_time
    windowed_df = dedup_df.withWatermark('event_time', '30 seconds').groupBy(
        window(col('event_time'), '10 seconds'),
        col('value')
    ).agg(
        count('id').alias('count'),
        avg('value_length').alias('avg_length')
    )

    # Integrate Great Expectations data quality checks in each micro-batch
    def validate_and_write(batch_df, batch_id):
        import pandas as pd
        import great_expectations as ge
        # Convert Spark DataFrame to Pandas DataFrame
        pdf = batch_df.toPandas()
        if pdf.empty:
            print(f"Batch {batch_id}: Empty batch, skipping write.")
            return
        gdf = ge.from_pandas(pdf)
        # Example expectations
        result1 = gdf.expect_table_row_count_to_be_between(min_value=1, max_value=100000)
        result2 = gdf.expect_column_values_to_not_be_null('value')
        result3 = gdf.expect_column_values_to_be_in_set('count', set(range(0, 10000)))
        if result1['success'] and result2['success'] and result3['success']:
            print(f"Batch {batch_id}: Validation passed, writing to Parquet.")
            batch_df.write.mode('append').parquet('/opt/airflow/data/stream_output')
        else:
            print(f"Batch {batch_id}: Validation failed, skipping write.")

    query = windowed_df.writeStream.outputMode('append').foreachBatch(validate_and_write)\
    .option('checkpointLocation', '/opt/airflow/data/stream_output/_checkpoint')\
        .start()
    query.awaitTermination()

if __name__ == "__main__":
    run_structured_streaming()
