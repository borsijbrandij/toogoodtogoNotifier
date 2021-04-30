import time
import getpass
from tgtg_requests import sendRequest
from notify_run import Notify
import os
import json

# Base url for tgtg API
base_url = "https://apptoogoodtogo.com/api/auth/v2/loginByEmail"


def save_tokens_to_file(response):
    """
    Saves tokens to ./data/tokens.json
    """
    tokens = {}
    tokens["access_token"] = response["access_token"]
    tokens["refresh_token"] = response["refresh_token"]
    if not os.path.exists("./data"):
        os.makedirs("./data")
    with open("./data/tokens.json", "w") as f:
        json.dump(tokens, f)


def setup_notify_run():
    # Setup notify run channel
    notify = Notify()
    notify.register()
    print(notify.info())

    # Save channel endpoint to file
    if not os.path.exists("./data"):
        os.makedirs("./data")
    f = open("./data/notify_channel.txt", "w")
    f.write(notify.endpoint)
    f.close()
    return notify.endpoint


def get_notify_run_channel():
    # Check if notify run channel has been setup, if not create one
    if os.path.isfile("./data/notify_channel.txt"):
        with open("./data/notify_channel.txt", "r") as channel_file:
            return channel_file.readlines()
    else:
        return setup_notify_run()


def login(email, pw):
    data = (
        '{{"device_type": "ANDROID", "email": "{email}" , "password": "{pw}" }}'.format(
            email=email, pw=pw
        )
    )

    response, code = sendRequest(base_url, data)
    if code == 200:
        success = True
        save_tokens_to_file(response)

    else:
        success = False
    notify_run_endpoint = get_notify_run_channel()
    return success, notify_run_endpoint


def first_setup():
    print("You have not logged in yet. Please enter your credentials")
    time.sleep(0.2)
    email = input("Enter email: ")
    pw = getpass.getpass()

    while not login(email, pw):
        print("Incorrect credentials, let's try again")
        email = input("Enter email: ")
        pw = getpass.getpass()
