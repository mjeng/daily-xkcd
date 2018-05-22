from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    print('This job is run every 10s.')

@sched.scheduled_job('cron', minute=0, timezone="US/Pacific")
def scheduled_job():
    print('This job is run at minute 00.')

@sched.scheduled_job('cron', minute=30, timezone="US/Pacific")
def scheduled_job():
    print('This job is run at minute 30.')

print("starting")
sched.start()
print("does it ever go here? :0")
