from clearml import Task
from clearml.automation import TaskScheduler
from datetime import datetime


# Create the scheduler and make it poll quickly for demo purpose
scheduler = TaskScheduler(
    sync_frequency_minutes=1,
    force_create_task_project='Project MLops',
    force_create_task_name='Scientist #1 Scheduler'
)

# Get the task that we want to rerun
get_data_task = Task.get_task(project_name='Project Data Scientist #1', task_name='get data')
today = datetime.today().strftime('%Y-%m-%d')

# Add the scheduler based on task above and override current date to get newest data
scheduler.add_task(
    schedule_task_id=get_data_task.id,
    queue='CPU Queue',
    hour=8,
    minute=30,
    weekdays=['friday'],
    execute_immediately=True,
    task_parameters={'General/query': f'SELECT * FROM asteroids WHERE strftime("%Y-%m-%d", `date`) <= strftime("%Y-%m-%d", "{today}")'}
)

# Start the scheduler
scheduler.start_remotely(queue='services')