from clearml import Task
from clearml.automation import TaskScheduler


scheduler = TaskScheduler(sync_frequency_minutes=1)
get_data_task = Task.get_task(project_name='Project Data Scientist #1', task_name='get data')
scheduler.add_task(
    schedule_task_id=get_data_task.id,
    queue='CPU Queue',
    minute=1,
    execute_immediately=True
)
scheduler.start_remotely(queue='services')