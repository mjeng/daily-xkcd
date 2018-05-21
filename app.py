from flask import Flask, request, render_template

app = Flask(__name__)
@app.route("/", methods=["POST"])
def homepage():
    # assert request.method == "POST" # not sure if this works
    print("we here")
    print(request.method)
    print(request.form)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
