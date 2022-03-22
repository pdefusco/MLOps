!pip3 install -r requirements.txt

import cdsw, time, os, random, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cmlbootstrap import CMLBootstrap
import seaborn as sns
import copy
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import cmlapi
from src.api import ApiUtility
from sklearn.metrics import classification_report

from __future__ import print_function
import time
import cmlapi
from cmlapi.rest import ApiException
from pprint import pprint

### MODEL WARMUP ###

spark = SparkSession.builder\
  .appName("1.1 - Train Model") \
  .config("spark.hadoop.fs.s3a.s3guard.ddb.region", os.environ["REGION"])\
  .config("spark.kerberos.access.hadoopFileSystems", os.environ["STORAGE"])\
  .config("spark.jars","/home/cdsw/lib/iceberg-spark3-runtime-0.9.1.1.13.317211.0-9.jar") \
  .config("spark.sql.extensions","org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
  .config("spark.sql.catalog.spark_catalog","org.apache.iceberg.spark.SparkSessionCatalog") \
  .config("spark.sql.catalog.spark_catalog.type","hive") \
  .getOrCreate()

#Explore putting GE here
sparkDF = spark.sql("SELECT * FROM spark_catalog.default.mlops_batch_load_table LIMIT 300")

df = sparkDF.toPandas()

# You can access all models with API V2

client = cmlapi.default_client()

project_id = os.environ["CDSW_PROJECT_ID"]

# You can use an APIV2-based utility to access the latest model's metadata. For more, explore the src folder
apiUtil = ApiUtility()

Model_AccessKey = apiUtil.get_latest_deployment_details_allmodels()["model_access_key"]
Deployment_CRN = apiUtil.get_latest_deployment_details_allmodels()["latest_deployment_crn"]

# Get the various Model Endpoint details
HOST = os.getenv("CDSW_API_URL").split(":")[0] + "://" + os.getenv("CDSW_DOMAIN")
model_endpoint = (
    HOST.split("//")[0] + "//modelservice." + HOST.split("//")[1] + "/model"
)

# This will randomly return True for input and increases the likelihood of returning
# true based on `percent`
def label_error(item, percent):
    if random.random() < percent:
        return True
    else:
        return True if item == "Yes" else False

df.groupby("label")["label"].count()
#df = df.astype('str').to_dict('records')


# Create an array of model responses.
response_labels_sample = []

# Run Similation to make 1000 calls to the model with increasing error
percent_counter = 0
percent_max = len(df)

for record in json.loads(df.astype("str").to_json(orient="records")):
    print("Added {} records".format(percent_counter)) if (
        percent_counter % 50 == 0
    ) else None
    percent_counter += 1
    no_approve_record = copy.deepcopy(record)
    
    no_approve_record = {'acc_now_delinq': '1.0', 'acc_open_past_24mths': '2.0', 'annual_inc': '3.0', 'avg_cur_bal': '4.0', 'funded_amnt': '5.0'}
    
    # **note** this is an easy way to interact with a model in a script
    response = cdsw.call_model(Model_AccessKey, no_approve_record)
    response_labels_sample.append(
        {
            "uuid": response["response"]["uuid"],
            "final_label": label_error(record["label"], percent_counter / percent_max),
            "response_label": response["response"]["prediction"],
            "timestamp_ms": int(round(time.time() * 1000)),
        }
    )

#{
#    "model_deployment_crn": "crn:cdp:ml:us-west-1:8a1e15cd-04c2-48aa-8f35-b4a8c11997d3:workspace:f5c6e319-47e8-4d61-83bf-2617127acc36/d54e8925-a9e1-4d1f-b7f1-b95961833eb6",
#    "prediction": {
#        "input_data": "{'acc_now_delinq': '1.0', 'acc_open_past_24mths': '2.0', 'annual_inc': '3.0', 'avg_cur_bal': '4.0', 'funded_amnt': '5.0'}",
#        "prediction": "0.0"
#    },
#    "uuid": "7e3b3373-4487-4788-8b63-0ef8d9e9fa5c"
#}
    
    
    
# The "ground truth" loop adds the updated actual label value and an accuracy measure
# every 100 calls to the model.
for index, vals in enumerate(response_labels_sample):
    print("Update {} records".format(index)) if (index % 50 == 0) else None
    cdsw.track_delayed_metrics({"final_label": vals["final_label"]}, vals["uuid"])
    if index % 100 == 0:
        start_timestamp_ms = vals["timestamp_ms"]
        final_labels = []
        response_labels = []
    final_labels.append(vals["final_label"])
    response_labels.append(float(vals["response_label"]["prediction"]))
    if index % 100 == 99:
        print("Adding accuracy metrc")
        end_timestamp_ms = vals["timestamp_ms"]
        accuracy = classification_report(
            [float(i) for i in final_labels], response_labels, output_dict=True, zero_division=1
        )["accuracy"]
        cdsw.track_aggregate_metrics(
            {"accuracy": accuracy},
            start_timestamp_ms,
            end_timestamp_ms,
            model_deployment_crn=Deployment_CRN,
        )