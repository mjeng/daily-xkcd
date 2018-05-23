import os
from flask import Flask, request, render_template
import server_utils
import router


###############################################
SERVER_ERR_MSGS = {
    server_utils.NAME_ERR: "your name input is too long. The character limit is 100.",
    server_utils.NUM_ERR: "the phone number you input isn't valid.",
    server_utils.TIME_ERR: "your time input was corrupted somehow. Refreshing might help.",
    server_utils.SUBMIT_ERR: "your submission was corrupted, somehow. Refreshing might help.",
}

ERR_VIEW = "err.html"
TRY_VIEW = "try.html"
SUB_VIEW = "sub.html"

SUCCESS = "completed"
FAILED = "failed"
NOTIFY = "TRUE"
###############################################

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def homepage():

    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        server_utils.log(request.form)
        name = request.form["name"]
        number = request.form["phone"]
        time = request.form["time"]
        submit_type = request.form["submit_type"]

        twilio_client = router.twilio_client
        err_code = server_utils.validate_inputs(name, number, twilio_client, time, submit_type)

        if err_code == server_utils.NO_ERR:
            pass
        else:
            err_msg = SERVER_ERR_MSGS[err_code]
            server_utils.log("Error code {0} with inputs NAME: {1} | NUMBER: {2} | TIME: {3} | SUBMIT_TYPE: {4}".format(err_code, name, number, time, submit_type))
            router.notify_matt(submit_type, name, number, time, FAILED)
            return render_template(ERR_VIEW, err_msg=err_msg)



        timestr = server_utils.parse_time(time)
        if submit_type == server_utils.TRY:
            router.run_once(name, number)
            if "NOTIFY" in os.environ.keys() and os.environ["NOTIFY"] == NOTIFY: # short-circuit check
                router.notify_matt(submit_type, name, number, time, SUCCESS)
            return render_template(TRY_VIEW, number=number)
        if submit_type == server_utils.SUB:
            router.add_db_entry(name, number, timestr)
            router.send_sub_confirmation(name, number, time)
            if "NOTIFY" in os.environ.keys() and os.environ["NOTIFY"] == NOTIFY:
                router.notify_matt(submit_type, name, number, time, SUCCESS)
            return render_template(SUB_VIEW, name=name)


    return render_template("index.html")


if __name__ == "__main__":
    app.run()
