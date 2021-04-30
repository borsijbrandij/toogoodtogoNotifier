import requests
import json

base_url = 'https://apptoogoodtogo.com/api/auth/v2/loginByEmail'
std_headers = {'Host': 'apptoogoodtogo.com', 'user-agent': 'TGTG/21.1.3 Dalvik/2.1.0 (Linux; U; Android 10; Mi 9T Pro Build/QQ3A.200805.001)', 'accept-language': 'nl-NL', 'content-type': 'application/json; charset=utf-8',
                                                 'accept-encoding': 'gzip'}

auth_token=''

def save_tokens_to_file(response):
    """
    Saves tokens to ./data/tokens.json
    """
    tokens = {}
    tokens['access_token'] = response['access_token']
    tokens['refresh_token'] = response['refresh_token']
    with open('./data/tokens.json', 'w') as f:
        json.dump(tokens, f)



def sendRequest(url, data, auth_token=''):

    if auth_token:
        hed = {'Host': 'apptoogoodtogo.com', 'user-agent': 'TGTG/21.1.3 Dalvik/2.1.0 (Linux; U; Android 10; Mi 9T Pro Build/QQ3A.200805.001)', 'accept-language': 'nl-NL', 'authorization': 'Bearer ' + auth_token, 'content-type': 'application/json; charset=utf-8',
               'accept-encoding': 'gzip'}
    else:
        hed = {'Host': 'apptoogoodtogo.com', 'user-agent': 'TGTG/21.1.3 Dalvik/2.1.0 (Linux; U; Android 10; Mi 9T Pro Build/QQ3A.200805.001)', 'accept-language': 'nl-NL', 'content-type': 'application/json; charset=utf-8',
               'accept-encoding': 'gzip'}

    response = requests.post(url, data, headers=hed)

    response_dict = json.loads(response.content)
    response_code = response.status_code

    return response_dict, response_code


def login(email, pw):
    data = '{{"device_type": "ANDROID", "email": "{email}" , "password": "{pw}" }}'.format(
        email=email, pw=pw)

    req = requests.Request('POST', base_url, headers={'Host': 'apptoogoodtogo.com', 'user-agent': 'TGTG/21.1.3 Dalvik/2.1.0 (Linux; U; Android 10; Mi 9T Pro Build/QQ3A.200805.001)', 'accept-language': 'nl-NL', 'content-type': 'application/json; charset=utf-8',
                                                 'accept-encoding': 'gzip'}, data=data)
    response, code = sendRequest(base_url, data)
    if code == 200:
        success = True
        save_tokens_to_file(response)
    else:
        success = False
    print(response)
    print(code)
    return success