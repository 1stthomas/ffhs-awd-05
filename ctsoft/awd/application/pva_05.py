# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 15:26:52 2018

@author: ctsoft
"""

import ctsoft.awd.application.message as message
import ctsoft.awd.application.settings as settings


class Application(object):
    def __init__(self):
        self.__settings = settings.Settings()
        self.__message = message.Message()

        self._setupMessages()

    def printWelcome(self):
        print(self.__message.getMessage('welcome-1'))
        print(self.__message.getMessage('welcome-2'))
        print(self.__message.getMessage('copyright'))

    def run(self):
        self.printWelcome()

    def _setupMessages(self):
        msgFilename = self.__settings.getFile('messages.xml')
        self.__message.load(msgFilename)
