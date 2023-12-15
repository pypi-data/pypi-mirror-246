# class file for all continuous probability density functions

from pystatslib import Integration as integ
import numpy as np
import math
import matplotlib.pyplot as plt


class Continuous:


    def __init__(self, name):
        self.name = name  

    
    """
    UNIFORM DISTRIBUTION ---------------RECTANGULAR INTEGRATION---------------
    """

    def Uniform_ex_rec(a, b, N, lower, upper):


        func = f"1/({str(upper)}-{str(lower)})"

        if a == "-inf":
            a = -10000
            prob = integ.integrate_rectangular(a,b,N,func)
        elif b == "inf":
            b = 10000
            prob = integ.integrate_rectangular(a, b, N, func)
        else:
            prob = integ.integrate_rectangular(a, b, N, func)


        """
        EXPECTATION AND VARIANCE

        """


        expectation_outputs = integ.integrate_rectangular(lower,upper,N, f"({func})*x")
        expectation = expectation_outputs[0]
        #print(expectation, type(expectation))


        expectation_squared_outputs = integ.integrate_rectangular(lower, upper, N, f"({func})*x*x")
        expectation_squared = expectation_squared_outputs[0]
        #print(expectation_squared, type(expectation_squared))


        variance = expectation_squared - pow(expectation,2)

        sd = math.sqrt(variance)



        """
        FOR PLOTTING

        """

        #**** Technically, uniform function is defined from a to b, and then we may be integrating between bounds of a and b, let's call them c and d

        # Generate the array of x-values with respect to bounds
        x_values = np.linspace(lower, upper, N)
        
        uniform_pdf = 1 / (upper-lower)

        #Modification since the uniform pdf does not take x as a parameter
        y_values = np.repeat(1 / (upper-lower), N)


        # Plot the PDF
        plt.plot(x_values, y_values, label=f'Uniform PDF')

        # Fill the area under the curve from a to b
        plt.fill_between(x_values, y_values, where=((x_values >= a) & (x_values <= b)), 
                         color='skyblue', alpha=0.4, label=f'Area ({a}, {b})')

        plt.title('Uniform Distribution: Rectangular Integration')
        plt.xlabel('x')
        plt.ylabel('Probability Density Function')

        # Plot Dotted lines for a, b, and x
        plt.axvline(a, color='red', linestyle='dotted', label=f'a={a}')
        plt.axvline(b, color='green', linestyle='dotted', label=f'b={b}')

        plt.legend()
        plt.grid(True)
        plt.show()

        return prob, expectation, variance, sd
    
    """
    UNIFORM DISTRIBUTION ---------------SIMPSON'S INTEGRATION---------------
    """

    """
    Probability Distribution Function (PDF) for the uniform distribution from a to b

    """


    def Uniform_ex_simp(a, b, N, lower, upper):


        func = f"1/({str(upper)}-{str(lower)})"

        if a == "-inf":
            a = -10000
            prob = integ.integrate_simpson(a,b,N,func)
        elif b == "inf":
            b = 10000
            prob = integ.integrate_simpson(a, b, N, func)
        else:
            prob = integ.integrate_simpson(a, b, N, func)


        """
        EXPECTATION AND VARIANCE

        """


        expectation_outputs = integ.integrate_simpson(lower,upper,N, f"({func})*x")
        expectation = expectation_outputs[0]
        #print(expectation, type(expectation))


        expectation_squared_outputs = integ.integrate_simpson(lower, upper, N, f"({func})*x*x")
        expectation_squared = expectation_squared_outputs[0]
        #print(expectation_squared, type(expectation_squared))


        variance = expectation_squared - pow(expectation,2)

        sd = math.sqrt(variance)


        """
        FOR PLOTTING
        """

        #**** Technically, uniform function is defined from a to b, and then we may be integrating between bounds of a and b, let's call them c and d

        # Generate the array of x-values with respect to bounds
        x_values = np.linspace(lower, upper, N)
        uniform_pdf = 1/(upper-lower)

        #Modification since the uniform pdf does not take x as a parameter
        y_values = np.repeat(1/(upper-lower), N)


        # Plot the PDF
        plt.plot(x_values, y_values, label=f'Uniform PDF')

        # Fill the area under the curve from a to b
        plt.fill_between(x_values, y_values, where=((x_values >= a) & (x_values <= b)), 
                         color='skyblue', alpha=0.4, label=f'Area ({a}, {b})')

        plt.title('Uniform Distribution: Simpsons Integration')
        plt.xlabel('x')
        plt.ylabel('Probability Density Function')

        # Plot Dotted lines for a, b, and x
        plt.axvline(a, color='red', linestyle='dotted', label=f'a={a}')
        plt.axvline(b, color='green', linestyle='dotted', label=f'b={b}')

        plt.legend()
        plt.grid(True)
        plt.show()

        return prob, expectation, variance, sd



    """
    UNIFORM DISTRIBUTION ---------------TRAPEZOIDAL INTEGRATION---------------
    """

    """
    Probability Distribution Function (PDF) for the uniform distribution from a to b

    """


    def Uniform_ex_trap(a, b, N, lower, upper):


        func = f"1/({str(upper)}-{str(lower)})"

        if a == "-inf":
            a = -10000
            prob = integ.integrate_trapezoidal(a,b,N,func)
        elif b == "inf":
            b = 10000
            prob = integ.integrate_trapezoidal(a, b, N, func)
        else:
            prob = integ.integrate_trapezoidal(a, b, N, func)


        """
        EXPECTATION AND VARIANCE

        """

        expectation_outputs = integ.integrate_trapezoidal(lower,upper,N, f"({func})*x")
        
        expectation = expectation_outputs[0]
        
        #print(expectation, type(expectation))


        expectation_squared_outputs = integ.integrate_trapezoidal(lower, upper, N, f"({func})*x*x")
        
        expectation_squared = expectation_squared_outputs[0]
        
        #print(expectation_squared, type(expectation_squared))


        variance = expectation_squared - pow(expectation,2)

        sd = math.sqrt(variance)


        """
        FOR PLOTTING
        """

        #**** Technically, uniform function is defined from a to b, and then we may be integrating between bounds of a and b, let's call them c and d

        # Generate the array of x-values with respect to bounds
        x_values = np.linspace(lower, upper, N)
        
        uniform_pdf = 1 / (upper-lower)

        #Modification since the uniform pdf does not take x as a parameter
        y_values = np.repeat(1/(upper-lower), N)


        # Plot the PDF
        plt.plot(x_values, y_values, label=f'Uniform PDF')

        # Fill the area under the curve from a to b
        plt.fill_between(x_values, y_values, where=((x_values >= a) & (x_values <= b)), 
                         color='skyblue', alpha=0.4, label=f'Area ({a}, {b})')

        plt.title('Uniform Distribution: Trapezoidal Integration')
        plt.xlabel('x')
        plt.ylabel('Probability Density Function')

        # Plot Dotted lines for a, b, and x
        plt.axvline(a, color='red', linestyle='dotted', label=f'a={a}')
        plt.axvline(b, color='green', linestyle='dotted', label=f'b={b}')

        plt.legend()
        plt.grid(True)
        plt.show()

        return prob, expectation, variance, sd



    def exponential_ex_rec(a, b, N, lam):

        func = f"({str(lam)}*exp((-{str(lam)})*x))"

        if a == "-inf":
            a = -10000
            prob = integ.integrate_rectangular(a,b,N,func)
        elif b == "inf":
            b = 10000
            prob = integ.integrate_rectangular(a, b, N, func)
        else:
            prob = integ.integrate_rectangular(a, b, N, func)


        """
        EXPECTATION AND VARIANCE
        """

        expectation_outputs = integ.integrate_rectangular(0,1000,N, f"({func})*x")
        expectation = expectation_outputs[0]
        #print(expectation, type(expectation))


        expectation_squared_outputs = integ.integrate_rectangular(0, 1000, N, f"({func})*x*x")
        expectation_squared = expectation_squared_outputs[0]
        #print(expectation_squared, type(expectation_squared))


        variance = expectation_squared - pow(expectation,2)

        sd = math.sqrt(variance)


        """
        FOR PLOTTING

        """

        # Generate the array of x-values with respect to bounds

        x_values = np.linspace(a, b , N)
        exp_pdf = lam * np.exp(-lam * x_values)


        # Plot the PDF
        plt.plot(x_values, exp_pdf, label=f'Exponential PDF')

        # Fill the area under the curve from a to b
        plt.fill_between(x_values, exp_pdf, where=((x_values >= a) & (x_values <= b)), color='skyblue', alpha=0.4, label=f'Area ({a}, {b})')

        plt.title('Exponential Distribution: Rectangular Integration')
        plt.xlabel('x')
        plt.ylabel('Probability Density Function')

        # Plot Dotted lines for a, b, and x
        plt.axvline(a, color='red', linestyle='dotted', label=f'a={a}')
        plt.axvline(b, color='green', linestyle='dotted', label=f'b={b}')
        #plt.axvline(x, color='blue', linestyle='dotted', label=f'x={x}')

            #ymax= not working to get dotted lines to stop at height

        plt.legend()
        plt.grid(True)
        plt.show()

        return prob, expectation, variance, sd




    """
    EXPONENTIAL DISTRIBUTION ---------------SIMPSON'S INTEGRATION---------------
    """

    def exponential_ex_simp(a, b, N, lam):

        func = f"({str(lam)}*exp((-{str(lam)})*x))"

        if a == "-inf":
            a = -10000
            prob = integ.integrate_simpson(a,b,N,func)
        elif b == "inf":
            b = 10000
            prob = integ.integrate_simpson(a, b, N, func)
        else:
            prob = integ.integrate_simpson(a, b, N, func)


        """
        EXPECTATION AND VARIANCE
        """

        expectation_outputs = integ.integrate_simpson(0,1000,N, f"({func})*x")
        expectation = expectation_outputs[0]
        #print(expectation, type(expectation))


        expectation_squared_outputs = integ.integrate_simpson(0, 1000, N, f"({func})*x*x")
        expectation_squared = expectation_squared_outputs[0]
        #print(expectation_squared, type(expectation_squared))


        variance = expectation_squared - pow(expectation,2)

        sd = math.sqrt(variance)


        """
        FOR PLOTTING

        """

        # Generate the array of x-values with respect to bounds

        x_values = np.linspace(a, b , N)
        exp_pdf = lam * np.exp(-lam * x_values)


        # Plot the PDF
        plt.plot(x_values, exp_pdf, label=f'Exponential PDF')

        # Fill the area under the curve from a to b
        plt.fill_between(x_values, exp_pdf, where=((x_values >= a) & (x_values <= b)), color='skyblue', alpha=0.4, label=f'Area ({a}, {b})')

        plt.title('Exponential Distribution: Simpsons Integration')
        plt.xlabel('x')
        plt.ylabel('Probability Density Function')

        # Plot Dotted lines for a, b, and x
        plt.axvline(a, color='red', linestyle='dotted', label=f'a={a}')
        plt.axvline(b, color='green', linestyle='dotted', label=f'b={b}')
        #plt.axvline(x, color='blue', linestyle='dotted', label=f'x={x}')

            #ymax= not working to get dotted lines to stop at height

        plt.legend()
        plt.grid(True)
        plt.show()

        return prob, expectation, variance, sd




    """
    EXPONENTIAL DISTRIBUTION ---------------TRAPEZOIDAL INTEGRATION---------------
    """

    def exponential_ex_trap(a, b, N, lam):

        func = f"({str(lam)}*exp((-{str(lam)})*x))"

        if a == "-inf":
            a = -10000
            prob = integ.integrate_trapezoidal(a,b,N,func)
        elif b == "inf":
            b = 10000
            prob = integ.integrate_trapezoidal(a, b, N, func)
        else:
            prob = integ.integrate_trapezoidal(a, b, N, func)


        """
        EXPECTATION AND VARIANCE
        """

        expectation_outputs = integ.integrate_trapezoidal(0,1000,N, f"({func})*x")
        expectation = expectation_outputs[0]
        #print(expectation, type(expectation))


        expectation_squared_outputs = integ.integrate_trapezoidal(0, 1000, N, f"({func})*x*x")
        expectation_squared = expectation_squared_outputs[0]
        #print(expectation_squared, type(expectation_squared))


        variance = expectation_squared - pow(expectation,2)

        sd = math.sqrt(variance)


        """
        FOR PLOTTING

        """

        # Generate the array of x-values with respect to bounds

        x_values = np.linspace(a, b , N)
        exp_pdf = lam * np.exp(-lam * x_values)


        # Plot the PDF
        plt.plot(x_values, exp_pdf, label=f'Exponential PDF')

        # Fill the area under the curve from a to b
        plt.fill_between(x_values, exp_pdf, where=((x_values >= a) & (x_values <= b)), color='skyblue', alpha=0.4, label=f'Area ({a}, {b})')

        plt.title('Exponential Distribution: Trapezoidal Integration')
        plt.xlabel('x')
        plt.ylabel('Probability Density Function')

        # Plot Dotted lines for a, b, and x
        plt.axvline(a, color='red', linestyle='dotted', label=f'a={a}')
        plt.axvline(b, color='green', linestyle='dotted', label=f'b={b}')
        #plt.axvline(x, color='blue', linestyle='dotted', label=f'x={x}')

            #ymax= not working to get dotted lines to stop at height

        plt.legend()
        plt.grid(True)
        plt.show()

        return prob, expectation, variance, sd



    """
    NORMAL DISTRIBUTION ---------------RECTANGULAR INTEGRATION---------------
    """


    def Normal_ex_rec(a,b,N, mu, sigma):

        func = f"((1/({str(sigma)}*sqrt(2*pi))*exp((-0.5)*((x-{str(mu)})/{str(sigma)})**2)))"

        if a == "-inf":
            a = -10000
            prob_norm = integ.integrate_rectangular(a,b,N,func)
        elif b == "inf":
            b = 10000
            prob_norm = integ.integrate_rectangular(a, b, N, func)
        else:
            prob_norm = integ.integrate_rectangular(a, b, N, func)


        """
        EXPECTATION AND VARIANCE

        """


        expectation_outputs = integ.integrate_rectangular(-10000,10000,N, f"({func})*x")
        expectation = expectation_outputs[0]
        #print(expectation, type(expectation))


        expectation_squared_outputs = integ.integrate_rectangular(-10000, 10000, N, f"({func})*x*x")
        expectation_squared = expectation_squared_outputs[0]
        #print(expectation_squared, type(expectation_squared))


        variance = expectation_squared - pow(expectation,2)

        sd = math.sqrt(variance)



        """
        FOR PLOTTING

        """

        # Generate the array of x-values with respect to bounds
        x_values = np.linspace(0, b , N)

        normal_pdf = (1 / (math.sqrt(2*math.pi) * sigma) ) * np.exp( - ( (x_values - mu)**2 ) / (2 * (sigma**2) ))

        #Calculate the value of the normal pdf at each x-value
        #pdf_values = normal_pdf(x_values, mu, sigma)

        # Plot the PDF
        plt.plot(x_values, normal_pdf, label=f'Normal PDF')

        # Fill the area under the curve from a to b
        plt.fill_between(x_values, normal_pdf, where=((x_values >= a) & (x_values <= b)), color='skyblue', alpha=0.4, label=f'Area ({a}, {b})')

        plt.title('Normal Distribution: Rectangular Integration')
        plt.xlabel('x')
        plt.ylabel('Probability Density Function')
        plt.xlim(a-1, b+1)

        # Plot Dotted lines for a, b, and x
        plt.axvline(a, color='red', linestyle='dotted', label=f'a={a}' )
        plt.axvline(b, color='green', linestyle='dotted', label=f'b={b}')


            #ymax= not working to get dotted lines to stop at height

        plt.legend()
        plt.grid(True)
        plt.show()

        return prob_norm, expectation, variance, sd

    #print(f" pnorm rectangular 50<x<90 = {Normal_ex_rec(50,90,10000,95,23)}")
    #print(f" pnorm rectangular x<100 = {Normal_ex_rec('-inf',100,10000,95,23)}")
    #print(f" pnorm rectangular x>135 = {Normal_ex_rec(135,'inf',10000,95,23)}")

    """
    NORMAL DISTRIBUTION ---------------SIMPSON'S INTEGRATION---------------
    """


    def Normal_ex_simp(a,b,N, mu, sigma):

        func = f"((1/({str(sigma)}*sqrt(2*pi))*exp((-0.5)*((x-{str(mu)})/{str(sigma)})**2)))"

        if a == "-inf":
            a = -10000
            prob_norm = integrate_simpson(a,b,N,func)
        elif b == "inf":
            b = 10000
            prob_norm = integrate_simpson(a, b, N, func)
        else:
            prob_norm = integrate_simpson(a, b, N, func)


        """
        EXPECTATION AND VARIANCE

        """


        expectation_outputs = integ.integrate_simpson(-10000,10000,N, f"({func})*x")
        expectation = expectation_outputs[0]
        #print(expectation, type(expectation))


        expectation_squared_outputs = integ.integrate_simpson(-10000, 10000, N, f"({func})*x*x")
        expectation_squared = expectation_squared_outputs[0]
        #print(expectation_squared, type(expectation_squared))


        variance = expectation_squared - pow(expectation,2)

        sd = math.sqrt(variance)

        """
        FOR PLOTTING

        """

        # Generate the array of x-values with respect to bounds
        x_values = np.linspace(0, b , N)

        normal_pdf = (1 / (math.sqrt(2*math.pi) * sigma) ) * np.exp( - ( (x_values - mu)**2 ) / (2 * (sigma**2) ))

        #Calculate the value of the normal pdf at each x-value
        #pdf_values = normal_pdf(x_values, mu, sigma)

        # Plot the PDF
        plt.plot(x_values, normal_pdf, label=f'Normal PDF')

        # Fill the area under the curve from a to b
        plt.fill_between(x_values, normal_pdf, where=((x_values >= a) & (x_values <= b)), color='skyblue', alpha=0.4, label=f'Area ({a}, {b})')

        plt.title('Normal Distribution: Simpsons Integration')
        plt.xlabel('x')
        plt.ylabel('Probability Density Function')
        plt.xlim(a-1, b+1)


        # Plot Dotted lines for a, b, and x
        plt.axvline(a, color='red', linestyle='dotted', label=f'a={a}' )
        plt.axvline(b, color='green', linestyle='dotted', label=f'b={b}')
        #plt.axvline(x, color='blue', linestyle='dotted', label=f'x={x}')

            #ymax= not working to get dotted lines to stop at height

        plt.legend()
        plt.grid(True)
        plt.show()

        return prob_norm, expectation, variance, sd

    #print(f"pnorm Simpson 50<x<90 = {Normal_ex_simp(50,90,1000,95,23)}")
    #print(f"pnorm Simpson x<100 = {Normal_ex_simp('-inf',100,10000,95,23)}")
    #print(f" pnorm Simpson x >135 = {Normal_ex_simp(135,'inf',10000,95,23)}")

    """
    NORMAL DISTRIBUTION ---------------TRAPEZOIDAL INTEGRATION---------------
    """

    def Normal_ex_trap(a,b,N, mu, sigma):

        func = f"((1/({str(sigma)}*sqrt(2*pi))*exp((-0.5)*((x-{str(mu)})/{str(sigma)})**2)))"

        if a == "-inf":
            a = -10000
            prob_norm = integ.integrate_trapezoidal(a,b,N,func)
        elif b == "inf":
            b = 10000
            prob_norm = integ.integrate_trapezoidal(a, b, N, func)
        else:
            prob_norm = integ.integrate_trapezoidal(a, b, N, func)


        #print(prob_norm)

        expectation_outputs = integ.integrate_trapezoidal(-10000,10000,N, f"({func})*x")
        expectation = expectation_outputs[0]
        #print(expectation, type(expectation))


        expectation_squared_outputs = integ.integrate_trapezoidal(-10000, 10000, N, f"({func})*x*x")
        expectation_squared = expectation_squared_outputs[0]
        #print(expectation_squared, type(expectation_squared))


        variance = expectation_squared - pow(expectation,2)

        sd = math.sqrt(variance)


        """
        FOR PLOTTING

        """

        # Generate the array of x-values with respect to bounds
        x_values = np.linspace(0, b , N)

        normal_pdf = (1 / (math.sqrt(2*math.pi) * sigma) ) * np.exp( - ( (x_values - mu)**2 ) / (2 * (sigma**2) ))

        #Calculate the value of the normal pdf at each x-value
        #pdf_values = normal_pdf(x_values, mu, sigma)

        # Plot the PDF
        plt.plot(x_values, normal_pdf, label=f'Normal PDF')

        # Fill the area under the curve from a to b
        plt.fill_between(x_values, normal_pdf, where=((x_values >= a) & (x_values <= b)), 
                         color='skyblue', alpha=0.4, label=f'Area ({a}, {b})')

        plt.title('Normal Distribution: Trapezoidal Integration')
        plt.xlabel('x')
        plt.ylabel('Probability Density Function')
        plt.xlim(a-1, b+1)

        # Plot Dotted lines for a, b, and x
        plt.axvline(a, color='red', linestyle='dotted', label=f'a={a}' )
        plt.axvline(b, color='green', linestyle='dotted', label=f'b={b}')
        #plt.axvline(x, color='blue', linestyle='dotted', label=f'x={x}')

            #ymax= not working to get dotted lines to stop at height

        plt.legend()
        plt.grid(True)
        plt.show()

        return prob_norm, expectation, variance, sd

#print(f"pnorm Trapezoid 50<x<90 = {Normal_ex_trap(50,90,1000,95,23)}")

