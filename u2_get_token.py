# -*- coding: utf-8 -*-

import json
import os

import requests


def request_post(url: str, data: str):
    response = requests.post(url=url, headers={'Content-Type': 'application/json'}, data=data)
    return json.loads(response.text) if response.status_code == 200 else None


def get_authorization_key(uid: str):
    url = 'https://u2.kysdm.com/api/v1/token'
    post_info = {'uid': uid}
    response_dict = request_post(url=url, data=json.dumps(post_info))
    return response_dict['data']['key'] if response_dict is not None else None


def get_token(uid: str, key: str):
    url = 'https://u2.kysdm.com/api/v1/token'
    post_info = {'uid': uid, 'key': key}
    response_dict = request_post(url=url, data=json.dumps(post_info))
    return response_dict['data']['token'] if response_dict is not None else None


if __name__ == '__main__':
    # check if u2_personal_info.json exists
    if not os.path.exists('u2_personal_info.json'):
        print('u2_personal_info.json not found.')
        user_uid = input('Please input your u2 uid: ')
    else:
        with open('u2_personal_info.json', 'r') as f:
            config = json.load(f)

        if config['token'] != '':
            print('Already get token, exit')
            exit(1)

        user_uid = config['uid']

    auth_key = get_authorization_key(user_uid)
    if auth_key is None:
        print('Failed to get key.')
        exit(-1)

    print(f'Your token is:\n{auth_key}')

    # wait for write key to personal description
    # input 'done' to continue
    input_content = ''
    while input_content != 'done':
        input_content = input('input \'done\' to continue: ')

    auth_token = get_token(user_uid, auth_key)
    if auth_token is None:
        print('Failed to get token.')
        exit(-1)

    print(f'Your token is:\n{auth_token}')
    config['token'] = auth_token
    with open('u2_personal_info.json', 'w') as f:
        json.dump(config, f, indent=2)
    print('Token saved.')
