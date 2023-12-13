# scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class Cosmograph:
    """
    Cosmograph is a class for scheduling asynchronous tasks using the apscheduler library.

    Usage Example:
    ```python
    from scheduler import Cosmograph, time_schedule, interval_schedule, date_schedule, on_shutdown

    # Use Cosmograph and scheduling methods as needed
    ```
    """
    
    # Create a shared instance of the scheduler
    scheduler = AsyncIOScheduler()
    scheduler.start()

    @classmethod
    def on_shutdown(cls):
        """
        Gracefully shut down the scheduler when the application is shutting down.
        """
        cls.scheduler.shutdown()

    @classmethod
    def time_schedule(cls, hour: int = 0, minute: int = 0, second: int = 0):
        """
        Decorator to schedule tasks based on a specific time using cron-like syntax.

        Args:
            hour (int): The hour of the day (0-23).
            minute (int): The minute of the hour (0-59).
            second (int): The second of the minute (0-59).

        Usage Example:
        ```python
        @time_schedule(hour=12, minute=30)
        async def my_scheduled_task():
            print("Task executed at 12:30 PM.")
        ```
        """
        def decorator(func):
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)

            cls.scheduler.add_job(wrapper, "cron", hour=hour, minute=minute, second=second)
            return wrapper

        return decorator

    @classmethod
    def interval_schedule(cls, seconds: int = 0, minutes: int = 0, hours: int = 0):
        """
        Decorator to schedule tasks based on regular intervals.

        Args:
            seconds (int): The interval in seconds.
            minutes (int): The interval in minutes.
            hours (int): The interval in hours.

        Usage Example:
        ```python
        @interval_schedule(minutes=15)
        async def my_repeating_task():
            print("Task executed every 15 minutes.")
        ```
        """
        def decorator(func):
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)

            cls.scheduler.add_job(wrapper, "interval", seconds=seconds, minutes=minutes, hours=hours)
            return wrapper

        return decorator

    @classmethod
    def date_schedule(cls, run_date):
        """
        Decorator to schedule tasks to run at a specific date and time.

        Args:
            run_date (str): The date and time in string format (e.g., "2023-01-01 00:00:00").

        Usage Example:
        ```python
        @date_schedule(run_date="2023-01-01 00:00:00")
        async def my_one_time_task():
            print("Task executed once at the specified date and time.")
        ```
        """
        def decorator(func):
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)

            cls.scheduler.add_job(wrapper, "date", run_date=run_date)
            return wrapper

        return decorator

# Create aliases for the scheduling methods for ease of use
time_schedule = Cosmograph.time_schedule
interval_schedule = Cosmograph.interval_schedule
date_schedule = Cosmograph.date_schedule
on_shutdown = Cosmograph.on_shutdown
