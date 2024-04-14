import os
import requests

class Subscription:
    def __init__(self, provider_id, title):
        self.provider_id = provider_id
        self.title = title

def get_subscriptions(user_id):
    subscriptions = []
    
    # Make the API request to fetch subscriptions
    r = requests.get(os.getenv('DB_URL') + "/subscriptions/" + str(user_id))
    
    if r.status_code == 200:
        data = r.json()  
        
        provider_titles = {
            1: "Netflix",
            6: "Hulu",
            3: "Disney+",
            2: "Prime",
            9: "Max"
        }
        
        for sub_data in data:
            provider_id = sub_data.get('provider_id')
            title = provider_titles.get(provider_id, "Unknown")  # Default to "Unknown" if provider_id not found
            subscription = Subscription(provider_id, title)
            subscriptions.append(subscription)
    else:
        print("Failed to fetch subscriptions. Status code:", r.status_code)
    
    return subscriptions
