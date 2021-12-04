from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession\
    .builder\
    .appName("PythonSQL")\
    .config("spark.hadoop.fs.s3a.s3guard.ddb.region","us-east-2")\
    .config('spark.jars.packages', 'org.apache.iceberg:iceberg-core:0.11.0')\
    .config("spark.yarn.access.hadoopFileSystems","s3a://gd01-uat2/")\
    .config("spark.sql.catalog.spark_catalog=org.apache.iceberg.spark.SparkSessionCatalog")\
    .config("spark.sql.catalog.spark_catalog.type=hive")\
    .getOrCreate()

sparkDF = spark.sql("SELECT * FROM DEFAULT.circles")

newBatchDF = sparkDF.sample(withReplacement=True, fraction=0.5)

newBatchDF.write.insertInto('DEFAULT.circles_iceberg')


newBatchDF.write\
    .format("iceberg")\
    .mode("overwrite")\
    .save("db.table")\



#df_concat = newBatchDF.union(sparkDF)

newBatchDF.sortWithinPartitions("label").write.format("iceberg").insertInto("default.circles_iceberg")

#.mode("append").save("default.circles_iceberg")

newBatchDF.write.insertInto('DEFAULT.circles_iceberg')


#newBatchDF.write\
#    .format("iceberg")\
#   .mode("append")\
#    .save("DEFAULT.circles_iceberg")
    
#newBatchDF.write.insertInto("default.circles_iceberg")



# ds.sortWithinPartitions("state")
#    .write.format("iceberg")
#    .mode("append").save("default.ice_t")