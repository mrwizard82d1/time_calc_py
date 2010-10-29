#! python

"""Summarizes time into tasks."""


import argparse
from datetime import datetime
import sys


class Task(object):
    """Defines a task."""

    def __init__(self, start_line):
        """Constructs an instance from a text line describing its start."""
        day_text, time_point_text, name = start_line.split(None, 2)
        self.name = name.strip()
        year, month, day = [int(part) for part in ((day_text[0:4]),
                                                   (day_text[4:6]),
                                                   (day_text[6:]))]
        hour, minute = [int(part) for part in (time_point_text[0:2],
                                               time_point_text[2:])]
        self.start_time = datetime(year, month, day, hour, minute, 0)
        self.end_time = self.start_time

    def duration(self):
        """Determines the duration of this task."""
        return (self.end_time - self.start_time)
        
        
def make_tasks(infile):
    """Summarizes time into tasks."""

    # Create all the tasks
    task_lines = [l for l in infile.readlines() if len(l.strip()) > 0]
    result = [Task(l) for l in task_lines]

    # End of each task is the start of the next task
    end_times = [t.start_time for t in result[1:]]
    for task_ndx in range(len(end_times)):
        result[task_ndx].end_time = end_times[task_ndx]
        
    # Strip last "task."
    result = result[:-1]
    
    return result


def print_summary(summary):
    """Print a task duration summary."""
    names = summary.keys()
    names.sort()
    for name in names:
        hours = summary[name] // 3600
        minutes = (summary[name] % 3600) // 60
        duration = hours + (minutes / 60.0)
        print('{0:16}{1:.2f}'.format(name, duration))


def sum_time(tasks):
    """Summarizes the time for all similar tasks."""
    
    result = {}
    for t in tasks:
        result[t.name] = (result.get(t.name, 0) + t.duration().seconds)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser\
        (description='Summarize tasks into activities')
    parser.add_argument('infile', nargs='?',
                        type=argparse.FileType('r'),
                        help='File to read for input (default=stdin)',
                        default=sys.stdin)
    args = parser.parse_args()
    print_summary(sum_time(make_tasks(args.infile)))
