# class for all the integration methods used

import numpy as np
import matplotlib.pyplot as plt
import math
from sympy import * 
from sympy import * 
init_printing()
from math import *
import sys
import time

class Integration: 


    def __init__(self, name):
         self.name = name  

    """
    INTEGRATION FUNCTIONS
    """

    def actual_integrate(expression, a, b):
        
        x = Symbol("x")
        
        actual = integrate(expression, (x, a, b))
        
        return actual.evalf()

    
    """
    RECTANGULAR INTEGRATION
    """



    def integrate_rectangular(a : float, b : float, Num : float, expression : str) -> float:
        
        """
        Returns the approximate area under the curve from a to b using
        the Rectangular Rule for numerical integration

        Parameters:
        ------------
        a : int
            start of the integration range
        b : int
            end of integration range
        Num : int
            number of intervals for integraton
        expression: str
            user entered function to be integrated over the range [a,b]

        Returns:
        --------
        float
            approximate area under the curve from a to b

        """
        start = time.time()
        
        delt_x = (b-a)/Num
        
        running_count = 0
        
        for k in range(1, Num+1):
        
            x_k = a + (delt_x * k)
        
            x = x_k

            answer = delt_x * eval(expression)
            
            running_count += answer
        
        
        actual = actual_integrate(expression, a, b)
        
        error_value = abs(running_count - actual)
        
        end = time.time()

        time_el = end - start

        return running_count, error_value, time_el



    def integrate_simpson(a : float, b : float, N: float, expression : any) -> float:
        """
        Returns the approximate area under the curve from a to b using
        Simpson's Rule for numerical integration

        Parameters:
        ------------
        a : int
            start of the integration range
        b : int
            end of integration range
        Num : int
            number of intervals for integraton must be even
        expression: str
            user entered function to be integrated over the range [a,b]

        Returns:
        --------
        float
            approximate area under the curve from a to b

        """
        start = time.time()
    
        if N % 2 != 0:
    
            raise ValueError("Number of Intervals Must be Even")
    
        delt_x = (b-a)/N
    
        multiplier = delt_x / 3
    
        x_k_even = 0
    
        x_k_odd = 0
    
        x_0 = 0
    
        x_N = 0
    
        for k in range (1,N+1):
    
            if k == 1:
                x = a
                x_0 = eval(expression)
    
            elif k == N:
                x = b
                x_N = eval(expression)
    
            elif k % 2 == 0:
                x = a+ (delt_x*k)
                x_k_even += 2 *eval(expression)
    
            else:
                x = a + (delt_x * k)
                x_k_odd += 4 *eval(expression)
    
        Sn = multiplier * (x_0 + x_k_even + x_k_odd + x_N)
    
        actual = actual_integrate(expression, a, b)
    
        error_value = abs(Sn - actual)
    
        end = time.time()
    
        total_time = end-start
    
        return Sn, error_value, total_time


    #Integration Alogrithm for Trapezoidal Rule
    def integrate_trapezoidal(a : float, b : float, N : float, expression : any) -> any:
        
        """
        Returns the approximate area under the curve from a to b using
        Trapezoidal Rule for numerical integration

        Parameters:
        ------------
        a : int
            start of the integration range
        b : int
            end of integration range
        Num : int
            number of intervals for integraton
        expression: str
            user entered function to be integrated over the range [a,b]

        Returns:
        --------
        float
            approximate area under the curve from a to b

        """
    
        start = time.time()
        
        delt_x = (b-a)/N
        
        x = a
        
        f_a = eval(expression)
        
        x = b
        
        f_b = eval(expression)
        
        running_sum = 0
        
        #for loop for the summation
        for k in range(1,N):
        
            x_k = a + (delt_x * k)
        
            x = x_k
        
            running_sum += eval(expression)
        
        mid = (f_b + f_a)/2
        
        final_answer = delt_x * (running_sum + mid)
        
        actual = actual_integrate(expression, a, b)
        
        error_value = abs(final_answer - actual)
        
        end = time.time()
        
        total_time = end-start
        
        return final_answer, error_value, total_time











