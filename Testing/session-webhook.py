from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import json
load_dotenv()
app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    try:
        data = request.json
        if data is None:
            print("No JSON payload received.")
            return jsonify({'status': 'error', 'message': 'Invalid JSON payload'}), 400
        print(f"The user data recieved is {data}\n")
        if 'messages' in data and len(data['messages']) > 0:
            user_message = data['messages'][0].get('text', {}).get('body', None)
            user_number = data['messages'][0].get('from', None)
            
            if user_message is None or user_number is None:
                print("Message body or user number is missing.")
                return jsonify({'status': 'error', 'message': 'Invalid message format'}), 400
            response_message = handle_user_message(user_message)
            send_session_message(user_number, response_message)
            res_msg=f"Response sent to user: {response_message}"
            print(res_msg)
            return jsonify({'status': 'success','msg':res_msg})
        else:
            print("Invalid message format.")
            return jsonify({'status': 'error', 'message': 'Invalid message format'}), 400
            
    except Exception as e:
        print(f"Error in webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def handle_user_message(message):
    try:
        return f"Thank you for your message: '{message}'. How can we assist you?"
    except Exception as e:
        print(f"Error in handle_user_message: {e}")
        return "Sorry, there was an error processing your message."

def send_session_message(to, message):
    try:
        url = "https://partners.pinbot.ai/v2/messages"
        headers = {
            "apikey": os.getenv("APIKEY"),
            "Content-Type": "application/json",
            "wanumber": os.getenv("WANUMBER")
        }
        payload = {
            "messaging_product": "whatsapp",
            "preview_url": False,
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {
            "body": message
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        print(f"Sending message to {to} with payload: {payload}")
        print(f"Response from Pinnacle API: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error in send_session_message: {e}")
        return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
