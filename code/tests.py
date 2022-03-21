# This will list jobs in the project. By default it will list the first 10, and provide a next_page_token to list more if there are any. This behavior can be controlled by adding the keyword argument "page_size".

import cmlapi
import os
from cmlapi.utils import Cursor
from __future__ import print_function
import time
import cmlapi
from cmlapi.rest import ApiException
from pprint import pprint

!pip3 install -r requirements.txt

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import matplotlib.pyplot as plt
from pyspark.ml.pipeline import PipelineModel

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
sparkDF = spark.sql("SELECT * FROM spark_catalog.default.mlops_iceberg_table")

#Put open source model registry call here
mPath = "s3a://demo-aws-go02/data/newdir"
persistedModel = PipelineModel.load(mPath)

df_model = persistedModel.transform(sparkDF)




    
import random
import numpy as np
from pyspark.sql import Row
from sklearn import neighbors
from pyspark.ml.feature import VectorAssembler
from pyspark.mllib.stat import Statistics
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit
from pyspark.ml.feature import StringIndexer, VectorAssembler, StandardScaler
from pyspark.ml import Pipeline
from pyspark.mllib.stat import Statistics
from pyspark.ml.linalg import DenseVector
from pyspark.sql import functions as F

#Creates a Pipeline Object including One Hot Encoding of Categorical Features  
def make_pipeline(spark_df):        
     
    for c in spark_df.columns:
        spark_df = spark_df.withColumn(c, spark_df[c].cast("float"))
    
    stages= []

    cols = ['acc_now_delinq', 'acc_open_past_24mths', 'annual_inc', 'avg_cur_bal', 'funded_amnt']
    
    #Assembling mixed data type transformations:
    assembler = VectorAssembler(inputCols=cols, outputCol="features").setHandleInvalid("skip")
    stages += [assembler]    
    
    #Scaling features
    scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures", withStd=True, withMean=True)
    stages += [scaler]
    
    #Logistic Regression
    lr = LogisticRegression(featuresCol='scaledFeatures', labelCol='label', maxIter=100, regParam=0.0001, elasticNetParam=0.0001)
    stages += [lr]
    
    #Creating and running the pipeline:
    pipeline = Pipeline(stages=stages)
    pipelineModel = pipeline.fit(spark_df)

    return pipelineModel

pipelineModel = make_pipeline(train)