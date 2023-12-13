# -*- coding: utf-8 -*-

import os
import requests
import json
from dotenv import load_dotenv


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


def ping(channel_username) -> dict:
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={channel_username}&text=Hello'
    res = requests.get(url)
    res = res.content.decode('utf-8')
    return json.loads(res)

if __name__ == '__main__':
    
    channel = '@votersc'
    res = ping(channel)