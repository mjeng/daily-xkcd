import router
import clock_utils, server_utils

def execute_job():
    timestr = clock_utils.get_time()
    router.run(timestr)

server_utils.log("Scheduler executing")
execute_job()
