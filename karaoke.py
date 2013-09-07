import os

from flask import Flask, render_template, jsonify

from twilio.rest import TwilioRestClient

app = Flask(__name__)

TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/call/')
def call():
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.calls.create(
        to="+15154512927",
        from_="+13198048229",
        url="http://kara-ok.herokuapp.com/response/"
    )
    return jsonify({"success": True})

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
