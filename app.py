from flask import Flask, request, jsonify, render_template
import os
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# 🔑 Authenticate Gmail once
def get_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


def send_email(subject, body_text):
    service = get_gmail_service()
    message = MIMEText(body_text)
    message['to'] = "YOUR_EMAIL@gmail.com"  # 📨 Replace this
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message = {'raw': raw}
    service.users().messages().send(userId="me", body=message).execute()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/send-quote', methods=['POST'])
def send_quote():
    data = request.json
    msg = f"""
    🧾 New Quote Request from Ole Hickory Site

    Name: {data.get('first_name')} {data.get('last_name')}
    Email: {data.get('email')}
    Phone: {data.get('phone')}
    Work Type: {data.get('work_type')}
    Area Size: {data.get('area_size')}
    Options: {data.get('options')}
    Zipcode: {data.get('zipcode')}
    """

    send_email("🌿 Ole Hickory Quote Request", msg)
    return jsonify({"status": "sent"})


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    msg = f"""
    💬 Chat Message from Website

    Message: {data.get('message')}
    """
    send_email("💬 Ole Hickory Live Chat Message", msg)
    return jsonify({"reply": "Thanks! We'll follow up soon via email."})


if __name__ == '__main__':
    app.run(debug=True)
