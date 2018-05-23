import router
import clock_utils, server_utils
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', minute=0, timezone="US/Pacific")
def scheduled_job():
    timestr = clock_utils.get_time()
    router.run(timestr)

@sched.scheduled_job('cron', minute=30, timezone="US/Pacific")
def scheduled_job():
    timestr = clock_utils.get_time()
    router.run(timestr)

server_utils.log("Scheduler starting")
sched.start()
