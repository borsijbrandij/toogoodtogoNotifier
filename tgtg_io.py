import json
from notify_run import Notify
import os


def check_notify_files_exist():
    return os.path.isfile("./data/notify_channel.txt")


def check_tokens_exist():
    return os.path.isfile("./data/tokens.json")


def get_tokens_from_file():
    """
    Loads tokens from tokens.json and returns them
    """
    with open("./data/tokens.json") as json_file:
        login_data = json.load(json_file)

    return login_data["access_token"], login_data["refresh_token"]


def get_user_id_from_file():
    """
    Loads user_id from tokens.json and returns them
    """
    with open("./data/tokens.json") as json_file:
        login_data = json.load(json_file)

    return login_data["user_id"]


def save_tokens_to_file(response):
    """
    Saves tokens and user_id to ./data/tokens.json
    """
    if response["access_token"] and response["refresh_token"]:
        tokens = {
            "access_token": response["access_token"],
            "refresh_token": response["refresh_token"],
            "user_id": response["startup_data"]["user"]["user_id"],
        }

        if not os.path.exists("./data"):
            os.makedirs("./data")
        with open("./data/tokens.json", "w") as f:
            json.dump(tokens, f)
        return True
    else:
        return False


def save_notify_run_settings(notify):
    """
    Save channel endpoint to file.
    """
    if not os.path.exists("./data"):
        os.makedirs("./data")
    f = open("./data/notify_channel.txt", "w")
    f.write(notify.endpoint)
    return


def get_notify_run_channel_disk():
    with open("./data/notify_channel.txt", "r") as channel_file:
        return channel_file.readlines()[0]
