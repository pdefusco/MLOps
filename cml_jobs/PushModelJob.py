!pip3 install -r requirements.txt

import os
import cmlapi
from cmlapi.utils import Cursor
import string
import random
import json

cluster = os.getenv("CDSW_DOMAIN")

try:
    client = cmlapi.default_client()
except ValueError:
    print("Could not create a client. If this code is not being run in a CML session, please include the keyword arguments \"url\" and \"cml_api_key\".")

session_id = "".join([random.choice(string.ascii_lowercase) for _ in range(6)])
session_id

# List projects using the default sort and default page size (10)
client.list_projects(page_size = 20)

project_id = os.environ["CDSW_PROJECT_ID"]

### CREATE AN ENDPOINT AND PUSH THE TF MODEL ###

#Would be nice to name it with job id rather than session id
modelReq = cmlapi.CreateModelRequest(
    name = "demo-model-" + session_id,
    description = "model created for demo",
    project_id = project_id,
    disable_authentication = True
)

model = client.create_model(modelReq, project_id)

model_build_request = cmlapi.CreateModelBuildRequest(
    project_id = project_id,
    model_id = model.id,
    comment = "test comment",
    file_path = "models/model_endpoint.py",
    function_name = "predict",
    kernel = "python3",
    runtime_identifier = "docker.repository.cloudera.com/cdsw/ml-runtime-workbench-python3.7-standard:2021.09.1-b5"
    #runtime_addon_identifiers = "spark311-13-hf1"
)

modelBuild = client.create_model_build(
    model_build_request, project_id, model.id
)

model_deployment = cmlapi.CreateModelDeploymentRequest(
        project_id = project_id, 
        model_id = model.id, 
        build_id = modelBuild.id, 
        cpu = 1.00,
        memory = 2.00
    )

model_deployment_response = client.create_model_deployment(
        model_deployment, 
        project_id = project_id, 
        model_id = model.id, 
        build_id = modelBuild.id
    )
