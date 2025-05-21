import json
import requests
from flask import Flask, request

app = Flask(__name__)

# Your verification token to be used in Meta Developer Portal
VERIFY_TOKEN = 'priyal'

# Your WhatsApp Business API access token
PAGE_ACCESS_TOKEN = 'EAAR3Q64BTQcBOyjpT3wNZBJT0ccdLG72bpfk5RRJM9oa74VcYN4H5CaGscjO6763HrApo0SiVc9Lowahj8PoDsgvd1G8niYsOaoZCwGUHEUS5mUXI5TZB2rOUMDIstV7SAOrNgURzaagSxZCmhO3PsZClQFm3kclLrkvu6EFR78hdkyv29OFJMBvErZA8oXk36dYIAOfGWO8YhuZANYU97WUIkJN8pk0wQZD'  # Replace with your actual access token


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Webhook verification (for Meta to confirm the webhook)
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("Webhook verified!")
            return challenge, 200
        else:
            return "Verification failed", 403

    elif request.method == 'POST':
        # Handle incoming messages (WhatsApp)
        data = request.get_json()
        print("Received POST data:", json.dumps(data, indent=4))  # For debugging

        # Check if the data object is from WhatsApp (meta sends this in the payload)
        if data.get('object') == 'whatsapp':
            for entry in data.get('entry', []):
                for messaging_event in entry.get('changes', []):
                    if 'value' in messaging_event:
                        value = messaging_event['value']
                        messages = value.get('messages', [])
                        for message in messages:
                            # WhatsApp message will have the 'from' field
                            sender_id = message['from']
                            if 'text' in message:
                                message_text = message['text']['body']
                                print(f"Received message: {message_text}")

                                # Send the message back as an echo
                                send_message(sender_id, f"You said: {message_text}")

        return "EVENT_RECEIVED", 200


def send_message(recipient_id, message_text):
    """Send a message back to the user via WhatsApp Business API"""
    url = f"https://graph.facebook.com/v22.0/661130447082661/messages"
    
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "to": recipient_id,  # WhatsApp recipient ID
        "text": {"body": message_text}
    }

    params = {"access_token": PAGE_ACCESS_TOKEN}  # Use your WhatsApp page access token

    response = requests.post(url, headers=headers, params=params, json=payload)
    print("Message sent:", response.status_code, response.text)


if __name__ == "__main__":
    app.run(debug=True)

