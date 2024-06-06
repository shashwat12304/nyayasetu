from flask import Flask, request, jsonify
import requests
import os
app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    print(f"The user data recieved is {data}\n")
    user_message = data['messages'][0]['text']['body']
    user_number = data['messages'][0]['from']
    response_message = handle_user_message(user_message)
    send_response=send_session_message(user_number, response_message)
    print(f"Response sent to user: {send_response}")
    return jsonify({'status': 'success'})

def handle_user_message(message):
    return f"Thank you for your {message}. How can we assist you?"

def send_session_message(to, message):
    url = "https://partners.pinbot.ai/v2/messages"
    headers = {
        "apikey": "bfa3bcfa-14ce-11ef-b22d-92672d2d0c2d",
        "Content-Type": "application/json",
        "wanumber": "917030207944"
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
