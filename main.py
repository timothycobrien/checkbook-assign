from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import json
import ast

# received from sandbox
API_KEY = "7987fefcfe2c444faa773a51a3844532"
API_SECRET = "u73zig5Z7C1JtE4V2emWNlqZwZp1ak"
AUTH = API_KEY + ":" + API_SECRET
URL = "https://sandbox.checkbook.io/v3/check/digital"

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def handle():
    body = request.values.get("Body", None)

    # Send ${amount} to {name} ({email}) for {description}
    body_args = body.split(' ')
    # splitting at space [send, amount, to, name, (email), for, description]
    # need to flatten body_args[6..] into one entry
    body_args[6] = ' '.join(body_args[6:])
    header = {"content-type": "application/json", "accept": "application/json", "authorization": AUTH}
    
    # literal_eval needed to interface with api with number literal
    payload = json.JSONEncoder().encode({"recipient": (body_args[4])[1:-1], "name": body_args[3], "amount": ast.literal_eval((body_args[1])[1:]), "description": body_args[6]})

    r = requests.post(URL, data=payload, headers=header)

    resp = MessagingResponse()

    if r.status_code == 201:
        resp.message("Check successfully sent!")
    else:
        resp.message("Error sending check!")

    return str(resp)