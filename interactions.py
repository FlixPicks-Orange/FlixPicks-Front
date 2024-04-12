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

def postLike(package, user_id, movie_id):
    r = requests.post(os.getenv('DB_URL') + f"/user_ratings/" + str(user_id) + "/movie/" + str(movie_id) + "/like", json=package)
    if r.status_code == 201:
        print('Succesfully updated Watch History.')
    return "Worked"

def postDislike(package, user_id, movie_id):
    r = requests.post(os.getenv('DB_URL') + f"/user_ratings/" + str(user_id) + "/movie/" + str(movie_id) + "/dislike", json=package)
    if r.status_code == 201:
        print('Succesfully updated Watch History.')
    return "Worked"