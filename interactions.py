import requests, os

def click(click_num, page_url, user_id):
    entry = "e"


    entry = {
        'user_id' : user_id,
        'page_id' : page_url,
        'click_num' : click_num


    }

    r = requests.post(os.getenv('DB_URL') + "/user_clicks", json=entry)
    if r.status_code == 201:
        print(f"succesful, {r}")
    else:
        print(f"failed, {r}")

    return "Worked"