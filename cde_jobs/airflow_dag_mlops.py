from datetime import datetime, timedelta, timezone
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from cloudera.cdp.airflow.operators.cde_operator import CDEJobRunOperator
#from cloudera.cdp.airflow.operators.cdw_operator import CDWOperator


################## CML OPERATOR CODE START #######################
from airflow.exceptions import AirflowException
from airflow.models.baseoperator import BaseOperator
from airflow.hooks.http_hook import HttpHook
import time

class CMLJobRunOperator(BaseOperator):

    def __init__(
            self,
            project: str,
            job: str,
            **kwargs) -> None:
        super().__init__(**kwargs)
        self.project = project
        self.job = job

    def execute(self, context):
        job_label = '({}/{})'.format(self.project, self.job)

        get_hook = HttpHook(http_conn_id='cml_rest_api', method='GET')
        post_hook = HttpHook(http_conn_id='cml_rest_api', method='POST')
        projects_url = 'api/v2/projects'
        r = get_hook.run(endpoint=projects_url)
        projects = {p['name'] : p['id'] for p in r.json()['projects']} if r.ok else None
        
        if projects and self.project in projects.keys():
            jobs_url = '{}/{}/jobs'.format(projects_url, projects[self.project])
            r = get_hook.run(endpoint=jobs_url)
            jobs = {j['name'] : j['id'] for j in r.json()['jobs']} if r.ok else None
            
            if jobs and self.job in jobs.keys():
                runs_url = '{}/{}/runs'.format(jobs_url, jobs[self.job])
                r = post_hook.run(endpoint=runs_url)
                run = r.json() if r.ok else None
        
                if run:
                    status = run['status']
                    RUNNING_STATES = ['ENGINE_SCHEDULING', 'ENGINE_STARTING', 'ENGINE_RUNNING']
                    SUCCESS_STATES = ['ENGINE_SUCCEEDED']
                    POLL_INTERVAL = 10
                    while status and status in RUNNING_STATES:
                        run_id_url = '{}/{}'.format(runs_url, run['id'])
                        r = get_hook.run(endpoint=run_id_url)
                        status = r.json()['status'] if r.ok else None
                        time.sleep(POLL_INTERVAL)
                    if status not in SUCCESS_STATES:
                        raise AirflowException('Error while waiting for CML job ({}) to complete'
                            .format(job_label))
                else:
                    raise AirflowException('Problem triggering CML job ({})'.format(job_label))
            else:
                raise AirflowException('Problem finding the CML job ID ({})'.format(self.job))
        else:
            raise AirflowException('Problem finding the CML project ID ({})'.format(self.project))
################## CML OPERATOR CODE END #######################


default_args = {
    'owner': 'pauldefusco',
    'retry_delay': timedelta(seconds=5),
    'start_date': datetime(2021,1,1,1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

dag = DAG(
    'MLOps',
    default_args=default_args,
    schedule_interval='0 0 12 * *',
    catchup=False,
    is_paused_upon_creation=False
)





batch_load_job = CDEJobRunOperator(
    task_id='batch_load',
    retries=3,
    dag=dag,
    job_name='BatchLoad'
)

cml_job = CMLJobRunOperator(
    task_id='cml_job_task',
    project='MLOps',
    job='TrainModelJob', 
    dag=dag)

start = DummyOperator(task_id='start', dag=dag)
end = DummyOperator(task_id='end', dag=dag)



start >> batch_load_job >> cml_job >> end
