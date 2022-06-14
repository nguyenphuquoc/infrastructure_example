# Training settings
import argparse
from asyncio import sleep
from clearml import Task
import time


def create_template():
    template_task = Task.init(
        project_name=args.project_name,
        task_name=f'template task',
    )
    template_task.close()

    return template_task

parser = argparse.ArgumentParser(description='Generate filler tasks')
subparsers = parser.add_subparsers(dest='command', help='sub-command help')

# Set the global var: project name
parser.add_argument('--project-name', type=str, required=True, help='Project name to perform operations on')

# Send filler tasks
send_parser = subparsers.add_parser(name='send', help='Send a bunch of filler tasks to the server')
send_parser.add_argument('--amount', type=int, default=2,
                    help='The amount of tasks to create PER QUEUE')
send_parser.add_argument('--queues', type=str, default=['default'], nargs='+',
                    help='Which queues to put filler tasks in')
send_parser.add_argument('--sleep-time', type=int, default=10,
                    help='Amount of time a single task will be active (time sleep) in seconds')

# Remove filler tasks
remove_parser = subparsers.add_parser(name='remove', help='Remove all active filler tasks from a project')

# Get the arguments
args = parser.parse_args()

if args.command == 'remove':
    filler_tasks = Task.get_tasks(
        project_name=args.project_name,
        task_name='example task*'
    )
    for task in filler_tasks:
        task.close()
        task.delete()
if args.command == 'send':
    for queue in args.queues:
        template_task = create_template()
        for i in range(args.amount):
            filler_task = template_task.clone(
                source_task=template_task.id,
                name=f'example task {i}'
            )
            filler_task.set_parameter('Args/command', 'run')
            Task.enqueue(filler_task, queue_name=queue)
        template_task.delete()
if args.command == 'run':
    time.sleep(args.sleep_time)