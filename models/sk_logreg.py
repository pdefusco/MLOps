import cdsw, numpy, sklearn
from sklearn.linear_model import LogisticRegression


!pip3 install -r requirements.txt

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.ml.pipeline import PipelineModel
from joblib import dump, load

spark = SparkSession.builder\
  .appName("1.1 - Train Model") \
  .config("spark.hadoop.fs.s3a.s3guard.ddb.region", "us-east-2")\
  .config("spark.yarn.access.hadoopFileSystems", "s3a://demo-aws-go02")\
  .config("spark.jars","/home/cdsw/lib/iceberg-spark3-runtime-0.9.1.1.13.317211.0-9.jar") \
  .config("spark.sql.extensions","org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
  .config("spark.sql.catalog.spark_catalog","org.apache.iceberg.spark.SparkSessionCatalog") \
  .config("spark.sql.catalog.spark_catalog.type","hive") \
  .getOrCreate()

#Explore putting GE here
sparkDF = spark.sql("SELECT * FROM spark_catalog.default.mlops_iceberg_table LIMIT 100")

X = sparkDF.toPandas()
y = X["prediction"]
X = X.drop(columns=["prediction"])

clf = LogisticRegression(random_state=0).fit(X, y)
dump(clf, '/home/cdsw/models/logreg.joblib')