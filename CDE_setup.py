### SETTING UP THE CDE CLI ###

import yaml
import os

!mkdir .cde

### Recreating Yaml file with your credentials:

dict_yaml = {"user" : os.environ["WORKLOAD_USER"], 
             "vcluster-endpoint": os.environ["CDE_VC_ENDPOINT"]}

with open(r'.cde/config.yaml', 'w') as file:
  documents = yaml.dump(dict_yaml, file)

### Manually upload the CDE CLI before running the below commands:

!mkdir /home/cdsw/.local/bin
!chmod 777 /home/cdsw/.local/bin
!mv cde /home/cdsw/.local/bin
!chmod 777 /home/cdsw/.local/bin/cde


### CREATE A PYTHON ENV FOR THE CDE JOB ###


## CDE has a rich CLI. For more on it you can follow the documentation here: https://docs.cloudera.com/data-engineering/cloud/use-resources/topics/cde-python-virtual-env.html 
## or refer to this demo by Curtis Howard: https://github.com/curtishoward/CDE_CLI_demo
 
## Enter the following commands in the terminal from this CML Session
  
#cde resource create --name cde-python-env-resource-mlops --type python-env --python-version python3

## Verify that the resource was created successfully

#cde resource list --filter name[rlike]cde-python-env-resource-mlops

## Upload the requirements file for the cde python env

#cde resource upload --name cde-python-env-resource-mlops --local-path ${HOME}/cde_requirements.txt --resource-path requirements.txt
  
## Check the status of the environment

#cde resource list-events --name cde-python-env-resource-mlops

## Create a second resource to store the files for the jobs
#cde resource create --name cde-file-resource-mlops --type files

## Upload the python files for the batch-load and the Airflow jobs to the resource

#cde resource upload --name cde-file-resource-mlops --local-path batch_load.py
#cde resource upload --name cde-file-resource-mlops --local-path mlops_airflow_config.py

## 

#cde job create --name batch-load --type spark \
#               --mount-1-prefix appFiles/ \
#              --mount-1-resource cde-file-resource-mlops \
#               --python-env-resource-name cde-python-env-resource-mlops \
#               --application-file /app/mount/appFiles/sklearn_dependency.py \
#               --conf spark.executorEnv.PYTHONPATH=/app/mount/appFiles/deps_udf.zip \
#               --py-file /app/mount/appFiles/deps_udf.zip



### CREATE THE AIRFLOW JOB IN THE CDE VIRTUAL CLUSTER ###

## Create a Spark Job using the custom python environment. This job will create and/or refresh the table with new data at each iteration. The purpose is to simulate new data batches being loaded.

#cde job create --type spark --application-file batch_load.py --python-env-resource-name cde-python-env-resource-mlops --name batch-load


## Create an Airflow Job. The purpose is to execute the batch refresh spark job and trigger model training in CML via the CML Airflow Operator



## The CML Operator for Airflow was created by Curtis Howard. For more on it please visit his github: 