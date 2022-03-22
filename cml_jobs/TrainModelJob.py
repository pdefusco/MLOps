!pip3 install -r requirements.txt

import pandas as pd
import numpy as np
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import matplotlib.pyplot as plt
from pyspark.ml.pipeline import PipelineModel

spark = SparkSession.builder\
  .appName("1.1 - Train Model") \
  .config("spark.hadoop.fs.s3a.s3guard.ddb.region", os.environ["REGION"])\
  .config("spark.yarn.access.hadoopFileSystems", os.environ["STORAGE"])\
  .config("spark.jars","/home/cdsw/lib/iceberg-spark3-runtime-0.9.1.1.13.317211.0-9.jar") \
  .config("spark.sql.extensions","org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
  .config("spark.sql.catalog.spark_catalog","org.apache.iceberg.spark.SparkSessionCatalog") \
  .config("spark.sql.catalog.spark_catalog.type","hive") \
  .getOrCreate()
#"spark.yarn.access.hadoopFileSystems" spark.kerberos.access.hadoopFileSystems
#Explore putting GE here
sparkDF = spark.sql("SELECT * FROM spark_catalog.default.mlops_batch_load_table") #mlops_batch_load_table

#Put open source model registry call here
mPath = os.environ["STORAGE"]+"/data/newdir"
persistedModel = PipelineModel.load(mPath)

df_model = persistedModel.transform(sparkDF)

#Push this method to utils 
def get_confusion_matrix(spark_df):

    input_data = spark_df.rdd.map(lambda x: (x["label"], x["prediction"], float(x["probability"][1])))
    predictions = spark.createDataFrame(input_data, ["label", "prediction", "probability"])

    y_true = predictions.select(['label']).collect()
    y_pred = predictions.select(['prediction']).collect()

    from sklearn.metrics import classification_report, confusion_matrix
    print(classification_report(y_true, y_pred))
    cf_matrix = confusion_matrix(y_true, y_pred, labels=None, sample_weight=None, normalize=None)
    
    import seaborn as sns
    group_names = ["True Neg","False Pos","False Neg","True Pos"]
    group_counts = ["{0:0.0f}".format(value) for value in
                    cf_matrix.flatten()]
    group_percentages = ["{0:.2%}".format(value) for value in
                         cf_matrix.flatten()/np.sum(cf_matrix)]
    labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in
              zip(group_names,group_counts,group_percentages)]
    labels = np.asarray(labels).reshape(2,2)
    sns.heatmap(cf_matrix, annot=labels, fmt="", cmap='Blues')

get_confusion_matrix(df_model)

try: 
    df_model.writeTo("spark_catalog.default.mlops_staging_scores_table").create()
    df_model.writeTo("spark_catalog.default.mlops_scores_table").create()
except:
    spark.sql("INSERT INTO spark_catalog.default.mlops_scores_table SELECT * FROM spark_catalog.default.mlops_staging_scores_table").show()
else:
    spark.sql("INSERT INTO spark_catalog.default.mlops_scores_table SELECT * FROM spark_catalog.default.mlops_staging_scores_table").show()

spark.sql("DROP TABLE IF EXISTS spark_catalog.default.mlops_staging_scores_table")