# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 15:26:52 2018

@author: ctsoft
"""

import ctsoft.awd.application.information as information
import ctsoft.awd.application.settings as settings


class Application(object):
    def __init__(self):
        self.__settings = settings.Settings()
        self.__information = information.Information()

        self._setupInformations()

    def printWelcome(self):
        print(self.__information.getInfo('welcome-1'))
        print(self.__information.getInfo('welcome-2'))
        print(self.__information.getInfo('copyright'))

    def run(self):
        self.printWelcome()

    def _setupInformations(self):
        infoFilename = self.__settings.getFile('informations.xml')
        self.__information.load(infoFilename)
