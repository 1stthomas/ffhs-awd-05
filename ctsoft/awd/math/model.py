# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 18:47:46 2018

@author: ctsoft
"""


class Function(object):
    def __init__(self, function, rCircle, rTorus, steps):
        self.__function = function
        self.__rCircle = rCircle
        self.__rTorus = rTorus
        self.__steps = steps

    def getFunction(self):
        return self.__function

    def getRCircle(self):
        return self.__rCircle

    def getRTorus(self):
        return self.__rTorus

    def getSteps(self):
        return self.__steps


class Origin(object):
    def __init__(self, calcType, function, calculatedValue):
        self.__function = function
        self.__calculatedValue = calculatedValue
        self.__type = calcType

    def getCalculatedValue(self):
        return self.__calculatedValue

    def getCalculationType(self):
        return self.__type

    def getFunction(self):
        return self.__function


class Result(Origin):
    def __init__(self, calcType, function, calculatedValue, derivation):
        super(Result, self).__init__(calcType, function, calculatedValue)
        self.__derivation = derivation

    def getDerivation(self):
        return self.__derivation
