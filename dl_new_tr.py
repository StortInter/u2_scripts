# -*- coding: utf-8 -*-

import datetime
import json
import os
import time

import pandas as pd
import requests


def request_get(url: str, params: dict):
    response = requests.get(url=url, params=params)
    return json.loads(response.text) if response.status_code == 200 else None


def get_new_torrents(uid: str, token: str, maximum: int = 25, simple: int = 2):
    url = 'https://u2.kysdm.com/api/v1/torrent'
    params = {
        'uid': uid,
        'token': token,
        'maximum': maximum,
        'simple': simple
    }
    response_dict = request_get(url=url, params=params)
    return response_dict['data']['torrent'] if response_dict is not None else None


def get_promotion_super(uid: str, token: str, torrent_id: str):
    url = 'https://u2.kysdm.com/api/v1/promotion_super'
    params = {
        'uid': uid,
        'token': token,
        'torrent_id': torrent_id
    }
    response_dict = request_get(url=url, params=params)
    return response_dict['data']['promotion_super'][0] if response_dict is not None else None


def get_torrent(passkey: str, torrent_id: str):
    url = 'https://u2.dmhy.org/download.php'
    headers = {
        'authority': 'u2.dmhy.org',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.8',
        'referer': 'https://u2.dmhy.org/index.php',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'
    }
    params = {
        'https': '1',
        'passkey': passkey,
        'id': torrent_id
    }
    response = requests.get(url=url, params=params, headers=headers)
    return response.content if response.status_code == 200 else None


def update_torrent_table(uid: str, token: str, tr_table: pd.DataFrame) -> pd.DataFrame:
    torrent_list = get_new_torrents(uid, token)

    for tr in torrent_list:
        tr_dict = {
            'torrent_id': tr['torrent_id'],
            'upload_time': datetime.datetime.strptime(tr['uploaded_at'], '%Y-%m-%dT%H:%M:%S'),
            'torrent_size': tr['torrent_size'],  # size in bytes
            'seeders': tr['seeders'],
            'leechers': tr['leechers'],
            'get_time': datetime.datetime.strptime(tr['get_time'], '%Y-%m-%dT%H:%M:%S')
        }
        # check if torrent_id exists in torrent_table
        if tr['torrent_id'] in tr_table['torrent_id'].values:
            continue
        # get magic
        promotion_super = get_promotion_super(uid, token, tr['torrent_id'])
        magic = promotion_super['private_ratio'].split('/')
        tr_dict['magic_upload'] = float(magic[0])
        tr_dict['magic_download'] = float(magic[1])
        tr_dict['magic_get_time'] = datetime.datetime.strptime(promotion_super['get_time'], '%Y-%m-%dT%H:%M:%S')
        tr_dict['checked'] = False
        tr_table.loc[len(tr_table)] = list(tr_dict.values())
        time.sleep(1)

    return tr_table


if __name__ == '__main__':
    if not os.path.exists('u2_personal_info.json'):
        print('u2_personal_info.json not found.')
        exit(-1)

    with open('u2_personal_info.json', 'r') as _f:
        config = json.load(_f)

    if config['token'] == '':
        print('Not get token, exit')
        exit(-1)
    if 'passkey' not in config or config['passkey'] == '':
        print('Not get passkey, exit')
        exit(-1)

    user_id = config['uid']
    user_token = config['token']
    user_passkey = config['passkey']

    # check if torrent_table.pkl exists
    if os.path.exists('torrent_table.pkl'):
        torrent_table = pd.read_pickle('torrent_table.pkl')
    else:
        torrent_table = pd.DataFrame(columns=[
            'torrent_id', 'upload_time', 'torrent_size', 'seeders', 'leechers', 'get_time',
            'magic_upload', 'magic_download', 'magic_get_time', 'checked'
        ])
