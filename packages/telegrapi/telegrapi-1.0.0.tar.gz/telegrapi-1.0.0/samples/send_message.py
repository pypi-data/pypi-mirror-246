# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
import json
from telegrapi import Chat, TEngine


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

        
if __name__ == '__main__':
    
    bot = TEngine(TELEGRAM_TOKEN)
    channel = Chat(CHAT_ID, bot)
    
    # to Text message into channel
    channel.message("This is a <b>bold</b> <i>text message</i>.").send()
    
    # to send file into channel
    filepath_to_send = "../telegrapi/api.py"
    caption='test sending file.'
    result = channel.file(filepath_to_send, caption).send()
    print(result)
    
    # to send text message into channel
    # message = json.dumps(result, ensure_ascii=False, indent=4)
    result = channel.json(result).send()
    print(result)
    

    # to send text message into channel
    voice_file = "./sample-voice.ogg"
    result = channel.voice(voice_file).send()
    print(result)
    