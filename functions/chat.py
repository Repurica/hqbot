import requests
class Chat:
    def __init__(self,telegram_api_url):
        self.messages = []
        self.telegram_api_url = telegram_api_url

    def add_message(self, user, message):
        self.messages.append({'user': user, 'message': message})
        

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages = []
    
    def send_message(self,chat_id, parse_mode=None):
        url = f"{self.telegram_api_url}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": "\n".join([f"{msg['user']}: {msg['message']}" for msg in self.messages]),
        }
        if parse_mode:
            payload["parse_mode"] = parse_mode
        requests.post(url, json=payload)