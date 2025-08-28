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
    
    def send_message(self,chat_id, text, parse_mode=None):
        url = f"{self.telegram_api_url}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": text
        }
        if parse_mode:
            payload["parse_mode"] = parse_mode
        requests.post(url, json=payload)
        

        
        
    def in_chat(self, chat_id) -> None:
        text = "Currently in chat:\n\n"
        for username, (cid, icon) in self.in_chat_users.items():
            text += f"@{username} {icon}\n"

        self.send_message(chat_id, text[:-1])
        
        
        
        
    def get_user_icon(self) -> str:
        """Assigns a unique animal icon for each user."""
        icon = random.choice(self.icons)
        self.icons.remove(icon)
        return icon

    def chat(self, chat_id, username) -> None:
        if username in self.in_chat_users:
            self.send_message(chat_id, "You are already in chat.")
            return 0

        icon = self.get_user_icon()
        self.in_chat_users[username] = (chat_id, icon)
        text = "You are in chat now! Currently in chat:\n\n"

        for uname, (cid, icn) in self.in_chat_users.items():
            text += f"@{uname} {icn}\n"
            if cid != chat_id:
                self.send_message(cid, text=f"@{username} {icon} joined the chat")

        self.send_message(chat_id, text)
        return 0


    def exit(self, chat_id, username) -> int:
        if username not in self.in_chat_users:
            self.send_message(chat_id, "You are not in chat.")
            return -1

        text = "You have exited the chat."
        self.send_message(chat_id, text, parse_mode=None)

        self.icons.append(self.in_chat_users[username][1])
        del self.in_chat_users[username]

        for uname, (cid, icon) in self.in_chat_users.items():
            if cid != chat_id:
                text = f"@{username} {icon} exited the chat."
                self.send_message(cid, text)

        return 0
    
    def normal_message(self, chat_id, username, text) -> None:
        if username not in self.in_chat_users:
            self.send_message(chat_id, "You are not in chat. Use /chat to join the chat.")
            return
        chat_id, icon = self.in_chat_users.get(username)
        for uname, (cid, icn) in self.in_chat_users.items():
            if cid != chat_id:
                self.send_message(cid, text=f"@{username} {icon}:\n\n {text}")
    
    def start(self, chat_id):
        self.send_message(
            chat_id,
            "Welcome to smuhq bot! This bot is designed to better facilitate HQ!\n\n"
            "Available Commands:\n\n"
            "<strong>chat</strong>\n"
            "/chat - join a virtual chat group\n"
            "any message - broadcast message to those who are in chat\n"
            "/in_chat - list all users in chat\n"
            "/exit - exit chat group",
            parse_mode="HTML"
        )


    def forward_photo(self, chat_id, username, file_id, caption=None):
        if username not in self.in_chat_users:
            self.send_message(chat_id, "You are not in chat. Use /chat to join the chat.")
            return

        chat_id, icon = self.in_chat_users.get(username)

        url = f"{self.telegram_api_url}/sendPhoto"
        data = {
            "chat_id": chat_id,
            "photo": file_id
        }
        data["caption"] = f"@{username}{icon}"
        if caption:
            data["caption"] += f": {caption}"
        for uname, (cid, icn) in self.in_chat_users.items():
            if cid != chat_id:
                requests.post(url, json=data)
        
        return

    def forward_sticker(self, chat_id, username, file_id, caption=None):
        if username not in self.in_chat_users:
            self.send_message(chat_id, "You are not in chat. Use /chat to join the chat.")
            return

        chat_id, icon = self.in_chat_users.get(username)

        url = f"{self.telegram_api_url}/sendSticker"
        data = {
            "chat_id": chat_id,
            "sticker": file_id
        }
        data["caption"] = f"@{username}{icon}"
        if caption:
            data["caption"] += f": {caption}"
        for uname, (cid, icn) in self.in_chat_users.items():
            if cid != chat_id:
                self.send_message(cid, text=f"@{username}{icon} sent a sticker.")
                requests.post(url, json=data)
        return

    def forward_tele_bubble(self, chat_id, username, file_id, caption=None):
        if username not in self.in_chat_users:
            self.send_message(chat_id, "You are not in chat. Use /chat to join the chat.")
            return

        chat_id, icon = self.in_chat_users.get(username)

        url = f"{self.telegram_api_url}/sendVideoNote"
        # sendVideoNote uses the "video_note" field
        # Telegram's sendVideoNote doesn't support captions, so send a separate text announcement
        announce = f"@{username}{icon} sent a telebubble."
        if caption:
            announce += f": {caption}"

        for uname, (cid, icn) in self.in_chat_users.items():
            if cid != chat_id:
                # announce to each user
                self.send_message(cid, text=announce)
                # send the actual video note to each user
                requests.post(url, json={"chat_id": cid, "video_note": file_id})

        return

    def forward_video(self, chat_id, username, file_id, caption=None):
        if username not in self.in_chat_users:
            self.send_message(chat_id, "You are not in chat. Use /chat to join the chat.")
            return

        chat_id, icon = self.in_chat_users.get(username)

        url = f"{self.telegram_api_url}/sendVideo"
        data = {
            "chat_id": chat_id,
            "video": file_id
        }
        data["caption"] = f"@{username}{icon}"
        if caption:
            data["caption"] += f": {caption}"
        for uname, (cid, icn) in self.in_chat_users.items():
            if cid != chat_id:
                requests.post(url, json=data)

        return

    def forward_file(self, chat_id, username, file_id, caption=None):
        if username not in self.in_chat_users:
            self.send_message(chat_id, "You are not in chat. Use /chat to join the chat.")
            return

        chat_id, icon = self.in_chat_users.get(username)

        url = f"{self.telegram_api_url}/sendDocument"
        data = {
            "chat_id": chat_id,
            "document": file_id
        }
        data["caption"] = f"@{username}{icon}"
        if caption:
            data["caption"] += f": {caption}"
        for uname, (cid, icn) in self.in_chat_users.items():
            if cid != chat_id:
                requests.post(url, json=data)

        return

    def forward_voice(self, chat_id, username, file_id, caption=None):
        if username not in self.in_chat_users:
            self.send_message(chat_id, "You are not in chat. Use /chat to join the chat.")
            return

        chat_id, icon = self.in_chat_users.get(username)

        url = f"{self.telegram_api_url}/sendVoice"
        data = {
            "chat_id": chat_id,
            "voice": file_id
        }
        data["caption"] = f"@{username}{icon}"
        if caption:
            data["caption"] += f": {caption}"
        for uname, (cid, icn) in self.in_chat_users.items():
            # if cid != chat_id:
                requests.post(url, json=data)

        return