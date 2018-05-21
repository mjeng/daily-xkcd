from flask import Flask, request, render_template
import server_utils
import router

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def homepage():
    print(request.method)
    print(request.form)

    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        name = request.form["name"]
        number = request.form["phone"]
        timestr = server_utils.parse_validate_time(request.form["time"])
        submit_type = request.form["submit_type"]

        if submit_type == server_utils.TRY:
            router.run_once(name, number)
            return render_template("try.html", number=number)
        if submit_type == server_utils.SUB:
            router.add_db_entry(name, number, timestr)
            return render_template("sub.html", name=name)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
