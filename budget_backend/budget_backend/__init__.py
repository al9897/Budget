
# This file will be compiled at the startup of Django 
# # All the tasks for the scheduler need to be put here #


# Run setup of django before importing unprepared apps 

import django
django.setup()

from apscheduler.schedulers.background import BackgroundScheduler
from .management.commands import RunSimulator


scheduler = BackgroundScheduler()


scheduler.add_job(RunSimulator.Run, 'interval', seconds=5)
scheduler.add_job(RunSimulator.Matcher, 'interval', seconds=5)
scheduler.start()
    
