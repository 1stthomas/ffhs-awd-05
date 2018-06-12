# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 15:29:36 2018

@author: ctsoft
"""

import xml.etree.ElementTree as xmlee


class Information(object):
    def __init__(self):
        self.__informations = {}

    def getInfo(self, infoType):
        for info in self.__informations:
            infoId = info.attrib.get('id', '')
            if infoId == infoType:
                return info.text
        return ''

    def load(self, path):
        root = xmlee.parse(path).getroot()
        self.__informations = root.find('informations').findall('*')
