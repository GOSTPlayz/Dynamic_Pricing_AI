from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, month, dayofweek, sum as spark_sum, avg
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator
import pandas as pd
import os

# Set environment for winutils (optional if already set)
os.environ["HADOOP_HOME"] = "C:\\Hadoop"

# Initialize Spark
spark = SparkSession.builder \
    .appName("DynamicPricing_Predictions") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.11.1026") \
    .getOrCreate()

# Load Excel using pandas
df = pd.read_excel("online_retail_downloaded.xlsx", sheet_name="Year 2010-2011")
spark_df = spark.createDataFrame(df)

# Clean data
df_clean = spark_df.filter(
    (col("Price") > 0) &
    (col("Quantity") > 0) &
    (col("competitor_price") > 0)
).withColumn("InvoiceDate", to_timestamp("InvoiceDate"))

# Feature engineering
df_features = df_clean.withColumn("price_diff", col("Price") - col("competitor_price")) \
    .withColumn("month", month("InvoiceDate")) \
    .withColumn("day_of_week", dayofweek("InvoiceDate"))

# Aggregate data
agg_df = df_features.groupBy("StockCode", "month", "day_of_week").agg(
    spark_sum("Quantity").alias("total_quantity"),
    avg("Price").alias("avg_price"),
    avg("competitor_price").alias("avg_competitor_price"),
    avg("price_diff").alias("avg_price_diff")
)

# Filter out extreme outliers
agg_df_filtered = agg_df.filter(col("total_quantity") < 1000)

# Preserve important columns before transformation
df_model = agg_df_filtered.select(
    "StockCode", "month", "day_of_week", "total_quantity",
    "avg_price", "avg_competitor_price", "avg_price_diff"
)

# Assemble features
assembler = VectorAssembler(
    inputCols=["avg_price", "avg_competitor_price", "avg_price_diff", "month", "day_of_week"],
    outputCol="features"
)
df_model = assembler.transform(df_model)

# Split for training
train_df, test_df = df_model.randomSplit([0.8, 0.2], seed=42)

# Train Random Forest
rf = RandomForestRegressor(featuresCol="features", labelCol="total_quantity", numTrees=100)
rf_model = rf.fit(train_df)

# Predict
predictions = rf_model.transform(df_model)

# Evaluate
evaluator_rmse = RegressionEvaluator(labelCol="total_quantity", predictionCol="prediction", metricName="rmse")
evaluator_r2 = RegressionEvaluator(labelCol="total_quantity", predictionCol="prediction", metricName="r2")

rmse = evaluator_rmse.evaluate(predictions)
r2 = evaluator_r2.evaluate(predictions)

print(f"\nRandom Forest RMSE: {rmse:.2f}")
print(f"R² Score: {r2:.2f}")

# Select final results and save to CSV
result = predictions.select(
    "StockCode", "month", "day_of_week",
    "prediction", "total_quantity", "avg_competitor_price"
)
result.toPandas().to_csv("predicted_quantities.csv", index=False)
print(" Saved predictions to predicted_quantities.csv")
