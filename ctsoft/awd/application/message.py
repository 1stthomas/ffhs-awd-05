# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 15:29:36 2018

@author: ctsoft
"""

import xml.etree.ElementTree as xmlee


class Message(object):
    def __init__(self):
        self.__messages = {}

    def getMessage(self, msgType):
        for msg in self.__messages:
            msgId = msg.attrib.get('id', '')
            if msgId == msgType:
                return msg.text
        return ''

    def load(self, path):
        root = xmlee.parse(path).getroot()
        self.__messages = root.find('messages').findall('*')
