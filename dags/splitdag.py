"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
import os
import splitdag_jobs

tmp = os.path.basename(__file__)
tmp1 = os.path.splitext(tmp)[0]

filename = os.path.basename(__file__)
dag_name = os.path.splitext(filename)[0]


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2015, 6, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(dag_name, 
    default_args=default_args, 
    schedule_interval=timedelta(1),
    start_date=datetime(2015, 6, 1),    
    tags=[dag_name],
    )

# t1, t2 and t3 are examples of tasks created by instantiating operators
#t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)
#
#t2 = BashOperator(task_id="sleep", bash_command="sleep 20", retries=3, dag=dag)
#
#templated_command = """
#    {% for i in range(5) %}
#        echo "{{ ds }}"
#        echo "{{ macros.ds_add(ds, 7)}}"
#        echo "{{ params.my_param }}"
#    {% endfor %}
#"""
#
#t3 = BashOperator(
#    task_id="templated",
#    bash_command=templated_command,
#    params={"my_param": "Parameter I passed in"},
#    dag=dag,
#)
#
splitdag_jobs.t1.dag=dag
splitdag_jobs.t2.dag=dag
splitdag_jobs.t3.dag=dag
splitdag_jobs.t2.set_upstream(splitdag_jobs.t1)
splitdag_jobs.t3.set_upstream(splitdag_jobs.t1)
