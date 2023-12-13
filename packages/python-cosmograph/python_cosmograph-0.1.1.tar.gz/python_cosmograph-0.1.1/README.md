# Cosmograph - Async Task Scheduler

Cosmograph is a  library for scheduling asynchronous tasks using the `apscheduler` library. It provides decorators to easily schedule tasks at specific times, intervals, or dates.

## Installation

```bash
pip install apscheduler
```

## Quick Start

```python
from scheduler import Cosmograph, time_schedule, interval_schedule, date_schedule, on_shutdown
```

Use Cosmograph and scheduling methods as needed

## Features

Schedule tasks at specific times using cron-like syntax.
Schedule tasks at regular intervals.
Schedule tasks to run at a specific date and time.
Gracefully shut down the scheduler when the application is shutting down.

## Usage

### Time Schedule

```python
@time_schedule(hour=12, minute=30)
async def my_scheduled_task():
    print("Task executed at 12:30 PM.")
```

### Interval Schedule

```python
@interval_schedule(minutes=15)
async def my_repeating_task():
    print("Task executed every 15 minutes.")

```

### Date Schedule

```python
@date_schedule(run_date="2023-01-01 00:00:00")
async def my_one_time_task():
    print("Task executed once at the specified date and time.")
```

### Graceful Shutdown

```python
# Perform this during application shutdown
on_shutdown()
```

## Contribution

Feel free to contribute by opening issues or creating pull requests. We welcome your feedback and contributions!

## License

This project is licensed under the MIT License AGPLv3 - see the LICENSE file for details.
