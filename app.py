from flask import Flask, render_template, request
from routes.summarize import summarize

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize_route():
    return summarize()

if __name__ == "__main__":
    app.run(debug=True, port=5002)
