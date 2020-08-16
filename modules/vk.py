import requests
import time
import json
from urllib.parse import urlencode

def get_token():
    app_id = 7412922
    oauth_url = 'https://oauth.vk.com/authorize'
    oauth_params = {
        'client_id': app_id,
        'display': 'page',
        'scope': 'friends, groups, stats, offline',
        'response_type': 'token',
        'v': '5.122'
    }
    print('?'.join((oauth_url, urlencode(oauth_params))))


def get_subs(group_screen_name, access_token):
    '''
    Функция возвращает количество подписчиков сообщества.
    '''
    try:
        URL = 'https://api.vk.com/method/groups.getById'
        params = {
            'group_id': group_screen_name,
            'fields': 'members_count',
            'access_token': access_token,
            'v': '5.122'
        }
        response = requests.get(URL, params=params)
        members_count = response.json()['response'][0]['members_count']
        return members_count
    except requests.exceptions.ReadTimeout:
        print("\n Переподключение к серверу. \n")
        time.sleep(3)   
        members_count = get_subs(group_screen_name, access_token)
        return members_count

# Следующие функции не реализованы в коде, но позволят расширить фукнкционал программы:

def get_group_id(group_screen_name, access_token):
    '''
    Функция возвращает уникальный ID группы ВК по её Screen name.
    (в некоторых методах API VK необходим именно ID группы, а не Screen name)
    '''
    try:
        URL = 'https://api.vk.com/method/utils.resolveScreenName'
        params = {
            'screen_name': group_screen_name,
            'fields': 'object_id',
            'access_token': access_token,
            'v': '5.122'
        }
        response = requests.get(URL, params=params)
        group_id = response.json()['response']['object_id']
        return group_id
    except requests.exceptions.ReadTimeout:
        print("\n Переподключение к серверу. \n")
        time.sleep(3)   
        group_id = get_group_id(group_screen_name, access_token)
        return group_id


def get_ban_list(group_id, access_token):
    '''
    Функция возвращает количество пользователей в бан-листе сообщества.
    ВАЖНО: необходим ID группы и токен модератора сообщества.
    '''
    try:
        URL = 'https://api.vk.com/method/groups.getBanned'
        params = {
            'group_id': group_id,
            'access_token': access_token,
            'v': '5.122'
        }
        response = requests.get(URL, params=params)
        banned_count = response.json()['response']['count']
        return banned_count
    except requests.exceptions.ReadTimeout:
        print("\n Переподключение к серверу. \n")
        time.sleep(3)   
        banned_count = get_ban_list(group_id, access_token)
        return banned_count