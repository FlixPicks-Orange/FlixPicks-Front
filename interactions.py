import requests, os

def add_click(event):
    entry = "e"

    entry = {
        'user_id' : 1,
        'page_id' : 1,
        'click_num' : 1


    }

    r = requests.post(os.getenv('DB_URL') + "/user_clicks", json=entry)
    if r == 201:
        print(f"succesful, {r}")
    else:
        print(f"failed, {r}")