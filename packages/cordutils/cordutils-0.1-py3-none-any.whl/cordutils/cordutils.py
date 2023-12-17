# cordutils/cordutils.py
import requests

class MessageClient:
    def __init__(self, token):
        self.base_url = "https://discord.com/api/v10/"
        self.headers = {"Authorization": f"{token}"}

    def send_message(self, channel_id, content):
        url = f"{self.base_url}channels/{channel_id}/messages"
        payload = {"content": content}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
