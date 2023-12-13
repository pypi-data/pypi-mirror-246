# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 20:22:44 2023

@author: kunth
"""
from __future__ import annotations
from abc import abstractmethod, ABC
import json
import requests

from telegrapi.method import Method

# Source: https://core.telegram.org/bots/api
# https://api.telegram.org/<<your_bot_api_token>>/sendMessage?chat_id=@<<channel_name>>&text=Hello



class TEngine:
    def __init__(self, token: str):
        self.token = token
        self.base_url = f'https://api.telegram.org/bot{token}'

    def send(self, message: TData) -> dict:
        global res
        url = f'{self.base_url}/{message.method}'
        res = requests.post(url, data=message.data, files=message.files)
        res = res.content.decode('utf-8')
        res = json.loads(res)
        return res



class TData(ABC):
    bot: TEngine
    chat_id: str
    _data: dict  = None
    _files: dict = None
    _method: Method = None
    _attatch_path:str = None
    _parse_mode:str = "HTML"
    
    @property
    def method(self) -> str:
        return self._method
    
    @property
    def data(self) -> dict:
        return self._data
    
    @property
    def files(self) -> dict:
        return self._files
    
    @abstractmethod
    def send(bot: TEngine): pass



class TText(TData):
    def __init__(self,bot: TEngine, text:str, chat_id:str=None, parse_mode:str='HTML'):
        super()
        self.bot = bot
        self._method = Method.sendMessage
        self.chat_id = chat_id
        self._parse_mode = parse_mode
        self._data = {
            'chat_id': self.chat_id,
            'parse_mode': self._parse_mode,
            'text': text,
        }
      
    def send(self):
        self.bot.send(self)



class TFile(TData):
    def __init__(self,bot: TEngine, filepath: str, caption:str=None, chat_id:str=None, parse_mode:str='HTML'):
        super()
        self.bot = bot
        self._method = Method.sendDocument
        self.chat_id = chat_id
        self._attatch_path = filepath
        self._parse_mode = parse_mode
        self._data = {
                'chat_id': self.chat_id,
                'parse_mode': self._parse_mode,
                'caption': caption,
            }
      
    def send(self):
        with open(self._attatch_path, 'rb') as f:
            self._files = { 'document': f }
            return self.bot.send(self)



class TVoice(TFile):
    def __init__(self,bot: TEngine, filepath: str, caption:str=None, chat_id:str=None, parse_mode:str='HTML'):
        super().__init__(bot, filepath, caption)
        self._method = Method.sendVoice

    def send(self):
        with open(self._attatch_path, 'rb') as f:
            data = f.read()
        self._files = {
            'voice': ('Message.ogg', data),
        }
        return self.bot.send(self)




# Factory
class Chat:
    
    chat_id: str
    
    def __init__(self, chat_id: str, bot: TEngine = None, parse_mode:str = 'HTML'):
        self.chat_id = chat_id
        self.parse_mode = parse_mode
        self.bot = bot
    
    def message(self, msg: str) -> TText:
        return TText(self.bot, msg, self.chat_id, self.parse_mode)
    
    def json(self, data:dict) -> TText:
        text = json.dumps(data, ensure_ascii=False, indent=4)
        return TText(self.bot, text, self.chat_id, self.parse_mode)
    
    def file(self, filepath: str, caption: str = None) -> TFile:
        return TFile(self.bot, filepath, caption,self.chat_id)

    def voice(self, filepath: str, caption: str = None) -> TVoice:
        return TFile(self.bot, filepath, caption,self.chat_id)



