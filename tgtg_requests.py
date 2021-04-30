import requests
import json
import os
from tgtg_io import get_tokens_from_file
from notify_run import Notify


def get_new_items(oldDict, newDict):
    newItemDict = newDict.copy()
    for key in oldDict:
        newItemDict.pop(key, None)
    return newItemDict


def send_to_notify_run(new_items, endpoint):
    print("New magic boxes found! Check notify run channel!")
    notify = Notify(endpoint=endpoint[0])
    for item in new_items.values():
        name = item[0][1]
        loc = item[0][2]
        message = (
            "Magic Box @ "
            + str(name)
            + " "
            + loc
            + "!\n"
            + str(item[0][3])
            + " beschikbaar van "
            + str(item[0][0])
        )
        try:
            notify.send(message)
        except:
            time.sleep(5)
            send_to_notify_run(newItems)


def token_refresh():
    """
    Requests token refresh from server
    """
    _, refresh_token = get_tokens_from_file()
    url = "https://apptoogoodtogo.com/api/auth/v2/token/refresh"

    data = '{{"refresh_token": "{refresh_token}"}}'.format(refresh_token=refresh_token)

    response_dict, response_code = send_request(url=url, data=data)
    saveTokensToFile(response_dict)


def parse_dict(json_response):
    """
    Create python dict with relevant information from json respone of available items.
    """
    availible_dict = {}
    for item in json_response["items"]:
        if item["items_available"] > 0:
            data_list = []
            name = item["item"]["name"]
            id = item["item"]["item_id"]
            store_name = item["store"]["store_name"]
            address_line = item["store"]["store_location"]["address"]["address_line"]
            availibility = item["items_available"]
            data_list.append([name, store_name, address_line, availibility])
            availible_dict[id] = data_list
    return availible_dict


def get_fav_items(user_id):
    favs_url = "https://apptoogoodtogo.com/api/item/v7/"

    auth_token, _ = get_tokens_from_file()

    data = (
        '{"user_id":'
        + str(user_id)
        + ',"origin":{"latitude":52.379189,"longitude":4.899431},"radius":30.0,"page_size":100,"page":1,"discover":false,"favorites_only":true,"item_categories":[],"diet_categories":[],"pickup_earliest":null,"pickup_latest":null,"search_phrase":null,"with_stock_only":false,"hidden_only":false,"we_care_only":false}'
    )
    response_dict, response_code = send_request(
        url=favs_url, data=data, auth_token=auth_token
    )
    while response_code != 200:
        # Timeout, try again in 5 seconds
        if response_code == 408:
            print("Timeout error, trying again...")
            time.sleep(5)
            response_dict, response_code = send_request(
                url=favs_url, data=data, auth_token=auth_token
            )
        # Access token expired, try again after token refresh
        if response_code == 401 or response_code == 400:
            print("Access token expired, token refresh...")
            token_refresh()
            auth_token, _ = get_tokens_from_file()
            data = (
                '{"user_id":'
                + str(user_id)
                + ',"origin":{"latitude":52.379189,"longitude":4.899431},"radius":30.0,"page_size":100,"page":1,"discover":false,"favorites_only":true,"item_categories":[],"diet_categories":[],"pickup_earliest":null,"pickup_latest":null,"search_phrase":null,"with_stock_only":false,"hidden_only":false,"we_care_only":false}'
            )
            response_dict, response_code = send_request(
                url=favs_url, data=data, auth_token=auth_token
            )

    return parse_dict(response_dict)


def send_request(
    url="https://apptoogoodtogo.com/api/auth/v2/loginByEmail", data="", auth_token=""
):
    """
    Sends a http post request to the toogoodtogo server
    """
    if auth_token:
        hed = {
            "Host": "apptoogoodtogo.com",
            "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
            "accept-language": "nl-NL",
            "authorization": "Bearer " + auth_token,
            "content-type": "application/json; charset=utf-8",
            "accept-encoding": "gzip",
        }
    else:
        hed = {
            "Host": "apptoogoodtogo.com",
            "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
            "accept-language": "nl-NL",
            "content-type": "application/json; charset=utf-8",
            "accept-encoding": "gzip",
        }

    response = requests.post(url, data, headers=hed)

    response_dict = json.loads(response.content)
    response_code = response.status_code

    return response_dict, response_code
