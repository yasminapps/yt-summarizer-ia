from flask import Flask, render_template, request
from routes.summarize import summarize, get_transcript_only

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize_route():
    return summarize()

@app.route("/transcript", methods=["POST"])
def transcript_route():
    return get_transcript_only()

if __name__ == "__main__":
    app.run(debug=True, port=5005)
