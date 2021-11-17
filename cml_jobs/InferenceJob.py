!pip3 install -r requirements.txt

import cdsw, time, os, random, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from cmlbootstrap import CMLBootstrap
import seaborn as sns
import copy
from pyspark.sql import SparkSession
from pyspark.sql.types import *

### MODEL WARMUP ###

!pip3 install -r requirements.txt

import pandas as pd
import tensorflow as tf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from helpers import plot_decision_boundary

spark = SparkSession\
    .builder\
    .appName("PythonSQL")\
    .config("spark.hadoop.fs.s3a.s3guard.ddb.region","us-east-2")\
    .config("spark.yarn.access.hadoopFileSystems","s3a://gd01-uat2/")\
    .getOrCreate()

sparkDF = spark.sql("SELECT * FROM DEFAULT.circles")

df = sparkDF.toPandas()


# Get the various Model CRN details
HOST = os.getenv("CDSW_API_URL").split(":")[0] + "://" + os.getenv("CDSW_DOMAIN")
USERNAME = os.getenv("CDSW_PROJECT_URL").split("/")[6]
API_KEY = os.getenv("CDSW_API_KEY")
PROJECT_NAME = os.getenv("CDSW_PROJECT")

cml = CMLBootstrap(HOST, USERNAME, API_KEY, PROJECT_NAME)

# Get newly deployed churn model details using cmlbootstrapAPI
models = cml.get_models({})
churn_model_details = [
    model
    for model in models
    if model["creator"]["username"] == USERNAME
    and model["project"]["slug"] == PROJECT_NAME
][0]
latest_model = cml.get_model(
    {
        "id": churn_model_details["id"],
        "latestModelDeployment": True,
        "latestModelBuild": True,
    }
)

Model_CRN = latest_model["crn"]
Deployment_CRN = latest_model["latestModelDeployment"]["crn"]
model_endpoint = (
    HOST.split("//")[0] + "//modelservice." + HOST.split("//")[1] + "/model"
)

# This will randomly return True for input and increases the likelihood of returning
# true based on `percent`
def churn_error(item, percent):
    if random.random() < percent:
        return True
    else:
        return True if item == "Yes" else False


# Get 1000 samples
df_sample = df.sample(1000)

df_sample.groupby("label")["label"].count()

#df_sample_clean = (
#    df_sample.replace({"SeniorCitizen": {"1": "Yes", "0": "No"}})
#    .replace(r"^\s$", np.nan, regex=True)
#    .dropna()
#)

# Create an array of model responses.
response_labels_sample = []

# Run Similation to make 1000 calls to the model with increasing error
percent_counter = 0
percent_max = len(df_sample)

for record in json.loads(df_sample.to_json(orient="records")):
    print("Added {} records".format(percent_counter)) if (
        percent_counter % 50 == 0
    ) else None
    percent_counter += 1
    no_churn_record = copy.deepcopy(record)
    no_churn_record.pop("label")
    # **note** this is an easy way to interact with a model in a script
    
    rec = {'vals':[no_churn_record['X0'], no_churn_record['X1']]}
    response = cdsw.call_model(latest_model["accessKey"], rec)
    response_labels_sample.append(
        {
            "uuid": response["response"]["uuid"],
            "final_label": churn_error(record["label"], percent_counter / percent_max),
            "response_label": response["response"]["prediction"],
            "timestamp_ms": int(time.time() * 1000),
        }
    )

# The "ground truth" loop adds the updated actual label value and an accuracy measure
# every 100 calls to the model.
for index, vals in enumerate(response_labels_sample):
    print("Update {} records".format(index)) if (index % 50 == 0) else None
    cdsw.track_delayed_metrics({"final_label": vals["final_label"]}, vals["uuid"])
    if index % 100 == 0:
        start_timestamp_ms = vals["timestamp_ms"]
        final_labels = []
        response_labels = []
        response_probabs = []
    final_labels.append(int(vals["final_label"]))
    response_labels.append(int(vals["response_label"]))
    response_probabs.append(vals["response_label"])
    
    if index % 100 == 99:
        print("Adding accuracy metrc")
        end_timestamp_ms = vals["timestamp_ms"]
        accuracy = classification_report(
            final_labels, response_labels, output_dict=True
        )["accuracy"]
        cdsw.track_aggregate_metrics(
            {"accuracy": accuracy},
            start_timestamp_ms,
            end_timestamp_ms,
            model_deployment_crn=Deployment_CRN,
        )
        
        
### MODEL INFERENCE ###
        
import cdsw, time, os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import classification_report
from cmlbootstrap import CMLBootstrap
import seaborn as sns
import sqlite3

# Get newly deployed churn model details using cmlbootstrapAPI
HOST = os.getenv("CDSW_API_URL").split(":")[0] + "://" + os.getenv("CDSW_DOMAIN")
USERNAME = os.getenv("CDSW_PROJECT_URL").split("/")[6]  # args.username  # "vdibia"
API_KEY = os.getenv("CDSW_API_KEY")
PROJECT_NAME = os.getenv("CDSW_PROJECT")

cml = CMLBootstrap(HOST, USERNAME, API_KEY, PROJECT_NAME)

models = cml.get_models({})
churn_model_details = [
    model
    for model in models
    if model["creator"]["username"] == USERNAME
    and model["project"]["slug"] == PROJECT_NAME
][0]
latest_model = cml.get_model(
    {
        "id": churn_model_details["id"],
        "latestModelDeployment": True,
        "latestModelBuild": True,
    }
)

Model_CRN = latest_model["crn"]
Deployment_CRN = latest_model["latestModelDeployment"]["crn"]

# Read in the model metrics dict
model_metrics = cdsw.read_metrics(
    model_crn=Model_CRN, model_deployment_crn=Deployment_CRN
)

# This is a handy way to unravel the dict into a big pandas dataframe
metrics_df = pd.io.json.json_normalize(model_metrics["metrics"])
metrics_df.tail().T

# Write the data to SQL lite for visualization
if not (os.path.exists("model_metrics.db")):
    conn = sqlite3.connect("model_metrics.db")
    metrics_df.to_sql(name="model_metrics", con=conn)

# Do some conversions & calculations on the raw metrics
metrics_df["startTimeStampMs"] = pd.to_datetime(
    metrics_df["startTimeStampMs"], unit="ms"
)
metrics_df["endTimeStampMs"] = pd.to_datetime(metrics_df["endTimeStampMs"], unit="ms")
metrics_df["processing_time"] = (
    metrics_df["endTimeStampMs"] - metrics_df["startTimeStampMs"]
).dt.microseconds * 1000

# Create plots for different tracked metrics
sns.set_style("whitegrid")
sns.despine(left=True, bottom=True)

# Plot metrics.probability
#prob_metrics = metrics_df.dropna(subset=["metrics.probability"]).sort_values(
#    "startTimeStampMs"
#)
#sns.lineplot(
#    x=range(len(prob_metrics)), y="metrics.probability", data=prob_metrics, color="grey"
#)

# Plot processing time
time_metrics = metrics_df.dropna(subset=["processing_time"]).sort_values(
    "startTimeStampMs"
)
#sns.lineplot(
#    x=range(len(prob_metrics)), y="processing_time", data=prob_metrics, color="grey"
#)

# Plot model accuracy drift over the simulated time period
agg_metrics = metrics_df.dropna(subset=["metrics.accuracy"]).sort_values(
    "startTimeStampMs"
)
sns.barplot(
    x=list(range(1, len(agg_metrics) + 1)),
    y="metrics.accuracy",
    color="grey",
    data=agg_metrics,
)