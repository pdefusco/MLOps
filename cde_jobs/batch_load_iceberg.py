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

#Explore putting GE here to unit test column types
try:
    df = spark.read.parquet('s3a://demo-aws-go02/datalake/pdefusco/LoanStats_2015_subset.parquet',   
        header=True,
        sep=',',
        nullValue='NA')
    
    df = df.limit(2000)
    
    #Creating table for batch load if not present
    df.writeTo("spark_catalog.default.mlops_batch_load_table").create()
    
except:
    sparkDF = spark.sql("SELECT * FROM spark_catalog.default.mlops_batch_load_table")

else:
    sparkDF = spark.sql("SELECT * FROM spark_catalog.default.mlops_batch_load_table")
    
    
print("Total row count in the target table before batch load")
sparkDF.count()

newBatchDF = sparkDF.sample(withReplacement=True, fraction=0.5)

newBatchDF.count()

#spark.sql("DROP TABLE IF EXISTS spark_catalog.default.mlops_staging_table")


#Explore putting GE here to unit test column types
try:
    newBatchDF.writeTo("spark_catalog.default.mlops_staging_table").create()
except:
    spark.sql("INSERT INTO spark_catalog.default.mlops_batch_load_table SELECT * FROM spark_catalog.default.mlops_staging_table").show()
else:
    spark.sql("INSERT INTO spark_catalog.default.mlops_batch_load_table SELECT * FROM spark_catalog.default.mlops_staging_table").show()

spark.sql("DROP TABLE IF EXISTS spark_catalog.default.mlops_staging_table")

print("Total row count in the target table after batch load")
print(sparkDF.count())