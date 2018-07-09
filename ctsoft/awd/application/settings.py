# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 15:53:38 2018

@author: ctsoft
"""

import xml.etree.ElementTree as xmlee


class Settings(object):
    def __init__(self):
        self.__filename = 'settings.xml'
        self.__settings = {}

        self._load()

    def get(self, settingType):
        return self.__settings.find(settingType)

    def getFile(self, filename):
        fileContainer = self.get('files')
        files = fileContainer.findall('file')

        for file in files:
            name = file.find('name')
            if name.text == filename:
                filePath = file.find('path').text
                if filePath == '/':
                    path = ''
                else:
                    path = filePath
                return path + filename
        return None

    def _load(self):
        root = xmlee.parse(self.__filename).getroot()
        self.__settings = root
