import time
from clearml import Task

task = Task.init(
    project_name='DITLO_MLOps',
    task_name='dummy task',
    reuse_last_task_id=False
)
time.sleep(10)
