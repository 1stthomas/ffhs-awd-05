# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 15:26:52 2018

@author: ctsoft
"""

import ctsoft.awd.application.message as message
import ctsoft.awd.application.settings as settings
import ctsoft.awd.math.numerical as numerical
import ctsoft.awd.math.model as model


class Application(object):
    def __init__(self):
        self.__function = None
        self.__settings = settings.Settings()
        msgFilename = self.__settings.getFile('messages.xml')
        self.__message = message.Message(msgFilename)

    def calculateValues(self):
        results = []

        setIntegrageted = self.getIntegratedSettings()
        funcIntegrated = model.Function(**setIntegrageted)
        integrated = numerical.Integrated(funcIntegrated)
        resInt = integrated.calculate()
        results.append(resInt)

        settings = self.getFunctionSettings()
        function = model.Function(**settings)

        rectangle = numerical.Rectangle(function,
                                        integrated.getCalculatedValue())
        resRect = rectangle.calculate()
        results.append(resRect)

        trapezoid = numerical.Trapezoid(function,
                                        integrated.getCalculatedValue())
        resTrap = trapezoid.calculate()
        results.append(resTrap)

        simpson = numerical.Simpson(function,
                                    integrated.getCalculatedValue())
        resSim = simpson.calculate()
        results.append(resSim)

        self.printResults(results)

    def getFunction(self):
        if self.__function is None:
            self.__function = model.Function()

    def getFunctionSettings(self):
        return {'function': '4*r2*pi*(r1**2-x**2)**(1/2)',
                'rCircle': 1.0, 'rTorus': 2.0, 'steps': 10}

    def getIntegratedSettings(self):
        return {'function': '2*r2*r1**2*pi**2',
                'rCircle': 1.0, 'rTorus': 2.0, 'steps': 0}

    def printResults(self, results):
        for result in results:
            calcType = result.getCalculationType()
            function = result.getFunction()
            funcString = function.getFunction()
            rCircle = function.getRCircle()
            steps = function.getSteps()
            calculated = result.getCalculatedValue()
            
            print('--------------------------------------')
            print('Calculation Type: ', calcType, 'method')
            print('Function: ', funcString)

            if calcType is 'integral':
                print('calculated: ', calculated)
            else:
                derivation = result.getDerivation()
                stepSize = 2.0 * rCircle / steps
                print('steps: ', steps)
                print('stepSize: ', stepSize)
                print('calculated: ', calculated)
                print('derivation: ', derivation, '%')

    def printWelcome(self):
        self.__message.printWelcome()

    def run(self):
        self.printWelcome()
        self.calculateValues()
