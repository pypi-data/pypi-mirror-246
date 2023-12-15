# class for all the discrete probability density functions
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

class Discrete: 

    def __init__(self, name):
            self.name = name  
    
    
    """
    BINOMIAL DISTRIBUTION
    """

    def binomial_ex(a,b,x, n,p):

        exp = n*p
        var = n*p*(1-p)

        if(a == "n") & (b == "n"): #Then we want probability at a certain point


            #Calculate the probability that P(X = x)

            prob = comb(n,x) * (p**x) * ((1-p)**(n - x))

            """
            FOR PLOTTING

         """

            # Generate the array of x-values with respect to bounds
            x_values = np.arange(0, n + 1)
            pmf_values = comb(n,x_values) * (p**x_values) * ((1-p)**(n - x_values))

            # Plot the PMF
            graph = plt.bar(x_values, pmf_values, label=f'Binomial PMF')
            graph[x].set_color('red')

            plt.title('Binomial Distribution PMF')
            plt.xlabel('x')
            plt.ylabel('Probability Mass Function')

            plt.legend()
            plt.grid(True)
            plt.show()

            return prob, exp, var

        elif(x == "n"): #Then we want to calculate probability between a and b


            prob_a = 0
            prob_b = 0


            #Calculate cumulative probabilities
            for i in range(b+1):
                prob_b += math.comb(n,i) * p**i * (1-p)**(n - i)

            for i in range(a):
                prob_a += math.comb(n,i) * p**i * (1-p)**(n - i)


            #print(prob_a)
            #print(prob_b)

            prob_a_to_b = prob_b - prob_a



            """
            FOR PLOTTING

            """

            # Generate the array of x-values with respect to bounds
            x_values = np.arange(0, n + 1)
            pmf_values = comb(n,x_values) * (p**x_values) * ((1-p)**(n - x_values))

            # Plot the PMF
            graph = plt.bar(x_values, pmf_values, label=f'Binomial PMF')
            for i in range(a,b+1):
                graph[i].set_color('red')

            #graph[highlights].set_color('red')

            plt.title('Binomial Distribution PMF')
            plt.xlabel('x')
            plt.ylabel('Probability Mass Function')

            plt.legend()
            plt.grid(True)
            plt.show()

            return prob_a_to_b, exp, var



    #Case where calculating P(X=x)
    #binomial_ex(a='n', b='n', x=4, n=12, p = 0.25)

    #Case where calculating P(a <= x <= b)
    #binomial_ex(a=2, b=4, x='n', n=12, p = 0.25)

    """
    GEOMETRIC DISTRIBUTION
    """

    def geometric_ex(a, b,x, p):

        exp = 1/p
        var = (1-p)/(p**2)
        sd = math.sqrt(var)

        if(a == "n") & (b == "n"): #Then we want probability at a certain point


            #Calculate the probability that P(X = x)

            prob = ((1-p)**(x-1)) * p

            """
            FOR PLOTTING

            """

            # Generate the array of x-values with respect to bounds
            x_values = np.arange(1, x*2)
            pmf_values = (1-p)**(x_values-1) * p

            # Plot the PMF
            graph = plt.bar(x_values, pmf_values, label=f'Geometric PMF')
            graph[x-1].set_color('red')

            plt.title('Geometric Distribution PMF')
            plt.xlabel('x')
            plt.ylabel('Probability Mass Function')

            plt.legend()
            plt.grid(True)
            plt.show()

            return prob, exp, var

        elif(x == "n"): #Then we want to calculate probability between a and b

            #Calculate cumulative probabilities

            #P(X < a)
            prob_a = (1 - (1-p)**(a-1))

            #P(X <= b)
            prob_b = (1 - (1-p)**b)

            prob_a_to_b = prob_b - prob_a


            """
            FOR PLOTTING

            """

            # Generate the array of x-values with respect to bounds
            x_values = np.arange(1, b*2)
            pmf_values = (1-p)**(x_values-1) * p

            # Plot the PMF
            graph = plt.bar(x_values, pmf_values, label=f'Geometric PMF')
            for i in range(a-1,b):
                graph[i].set_color('red')

            #graph[highlights].set_color('red')

            plt.title('Geometric Distribution PMF')
            plt.xlabel('x')
            plt.ylabel('Probability Mass Function')

            plt.legend()
            plt.grid(True)
            plt.show()

            return prob_a_to_b, exp, var



    #Case where calculating P(X=x)
    #geometric_ex(a='n', b='n', x = 5, p = 0.5)

    #Case where calculating P(a <= x <= b)
    #geometric_ex(a=3, b=5, x = 'n', p = 0.5)

    """
    POISSON DISTRIBUTION
    """

    def poisson_ex(a,b,x,lam):

        exp = lam
        var = lam

        if(a == "n") & (b == "n"): #Then we want probability at a certain point


            #Calculate the probability that P(X = x)

            prob = (np.exp(-lam) * lam**x) / math.factorial(x)


            """
            FOR PLOTTING

            """

            # Generate the array of x-values with respect to bounds
            x_values = np.arange(0, x*2)
            pmf_values = (np.exp(-lam) * lam**x_values) / [math.factorial(i) for i in x_values]


            # Plot the PMF
            graph = plt.bar(x_values, pmf_values, label=f'Poisson PMF')
            graph[x].set_color('red')

            plt.title('Poisson Distribution PMF')
            plt.xlabel('x')
            plt.ylabel('Probability Mass Function')

            plt.legend()
            plt.grid(True)
            plt.show()

            return prob, exp, var

        elif(x == "n"): #Then we want to calculate probability between a and b


            prob_a = 0
            prob_b = 0


            #Calculate cumulative probabilities
            for i in range(b+1):
                prob_b += (np.exp(-lam) * lam**i) / math.factorial(i)

            for i in range(a):
                prob_a += (np.exp(-lam) * lam**i) / math.factorial(i)

            #print(prob_a)
            #print(prob_b)

            prob_a_to_b = prob_b - prob_a

            """
            FOR PLOTTING

            """

            # Generate the array of x-values with respect to bounds
            x_values = np.arange(0, b*2)
            pmf_values = (np.exp(-lam) * lam**x_values) / [math.factorial(i) for i in x_values]

            # Plot the PMF
            graph = plt.bar(x_values, pmf_values, label=f'Poisson PMF')

            for i in range(a,b+1):
                graph[i].set_color('red')

            plt.title('Poisson Distribution PMF')
            plt.xlabel('x')
            plt.ylabel('Probability Mass Function')

            plt.legend()
            plt.grid(True)
            plt.show()

            return prob_a_to_b, exp, var



    #Case where calculating P(X=x)
    #poisson_ex(a='n', b='n', x=3, lam = 2)

    #Case where calculating P(a <= x <= b)
    #poisson_ex(a=2, b=4, x='n', lam = 2)




