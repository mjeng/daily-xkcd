from flask import Flask, request, render_template

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        pass # TODO: to be implemented
    print(request.method)
    print(request.form)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
