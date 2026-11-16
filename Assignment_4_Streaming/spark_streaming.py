"""
Spark Structured Streaming program
-----------------------------------
Source      : folder 'input_stream' (JSON files written by data_generator.py)
Processing  : average temperature + reading count per sensor, per 10-second window
Sink        : console
Fault tolerance:
  1. checkpointLocation -> Spark saves its progress (which files were read, and
     the running aggregation state). After a crash/restart it continues from
     where it stopped, with no data lost and no file processed twice.
  2. withWatermark      -> tells Spark how long to wait for late data, so the
     state does not grow forever.
  3. File source with a fixed schema -> files are replayable, so Spark can
     re-read them if a batch fails.
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, avg, count, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

spark = (
    SparkSession.builder
    .appName("SensorStreaming")
    .master("local[2]")
    .config("spark.sql.shuffle.partitions", "2")   # small data, so few partitions
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

# Streaming needs a schema up front
schema = StructType([
    StructField("sensor_id", StringType()),
    StructField("temperature", DoubleType()),
    StructField("event_time", StringType()),
])

# 1. READ the stream (one new file per micro-batch)
raw = (
    spark.readStream
    .schema(schema)
    .option("maxFilesPerTrigger", 1)
    .json("input_stream")
)

# 2. TRANSFORM
events = raw.withColumn("event_time", to_timestamp(col("event_time")))

result = (
    events
    .withWatermark("event_time", "20 seconds")
    .groupBy(window("event_time", "10 seconds"), "sensor_id")
    .agg(
        avg("temperature").alias("avg_temp"),
        count("*").alias("readings"),
    )
)

# 3. WRITE the stream, with a checkpoint for fault tolerance
query = (
    result.writeStream
    .outputMode("update")
    .format("console")
    .option("truncate", "false")
    .option("checkpointLocation", "checkpoint/sensor_job")
    .start()
)

query.awaitTermination()
