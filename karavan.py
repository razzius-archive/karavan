import os

from flask import Flask, render_template, jsonify

from twilio import twiml
from twilio.rest import TwilioRestClient
from twilio.util import TwilioCapability

app = Flask(__name__)

TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_SID = os.environ["TWILIO_SID"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/call/')
def call():
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.calls.create(
        to="+15154512927",
        from_="+13198048229",
        url="http://karavan.herokuapp.com/response/"
    )
    return jsonify({"success": True})

@app.route("/response/", methods=["GET", "POST"])
def respond():
    return render_template("response.xml")

@app.route("/client", methods=["GET", "POST"])
def client():
    capability = TwilioCapability(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    capability.allow_client_outgoing(TWILIO_SID)
    token = capability.generate()
    return render_template('client.html', token=token)

@app.route("/conference", methods=["POST"])
def conference():
    response = twiml.Response()
    with response.dial() as dial:
        dial.conference("HOT LINES")
    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
