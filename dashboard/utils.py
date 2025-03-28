import requests
from django.conf import settings

def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v18.0/{settings.META_WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {settings.META_WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,  # Must include country code (e.g., "91XXXXXXXXXX" for India)
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()
