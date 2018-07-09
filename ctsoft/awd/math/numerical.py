# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 22:33:31 2018

@author: ctsoft
"""

import sympy
import ctsoft.awd.math.model as model


class Base(object):
    def __init__(self, function):
        self.__function = function
        self.__calculatedValue = None

    def calculate(self):
        x = sympy.Symbol('x')
        r1 = sympy.Symbol('r1')
        r2 = sympy.Symbol('r2')
        return {'x': x, 'r1': r1, 'r2': r2}

    def getCalculatedValue(self):
        return self.__calculatedValue

    def getFunction(self):
        return self.__function

    def setCalculatedValue(self, calculatedValue):
        self.__calculatedValue = calculatedValue


class Numerical(Base):
    def __init__(self, function, referenceValue):
        super(Numerical, self).__init__(function)
        self.result = None
        self.__referenceValue = referenceValue

    def calculateDerivation(self, calculatedValue, referenceValue):
        derivation = round(100.0 * calculatedValue / referenceValue - 100.0, 1)
        return abs(derivation)

    def fillResult(self, function, calculatedValue, derivation):
        return model.Result(function, calculatedValue, derivation)

    def getReferenceValue(self):
        return self.__referenceValue

    def getResult(self):
        return self.__result

    def setResult(self, result):
        self.__result = result


class Integrated(Base):
    def __init__(self, function):
        super(Integrated, self).__init__(function)

    def calculate(self):
        x = sympy.Symbol('x')
        r1 = sympy.Symbol('r1')
        r2 = sympy.Symbol('r2')

        function = self.getFunction()
        funcString = function.getFunction()

        substi = {x: 0.0, r1: 1.0, r2: 2.0}

        calculated = sympy.sympify(funcString).evalf(subs=substi)
        self.setCalculatedValue(calculated)

        calcType = 'integral'
        result = model.Origin(calcType, function, calculated)

        print('--------------------------------------')
        print('Exact integral calculated: ', calculated)

        return result


class Rectangle(Numerical):
    def __init__(self, function, referenceValue):
        super(Rectangle, self).__init__(function, referenceValue)

    def calculate(self):
        (x, r1, r2) = super(Rectangle, self).calculate()
        function = self.getFunction()
        funcString = function.getFunction()
        rCircle = function.getRCircle()
        rTorus = function.getRTorus()
        steps = function.getSteps()
        stepSize = 2.0 * rCircle / steps
        summe = 0.0

        for step in range(0, steps):
            xValue = (-1.0) * rCircle + stepSize * step
            substi = {x: xValue, r1: rCircle, r2: rTorus}
            funcValue = sympy.sympify(funcString).evalf(subs=substi)
            summe += funcValue

        calculated = summe * stepSize

        refValue = self.getReferenceValue()
        derivation = self.calculateDerivation(calculated, refValue)
        self.setCalculatedValue(calculated)

        calcType = 'rectangle'
        result = model.Result(calcType, function, calculated, derivation)
        self.setResult(result)

        return result


class Simpson(Numerical):
    def __init__(self, function, referenceValue):
        super(Simpson, self).__init__(function, referenceValue)

    def calculate(self):
        (x, r1, r2) = super(Simpson, self).calculate()

        function = self.getFunction()
        funcString = function.getFunction()
        rCircle = function.getRCircle()
        rTorus = function.getRTorus()
        steps = function.getSteps()
        stepSize = 2.0 * rCircle / steps
        sumOdd = 0.0
        sumEven = 0.0
        sumStartEnd = 0.0

        for step in range(0, steps + 1):
            xValue = (-1.0) * rCircle + stepSize * step
            substi = {x: xValue, r1: rCircle, r2: rTorus}
            funcValue = sympy.sympify(funcString).evalf(subs=substi)
            if step == 0 or step == steps:
                sumStartEnd += funcValue
            elif step % 2 == 0:
                sumEven += funcValue
            else:
                sumOdd += funcValue

        calculated = stepSize / 3 * (sumStartEnd + 4 * sumOdd + 2 * sumEven)

        refValue = self.getReferenceValue()
        derivation = self.calculateDerivation(calculated, refValue)
        self.setCalculatedValue(calculated)

        calcType = 'simpson'
        result = model.Result(calcType, function, calculated, derivation)
        self.setResult(result)

        return result


class Trapezoid(Numerical):
    def __init__(self, function, referenceValue):
        super(Trapezoid, self).__init__(function, referenceValue)

    def calculate(self):
        (x, r1, r2) = super(Trapezoid, self).calculate()

        function = self.getFunction()
        funcString = function.getFunction()
        rCircle = function.getRCircle()
        rTorus = function.getRTorus()
        steps = function.getSteps()
        stepSize = 2.0 * rCircle / steps
        sumEdge = 0.0
        sumMiddle = 0.0

        for step in range(0, steps):
            xValue = (-1.0) * rCircle + stepSize * step
            substi = {x: xValue, r1: rCircle, r2: rTorus}
            funcValue = sympy.sympify(funcString).evalf(subs=substi)

            if step == 0 or step == steps:
                sumEdge += funcValue
            else:
                sumMiddle += funcValue
            print('xValue: ', xValue)

        summe = 0.5 * sumEdge + sumMiddle
        calculated = stepSize * summe

        refValue = self.getReferenceValue()
        derivation = self.calculateDerivation(calculated, refValue)
        self.setCalculatedValue(calculated)

        calcType = 'trapezoid'
        result = model.Result(calcType, function, calculated, derivation)
        self.setResult(result)

        return result
