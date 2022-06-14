# Training settings
import argparse
from html.entities import name2codepoint
from operator import sub
from clearml import Task


def dummy_task(sleep_time):
    import time
    time.sleep(sleep_time)

class TaskFactory:
    def __init__(self, project_name, task_name_prefix='example task', sleep_time=10):
        self.project_name = project_name
        self.task_name_prefix = task_name_prefix
        self.sleep_time = sleep_time
        self.task = Task.init(
            project_name=self.project_name,
            task_name=f'filler task factory'
        )

    def create_remote_task(self, task_name_suffix):
        self.task.create_function_task(dummy_task, task_name=f'{self.task_name_prefix} {task_name_suffix}', kwargs={'sleep_time': self.sleep_time})


parser = argparse.ArgumentParser(description='Generate filler tasks')
subparsers = parser.add_subparsers(dest='command', help='sub-command help')

# Set the global var: project name
parser.add_argument('--project-name', type=str, required=True, help='Project name to perform operations on')

# Send filler tasks
send_parser = subparsers.add_parser(name='send', help='Send a bunch of filler tasks to the server')
send_parser.add_argument('--amount', type=int, default=10,
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
    task_factory = TaskFactory(project_name=args.project_name, task_name_prefix='example task', sleep_time=args.sleep_time)
    for queue in args.queues:
        for i in range(args.amount):
            task_factory.create_remote_task(i)

