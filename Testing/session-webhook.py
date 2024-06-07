from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import json
load_dotenv()
app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    print(request.data)
    try:
        data = json.loads(request.data)
        if data is None:
            print("No JSON payload received.")
            return jsonify({'status': 'error', 'message': 'Invalid JSON payload'}), 400
        print(f"The user data received is {data}\n")

        # Navigate through the provided JSON schema
        entry = data.get('entry', [])
        if entry:
            changes = entry[0].get('changes', [])
            if changes:
                value = changes[0].get('value', {})
                messages = value.get('messages', [])
                if messages:
                    user_message = messages[0].get('text', {}).get('body', None)
                    print(user_message)
                    user_number = messages[0].get('from', None)
                    
                    if user_message is None or user_number is None:
                        print("Message body or user number is missing.")
                        return jsonify({'status': 'error', 'message': 'Invalid message format'}), 400
                    response_message = handle_user_message(user_message)
                    send_session_message(user_number, response_message)
                    res_msg = f"Response sent to user: {response_message}"
                    print(res_msg)
                    return jsonify({'status': 'success', 'msg': res_msg})
                else:
                    print("No messages found.")
                    return jsonify({'status': 'error', 'message': 'No messages found'}), 400
            else:
                print("No changes found.")
                return jsonify({'status': 'error', 'message': 'No changes found'}), 400
        else:
            print("No entry found.")
            return jsonify({'status': 'error', 'message': 'No entry found'}), 400
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



#SAMPLE REQUEST
# {
#   "object": "whatsapp_business_account",
#   "entry": [
#     {
#       "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
#       "changes": [
#         {
#           "value": {
#             "messaging_product": "whatsapp",
#             "metadata": {
#               "display_phone_number": "1234567890",
#               "phone_number_id": "PHONE_NUMBER_ID"
#             },
#             "contacts": [
#               {
#                 "profile": {
#                   "name": "John Doe"
#                 },
#                 "wa_id": "1234567890"
#               }
#             ],
#             "messages": [
#               {
#                 "from": "9910204981",
#                 "id": "wamid.ID",
#                 "timestamp": "TIMESTAMP",
#                 "text": {
#                   "body": "Hello, I need legal assistance."
#                 },
#                 "type": "text"
#               }
#             ]
#           },
#           "field": "messages"
#         }
#       ]
#     }
#   ]
# }

