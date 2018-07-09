# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 22:33:31 2018

@author: ctsoft
"""

import sympy
import ctsoft.awd.math.model as model


class Base(object):
    """
    Base class for the calculation objects.
    
    Methods
    -------
    calculate:
        Defines the used symbols of the calculation.
    getCalculatedValue:
        Returns the calculated value of the current method object.
    getFunction:
        Returns the function object of the current method object.
    setCalculatedValue:
        Sets the calculated value of the current method object.
    """
    def __init__(self, function):
        self.__function = function
        self.__calculatedValue = None

    def calculate(self):
        """
        Defines some sympy symbols used by the underlying calculation.
        
        Returns
        -------
        dict : Dictonary with the keys: x, r1 and r2.
        """
        # defines the abscissa
        x = sympy.Symbol('x')
        # defines the radius of the circle of the torus
        r1 = sympy.Symbol('r1')
        # defines the radius of the torus
        r2 = sympy.Symbol('r2')

        return {'x': x, 'r1': r1, 'r2': r2}

    def getCalculatedValue(self):
        """
        Returns the calculated value.
        
        Returns
        -------
        double : The calculated value of the current method.
        """
        return self.__calculatedValue

    def getFunction(self):
        """
        Returns the function object.
        
        Returns
        -------
        ctsoft.awd.math.model.Function : A data object with the needed values
            for the calculation.
        """
        return self.__function

    def setCalculatedValue(self, calculatedValue):
        """
        Sets the calculated value of the current method.
        """
        self.__calculatedValue = calculatedValue


class Numerical(Base):
    """
    Base class for the numerical method objects.
    """
    def __init__(self, function, referenceValue):
        super(Numerical, self).__init__(function)
        self.result = None
        self.__referenceValue = referenceValue

    def calculateDerivation(self, calculatedValue, referenceValue):
        """
        Calculates the derivation of the current method compared to the
        calculation with the exact integral (the referenceValue variable)
        
        Parameters
        ----------
        calculatedValue : double
            The calculated value of the current numerical method.
        referenceValue : double
            The calculated value of the exact integral.

        Returns
        -------
        double : The derivation of the calculated value compared to the
            exact integral.
        """
        derivation = round(100.0 * calculatedValue / referenceValue - 100.0, 1)
        return abs(derivation)

    def fillResult(self, function, calculatedValue, derivation):
        """
        Fills a result model object with the needed values.

        Parameters
        ----------
        function : ctsoft.awd.math.model.Function
            An model object with the needed values for the numerical
            integration.
        calculatedValue : double
            The calculated value of the current numerical integration.
        derivation : double
            The derivation of the current numerical integration.
        """
        return model.Result(function, calculatedValue, derivation)

    def getReferenceValue(self):
        """
        Returns the reference value coming from the calculation of the exact
        integral.
        
        Returns
        -------
        double : The reference value calculated by the exact integral.
        """
        return self.__referenceValue

    def getResult(self):
        """
        Returns the result mdel object of the current numerical integration.
        
        Returns
        -------
        ctsoft.awd.math.model.Result : The model with the important values
            of the current calculation.
        """
        return self.__result

    def setResult(self, result):
        """
        Sets the result model object of the current numerical integration.
        
        Parameters
        ----------
        ctsoft.awd.math.model.Result : The result model with the important
            values of the current calculation.
        """
        self.__result = result


class Integrated(Base):
    """
    Class for the exact integral calculation.
    """
    def __init__(self, function):
        super(Integrated, self).__init__(function)

    def calculate(self):
        """
        Calculates the exact integral.
        
        Returns
        -------
        ctsoft.awd.math.model.Origin : The result model with the important
            values of the current calculation.
        """
        # get the used symbols
        (x, r1, r2) = super(Integrated, self).calculate()

        # get the function with the needed values
        function = self.getFunction()
        funcString = function.getFunction()

        # Set the substitutions of the calculation. These are the variables
        # of the function string.
        substi = {x: 0.0, r1: 1.0, r2: 2.0}

        # Calculates the function string by replacing the defined symbols with
        # the corresponding values.
        calculated = sympy.sympify(funcString).evalf(subs=substi)
        # Sets the calculated value as object variable.
        self.setCalculatedValue(calculated)

        # defines the calculation type which will be used to decide, which
        # printing method will be used and to output this information also
        # as a part of the result summary.
        calcType = 'integral'
        # Creates the model for the output.
        result = model.Origin(calcType, function, calculated)

        return result


class Rectangle(Numerical):
    """
    Class for the numerical integration calculation by the rectangle method.
    """
    def __init__(self, function, referenceValue):
        super(Rectangle, self).__init__(function, referenceValue)

    def calculate(self):
        """
        Calculates the numerical integration by the rectangle method.
        
        Returns
        -------
        ctsoft.awd.math.model.Result : The result model with the important
            values of the current calculation.
        """
        # get the used symbols
        (x, r1, r2) = super(Rectangle, self).calculate()

        # get the function with the needed values
        function = self.getFunction()
        # Gets the function string.
        funcString = function.getFunction()
        # Gets the radius of the circle.
        rCircle = function.getRCircle()
        # Gets the radius of the Torus (see the documentation for further
        # information of this variable).
        rTorus = function.getRTorus()
        # Gets the number of steps to calculate the numerical integration.
        steps = function.getSteps()
        # Calculates the step size for the calculation (this is the symbol "h"
        # in the documentation)
        stepSize = 2.0 * rCircle / steps
        # Variable for the sum of each rectangle coming from the rectangle
        # method.
        summe = 0.0

        for step in range(0, steps):
            # Calculates the current abscissa value of the loop.
            xValue = (-1.0) * rCircle + stepSize * step
            # Set the substitutions of the calculation. These are the variables
            # of the function string.
            substi = {x: xValue, r1: rCircle, r2: rTorus}
            # Calculates the function string by replacing the defined symbols with
            # the corresponding values.
            funcValue = sympy.sympify(funcString).evalf(subs=substi)
            # Sum all calculated ordinate values.
            summe += funcValue

        # The calculated numerical integration value by the rectangle method.
        calculated = summe * stepSize

        # Gets the reference value coming from the exact integral.
        refValue = self.getReferenceValue()
        # Calculate the derivation compared by the exact integration.
        derivation = self.calculateDerivation(calculated, refValue)
        # Sets the calculated value as object variable.
        self.setCalculatedValue(calculated)

        # defines the calculation type which will be used to decide, which
        # printing method will be used and to output this information also
        # as a part of the result summary.
        calcType = 'rectangle'
        # Creates the model for the output.
        result = model.Result(calcType, function, calculated, derivation)
        self.setResult(result)

        return result


class Simpson(Numerical):
    """
    Class for the numerical integration calculation by the simpson method.
    """
    def __init__(self, function, referenceValue):
        super(Simpson, self).__init__(function, referenceValue)

    def calculate(self):
        """
        Calculates the numerical integration by the simpson method.
        
        Returns
        -------
        ctsoft.awd.math.model.Result : The result model with the important
            values of the current calculation.
        """
        # get the used symbols
        (x, r1, r2) = super(Simpson, self).calculate()

        # get the function with the needed values
        function = self.getFunction()
        # Gets the function string.
        funcString = function.getFunction()
        # Gets the radius of the circle.
        rCircle = function.getRCircle()
        # Gets the radius of the Torus (see the documentation for further
        # information of this variable).
        rTorus = function.getRTorus()
        # Gets the number of steps to calculate the numerical integration.
        steps = function.getSteps()
        # Calculates the step size for the calculation (this is the symbol "h"
        # in the documentation)
        stepSize = 2.0 * rCircle / steps
        # Variable for the sum of all odd steps ordinate values coming
        # from the trapezoid method without the first and last step.
        sumOdd = 0.0
        # Variable for the sum of all even steps ordinate values coming
        # from the trapezoid method without the first and last step.
        sumEven = 0.0
        # Variable for the sum of first and last ordinate values coming
        # from the trapezoid method without the first and last step.
        sumStartEnd = 0.0

        for step in range(0, steps + 1):
            # Calculates the current abscissa value of the loop.
            xValue = (-1.0) * rCircle + stepSize * step
            # Set the substitutions of the calculation. These are the variables
            # of the function string.
            substi = {x: xValue, r1: rCircle, r2: rTorus}
            # Calculates the function string by replacing the defined symbols with
            # the corresponding values.
            funcValue = sympy.sympify(funcString).evalf(subs=substi)
            if step == 0 or step == steps:
                sumStartEnd += funcValue
            elif step % 2 == 0:
                sumEven += funcValue
            else:
                sumOdd += funcValue

        # The calculated numerical integration value by the simpson method.
        calculated = stepSize / 3 * (sumStartEnd + 4 * sumOdd + 2 * sumEven)

        # Gets the reference value coming from the exact integral.
        refValue = self.getReferenceValue()
        # Calculate the derivation compared by the exact integration.
        derivation = self.calculateDerivation(calculated, refValue)
        # Sets the calculated value as object variable.
        self.setCalculatedValue(calculated)

        # defines the calculation type which will be used to decide, which
        # printing method will be used and to output this information also
        # as a part of the result summary.
        calcType = 'simpson'
        # Creates the model for the output.
        result = model.Result(calcType, function, calculated, derivation)
        self.setResult(result)

        return result


class Trapezoid(Numerical):
    """
    Class for the numerical integration calculation by the trapezoid method.
    """
    def __init__(self, function, referenceValue):
        super(Trapezoid, self).__init__(function, referenceValue)

    def calculate(self):
        """
        Calculates the numerical integration by the trapezoid method.
        
        Returns
        -------
        ctsoft.awd.math.model.Result : The result model with the important
            values of the current calculation.
        """
        # get the used symbols
        (x, r1, r2) = super(Trapezoid, self).calculate()

        # get the function with the needed values
        function = self.getFunction()
        # Gets the function string.
        funcString = function.getFunction()
        # Gets the radius of the circle.
        rCircle = function.getRCircle()
        # Gets the radius of the Torus (see the documentation for further
        # information of this variable).
        rTorus = function.getRTorus()
        # Gets the number of steps to calculate the numerical integration.
        steps = function.getSteps()
        # Calculates the step size for the calculation (this is the symbol "h"
        # in the documentation)
        stepSize = 2.0 * rCircle / steps
        # Variable for the sum of the first and last ordinate values coming
        # from the trapezoid method.
        # method.
        sumEdge = 0.0
        # Variable for the sum of all other ordinate values coming
        # from the trapezoid method.
        sumMiddle = 0.0

        for step in range(0, steps):
            # Calculates the current abscissa value of the loop.
            xValue = (-1.0) * rCircle + stepSize * step
            # Set the substitutions of the calculation. These are the variables
            # of the function string.
            substi = {x: xValue, r1: rCircle, r2: rTorus}
            # Calculates the function string by replacing the defined symbols with
            # the corresponding values.
            funcValue = sympy.sympify(funcString).evalf(subs=substi)

            if step == 0 or step == steps:
                sumEdge += funcValue
            else:
                sumMiddle += funcValue

        summe = 0.5 * sumEdge + sumMiddle
        # The calculated numerical integration value by the trapezoid method.
        calculated = stepSize * summe

        # Gets the reference value coming from the exact integral.
        refValue = self.getReferenceValue()
        # Calculate the derivation compared by the exact integration.
        derivation = self.calculateDerivation(calculated, refValue)
        # Sets the calculated value as object variable.
        self.setCalculatedValue(calculated)

        # defines the calculation type which will be used to decide, which
        # printing method will be used and to output this information also
        # as a part of the result summary.
        calcType = 'trapezoid'
        # Creates the model for the output.
        result = model.Result(calcType, function, calculated, derivation)
        self.setResult(result)

        return result
