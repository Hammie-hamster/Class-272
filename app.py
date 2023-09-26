from flask import Flask, request, jsonify, render_template, send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename



app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/token')
def generate_token():
    #add your twilio credentials 
    TWILIO_ACCOUNT_SID = "ACe9367df6b269d530edcb061f47d38fcb"
    TWILIO_SYNC_SERVICE_SID = "IS13ce6cdead059929ed908052b2be2bb7"
    TWILIO_API_KEY = "SKa215b9a9c9d3e73e139898266e9e4631"
    TWILIO_API_SECRET = "8lvpIuQYY8noODsJb3aiUxkvOOhB6Cwf"

    username = request.args.get('username', fake.user_name())
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())






@app.route("/", methods = ["POST"])
def download_text():
    text_from_notepad = request.form["text"]
    with open("workfile.txt", "w") as f:
        f.write(text_from_notepad)
    
    path_to_store_txt = "workfile.txt"

    return send_file(path_to_store_txt, as_attachment = True)

if __name__ == "__main__":
    app.run(port=5001)

