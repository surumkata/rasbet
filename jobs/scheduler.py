from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .jobs import load_ucras


def start():
    sheduler = BackgroundScheduler()
    sheduler.add_job(load_ucras,IntervalTrigger(seconds=20),max_instances = 1)
    sheduler.start()
