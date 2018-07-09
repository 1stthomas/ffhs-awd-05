# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 15:29:36 2018

@author: ctsoft
"""

import xml.etree.ElementTree as xmlee


class Message(object):
    def __init__(self, filepath):
        self.__messages = {}
        self._load(filepath)

    def getMessage(self, msgType):
        for msg in self.__messages:
            msgId = msg.attrib.get('id', '')
            if msgId == msgType:
                return msg.text
        return ''

    def printWelcome(self):
        msgs = self._getWelcome()
        for msg in msgs:
            print(msg)

    def _getWelcome(self):
        msg = []
        msg.append(self.getMessage('welcome-1'))
        msg.append(self.getMessage('welcome-2'))
        msg.append(self.getMessage('copyright'))
        return msg

    def _load(self, path):
        root = xmlee.parse(path).getroot()
        self.__messages = root.find('messages').findall('*')
