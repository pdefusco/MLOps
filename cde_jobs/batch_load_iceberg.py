from pyspark.sql import SparkSession
from pyspark.sql.functions import *


#create version without iceberg extension options for CDE
spark = SparkSession.builder\
  .appName("0.2 - Batch Load into Icerberg Table") \
  .config("spark.hadoop.fs.s3a.s3guard.ddb.region", "us-east-2")\
  .config("spark.yarn.access.hadoopFileSystems", "s3a://demo-aws-go02")\
  .config("spark.jars","/home/cdsw/lib/iceberg-spark3-runtime-0.9.1.1.13.317211.0-9.jar") \
  .config("spark.sql.extensions","org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
  .config("spark.sql.catalog.spark_catalog","org.apache.iceberg.spark.SparkSessionCatalog") \
  .config("spark.sql.catalog.spark_catalog.type","hive") \
  .getOrCreate()

#Explore putting GE here
sparkDF = spark.sql("SELECT * FROM spark_catalog.default.mlops_original_table")

sparkDF.count()

newBatchDF = sparkDF.sample(withReplacement=True, fraction=0.5)

newBatchDF.count()

#spark.sql("DROP TABLE IF EXISTS spark_catalog.default.mlops_staging_table")

try:
  newBatchDF.writeTo("spark_catalog.default.mlops_staging_table").create()
except:
  spark.sql("INSERT INTO spark_catalog.default.mlops_original_table SELECT * FROM spark_catalog.default.mlops_staging_table").show()
else:
  spark.sql("INSERT INTO spark_catalog.default.mlops_original_table SELECT * FROM spark_catalog.default.mlops_staging_table").show()

sparkDF.count()