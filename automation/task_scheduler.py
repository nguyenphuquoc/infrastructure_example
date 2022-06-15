from clearml import Task
from clearml.automation import TaskScheduler
from datetime import datetime


# Create the scheduler and make it poll quickly for demo purpose
scheduler = TaskScheduler(
    sync_frequency_minutes=1,
    force_create_task_project='Project MLops',
    force_create_task_name='NASA Scheduler'
)

# Get the task that we want to rerun
task_to_schedule = Task.get_task(project_name='Project Team NASA', task_name='get data')
# task_to_schedule = Task.get_task(task_id='2303bbd4c3284474a1b6545db8e2ee7f')

# Add the scheduler based on task above and override current date to get newest data
scheduler.add_task(
    schedule_task_id=task_to_schedule.id,
    queue='CPU Queue',
    hour=8,
    minute=30,
    weekdays=['friday'],
    execute_immediately=True,
    task_parameters={'Args/query_date': datetime.today().strftime('%Y-%m-%d')}
)

# Start the scheduler
scheduler.start_remotely(queue='services')