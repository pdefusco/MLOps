### Install the API

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


# cursor also supports search_filter
# cursor = Cursor(client.list_runtimes, 
#                 search_filter = json.dumps({"image_identifier":"jupyter"}))
cursor = Cursor(client.list_runtimes)
runtimes = cursor.items()
for rt in runtimes:
    print(rt.image_identifier)


### CREATE A JOB TO RETRAIN THE MODEL ###
    
    
# Create a job. We will create dependent/children jobs of this job, so we call this one a "grandparent job". The parameter "runtime_identifier" is needed if this is running in a runtimes project.
grandparent_job_body = cmlapi.CreateJobRequest(
    project_id = project_id,
    name = "grandparentJob",
    script = "analysis.py",
    kernel = "python3",
)
# Create this job within the project specified by the project_id parameter.
grandparent_job = client.create_job(grandparent_job_body, project_id)


### CREATE A JOB TO PUSH THE MODEL TO A REST ENDPOINT ###


# Create a dependent job by specifying the parent job's ID in the parent_job_id field.
parent_job_body = cmlapi.CreateJobRequest(
    project_id = project_id,
    name = "parentJob",
    script = "analysis.py",
    kernel = "python3",
    parent_job_id = grandparent_job.id
)
parent_job = client.create_job(parent_job_body, project_id)


### CREATE A JOB TO DO INFERENCE ON THE MODEL ###


# Create a job that is dependent on the job from the previous cell. This leads to a dependency chain of grandparent_job -> parent_job -> child_job. If grantparent_job runs and succeeds, then parent_job will trigger, and if parent_job runs and succeeds, child_job will trigger. This one uses a template script that does not terminate, so we'll have the opportunity to try stopping it later.
child_job_body = cmlapi.CreateJobRequest(
    project_id = project_id,
    name = "childJob",
    script = "entry.py",
    kernel = "python3",
    parent_job_id = parent_job.id
)
child_job = client.create_job(child_job_body, project_id)

# Create a job run for the specified job.
# If the job has dependent jobs, the dependent jobs will run after the job succeeds.
# In this case, the grandparent job will run first, then the parent job, and then the child job, provided each job run succeeds.
jobrun_body = cmlapi.CreateJobRunRequest(project_id, grandparent_job.id)
job_run = client.create_job_run(jobrun_body, project_id, grandparent_job.id)
run_id = job_run.id

