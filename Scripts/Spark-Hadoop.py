from pyspark.sql import SparkSession
import os
os.environ["HADOOP_HOME"] = "C:\\Hadoop"


spark = SparkSession.builder \
    .appName("DynamicPricing") \
    .config("spark.hadoop.fs.s3a.access.key", "Your access key") \
    .config("spark.hadoop.fs.s3a.secret.key", "Your secret key") \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.2") \
    .getOrCreate()
