from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .jobs import *


def start():
    sheduler = BackgroundScheduler()
    #sheduler.add_job(load_ucras,IntervalTrigger(seconds=10),max_instances = 1)
    sheduler.add_job(close_started_games,IntervalTrigger(seconds=3),max_instances = 1)
    sheduler.start()
