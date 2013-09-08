import os

from flask import Flask, request, render_template, jsonify

from twilio import twiml
from twilio.rest import TwilioRestClient
from twilio.util import TwilioCapability

app = Flask(__name__)

TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_SID = os.environ["TWILIO_SID"]

caller_id = "+13198048229"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/call/')
def call():
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.calls.create(
        to="+15154512927",
        from_="+13198048229",
        url="http://hotlines.herokuapp.com/response/"
    )
    return jsonify({"success": True})

@app.route("/client/", methods=["GET", "POST"])
def client():
    capability = TwilioCapability(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    capability.allow_client_outgoing(TWILIO_SID)
    token = capability.generate()
    return render_template('client.html', token=token)

@app.route("/response/", methods=["GET", "POST"])
def respond():
    # Make the music play
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.calls.create(
        to="+13195943124",
        from_="+13198048229",
        url="http://hotlines.herokuapp.com/music/"
    )
    # Call my phone
    # response = twiml.Response()
    # with response.dial(calledId=caller_id) as r:
    #     r.number("+13195943124")
    # return str(response)
    response = twiml.Response()
    response.play("http://hotlines.herokuapp.com/static/mp3/indaclub.mp3")
    return str(response)

@app.route("/music/", methods=["GET", "POST"])
def music():
    response = twiml.Response()
    response.play("http://hotlines.herokuapp.com/static/mp3/indaclub.mp3")
    return str(response)

@app.route("/voice/", methods=['GET', 'POST'])
def voice():
    from_number = request.values.get('PhoneNumber', None)
    response = twiml.Response()
    with response.dial(callerId=caller_id) as r:
        r.number(from_number)
    return str(response)

@app.route("/conference/", methods=["POST"])
def conference():
    response = twiml.Response()
    with response.dial() as dial:
        dial.conference("HOT LINES")
    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
