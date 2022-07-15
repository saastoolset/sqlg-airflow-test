"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
import os


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
t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)

t2 = BashOperator(task_id="sleep", bash_command="sleep 5", retries=3, dag=dag)

templated_command = """
    {% for i in range(2) %}
        echo "{{ ds }}"
        echo "TIMEZONE1: {{ (dag_run.logical_date.astimezone(dag.timezone)).strftime('%Y%m%d') }}"        
        echo "TIMEZONE2: {{ logical_date.in_timezone('Asia/Taipei') }}"        
        echo "TIMEZONE3: {{ logical_date.in_timezone('Asia/Taipei').strftime('%Y%m%d') }}"        
        echo "TIMEZONE4: {{ (logical_date.astimezone(dag.timezone)).strftime('%Y%m%d') }}"        
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

#  (execution_date.astimezone('Asia/Taipei')).strftime('%Y%m%d')
#  (logical_date.strftime('%Y%m%d'))
#  (logical_date.astimezone('Asia/Taipei')).strftime('%Y%m%d')
# (dag_run.logical_date.astimezone(dag.timezone)).strftime('%Y%m%d')
# .in_timezone('Asia/Taipei')
#        echo "TIMEZONE2: {{ (dag_run.logical_date.in_timezone('Asia/Taipei')).strftime('%Y%m%d') }}"        
#        echo "TIMEZONE2: {{ logical_date.in_timezone('Asia/Taipei') }}"        
# 


t3 = BashOperator(
    task_id="templated",
    bash_command=templated_command,
    params={"my_param": "Parameter I passed in"},
    dag=dag,
)

t1.dag=dag
t2.dag=dag
t3.dag=dag
t2.set_upstream(t1)
t3.set_upstream(t1)
