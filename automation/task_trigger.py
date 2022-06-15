from clearml import Task
from clearml.automation import TriggerScheduler

# Create the scheduler and make it poll quickly for demo purpose
scheduler = TriggerScheduler(
    pooling_frequency_minutes=1,
    sync_frequency_minutes=1,
    force_create_task_project='Project MLops',
    force_create_task_name='Scientist #1 Trigger'
)

# Get the pipeline ID that we want to clone when a new dataset version drops
training_pipeline = Task.get_task(
    task_id='2f0456be3f46481699fe4e2d700ec1e9'
)

# Add the actual trigger and enqueue the pipeline in services because we're
# cloning the pipelinecontroller. The controller itself will properly enqueue
# the different nodes itself.
scheduler.add_dataset_trigger(
    schedule_task_id=training_pipeline.id,
    schedule_queue='services',
    name='Scientist #1 New Data Training',
    trigger_project='Project Data Scientist #1',
    trigger_name='raw_asteroid_dataset'
)

# Start the scheduler
scheduler.start_remotely(queue='services')
