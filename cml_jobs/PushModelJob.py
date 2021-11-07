!pip3 install -r requirements.txt

import os
cluster = os.getenv("CDSW_DOMAIN")

# If you are not on a TLS enabled cluster (your cluster url starts with ‘http’),
# please use the following command instead.
# !pip3 install http://{cluster}/api/v2/python.tar.gz
!pip3 install https://{cluster}/api/v2/python.tar.gz

  
from cmlapi.utils import Cursor
import cmlapi
import string
import random
import json

try:
    client = cmlapi.default_client()
except ValueError:
    print("Could not create a client. If this code is not being run in a CML session, please include the keyword arguments \"url\" and \"cml_api_key\".")

session_id = "".join([random.choice(string.ascii_lowercase) for _ in range(6)])
session_id

# List projects using the default sort and default page size (10)
client.list_projects()

project_id = "p4b4-1yyp-flae-ag2z" 

# cursor also supports search_filter
# cursor = Cursor(client.list_runtimes, 
#                 search_filter = json.dumps({"image_identifier":"jupyter"}))
cursor = Cursor(client.list_runtimes)
runtimes = cursor.items()
for rt in runtimes:
    print(rt.image_identifier)

### CREATE AN ENDPOINT AND PUSH THE TF MODEL ###

modelReq = cmlapi.CreateModelRequest(
    name = "demo-model-" + session_id,
    description = "model created for demo",
    project_id = project_id,
)
model = client.create_model(modelReq, project_id)

model_build_request = cmlapi.CreateModelBuildRequest(
    project_id = project_id,
    model_id = model.id,
    comment = "test comment",
    file_path = "models/model_endpoint.py",
    function_name = "predict",
    kernel = "python3"
    #runtime_identifier = "docker.repository.cloudera.com/cdsw/ml-runtime-workbench-python3.8-standard:2021.02.1-b2"

)
modelBuild = client.create_model_build(
    model_build_request, project_id, model.id
)

model_deployment = cmlapi.CreateModelDeploymentRequest(
        project_id = project_id, 
        model_id = model.id, 
        build_id = modelBuild.id
    )

model_deployment_response = client.create_model_deployment(
        model_deployment, 
        project_id = project_id, 
        model_id = model.id, 
        build_id = modelBuild.id
    )
