import requests
import random
class Chat:
    def __init__(self,telegram_api_url):
        self.messages = []
        self.telegram_api_url = telegram_api_url
        self.in_chat_users = {}
        self.icons = [
            "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔", "🐧", "🐦", "🐤", "🦆",
            "🦅", "🦉", "🦇", "🐺", "🐗", "🐴", "🦄", "🐝", "🐛", "🦋", "🐌", "🐞", "🐜", "🦟", "🦗", "🕷️", "🦂", "🐢", "🐍", "🦎",
            "🦖", "🦕", "🐙", "🦑", "🦐", "🦞", "🦀", "🐡", "🐠", "🐟", "🐬", "🐳", "🐋", "🦈", "🐊", "🐅", "🐆", "🦓", "🦍", "🦧",
            "🐘", "🦛", "🦏", "🐪", "🐫", "🦒", "🦘", "🐃", "🐂", "🐄", "🐎", "🐖", "🐏", "🐑", "🦙", "🐐", "🦌", "🐕", "🐩", "🦮",
            "🐕‍🦺", "🐈", "🐈‍⬛", "🐓", "🦃", "🦚", "🦜", "🦢", "🦩", "🕊️", "🐇", "🦝", "🦨", "🦡", "🦦", "🦥", "🐁", "🐀", "🐿️",
            "🦔", "🐾"
        ]

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
        
    async def in_chat(self, chat_id, text) -> None:
        text = "Currently in chat:\n\n"
        for username, (cid, icon) in self.in_chat_users.items():
            text += f"@{username} {icon}\n"

        self.send_message(chat_id, text[:-1])
        
        
        
        
    def get_user_icon(self) -> str:
        """Assigns a unique animal icon for each user."""
        icon = random.choice(self.icons)
        self.icons.remove(icon)
        return icon

    async def chat(self, chat_id, username, text) -> None:
        icon = self.get_user_icon(username)
        self.in_chat_users[username] = (chat_id, icon)
        text = "You are in chat now! Currently in chat:\n\n"

        for uname, (cid, icn) in self.in_chat_users.items():
            text += f"@{uname} {icn}\n"
            if cid != chat_id:
                self.send_message(cid, parse_mode=None)

        self.send_message(chat_id, parse_mode=None)
        return 0

    # async def exit(self, update, context) -> int:
    #     """Exits and ends the conversation."""
    #     username = update.message.from_user.username
    #     chat_id = update.message.chat_id

    #     self.send_message(chat_id, parse_mode=None)

    #     if username in self.in_chat_users:
    #         del self.in_chat_users[username]

    #     for uname, (cid, icon) in self.in_chat_users.items():
    #         if cid != chat_id:
    #             self.send_message(cid, parse_mode=None)

    #     return 0
    
    
    def start(self, chat_id):
        self.send_message(
            chat_id,
            "Welcome to smuhq bot! This bot is designed to better facilitate HQ!\n\n"
            "Available Commands:\n\n"
            "<strong>chat</strong>\n"
            "/chat - join a virtual chat group\n"
            "any message - broadcast message to those who are in chat\n"
            "/in_chat - list all users in chat\n"
            "/exit - exit chat group"
        )