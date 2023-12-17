# cordutils/__init__.py (Inside cordutils folder)
from .cordutils import MessageClient

def send_message(token, channel_id, content):
    # Create a MessageClient instance dynamically
    message_client_instance = MessageClient(token)
    
    # Assuming send_message can raise exceptions
    return message_client_instance.send_message(channel_id, content)
