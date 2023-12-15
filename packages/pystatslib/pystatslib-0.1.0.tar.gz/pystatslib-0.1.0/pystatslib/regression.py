# class for all the linear regression functions
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import t
from mpl_toolkits.mplot3d import Axes3D

class Regression:
    

    def __init__(self, name):
        self.name = name  


    #---------------------------------------------------------------------------------#
    #------------------------- Multiple Regression Function --------------------------#
    #---------------------------------------------------------------------------------#
    def multiple_regression():

        ###########################################################################################################################
        ########################### Solve for Regression Coefficients and plot scatterplot/regression plane #######################
        ###########################################################################################################################
        print(f'\n\n\nNot getting the correct output? Use the following instructions 
              to format your data in the following manner: \n\t(1) Make sure your file has a .csv file 
              extension\n\t(2) Ensure your data has column titles\n\t(3) The independent variables data must 
              be in the first two columns, while the dependent variable is in the third column\n\t(4) All 
              columns must be the same length and there should not be any missing cells of data\n\n')

        file_path = input(f"Enter the file path of the CSV file: ")

        # Read data from the CSV file
        df = pd.read_csv(file_path, header=0, usecols=[0, 1, 2])

        # This calculates the coefficients beta0, beta1, and beta2 using the normal equation beta_vector = (X'X)^1 X' y
        X = df.iloc[:, :-1]  # Exclude the last column (dependent variable)
    
        X = np.column_stack((np.ones(len(X)), X))  # Add a column of ones for the intercept
    
        y = df.iloc[:, -1]
    
        X = X.astype(float)
    
        y = y.to_numpy()
    
        X_T_X_inv = np.linalg.inv(np.dot(X.T, X))
    
        X_T_y = np.dot(X.T, y)
    
        betas = np.dot(X_T_X_inv, X_T_y) # each beta can be easily accessed by typing "betas[0]," 
                                        #if you want to access the intercept coefficient, for example

        print(f'\n\nThe multiple regression equation is: {betas[0]:.5f} + {betas[1]:.5f}x1 + {betas[2]:.5f}x2 + ε\n')

        # 3D scatterplot
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
    
        ax.scatter(df[list(df.columns)[0]], df[list(df.columns)[1]], df[list(df.columns)[2]], c='blue', marker='o')
    
        ax.set_xlabel(list(df.columns)[0])
        ax.set_ylabel(list(df.columns)[1])
        ax.set_zlabel(list(df.columns)[2])
        ax.set_title('3D Scatterplot')

        # Regression plane
        x1 = np.linspace(np.min(df[list(df.columns)[0]]), np.max(df[list(df.columns)[0]]), 100)
        x2 = np.linspace(np.min(df[list(df.columns)[1]]), np.max(df[list(df.columns)[1]]), 100)
    
        x1, x2 = np.meshgrid(x1, x2)
    
        z = betas[0] + betas[1] * x1 + betas[2] * x2
    
        ax.plot_surface(x1, x2, z, alpha=0.5, rstride=100, cstride=100, color='green')


        #################################################################################################
        ################################### Generate Summary Data #######################################
        #################################################################################################

        y_values = df[list(df.columns)[2]]
    
        min = np.percentile(y_values, 0)
    
        q1 = np.percentile(y_values, 25)
        median = np.percentile(y_values, 50)
    
        q3 = np.percentile(y_values, 75)
        max = np.percentile(y_values, 100)
    
        summary_data = {'Minimum': [min],
                        'Quartile 1': [q1],
                        'Median': [median],
                        'Quartile 3': [q3],
                        'Maximum': [max]}

        summary_data = pd.DataFrame(summary_data)

        print(f'Summary Data: \n{summary_data}\n')

        ###############################################################################################################################
        ########################################### Generate Regression Coefficient Table #############################################
        ###############################################################################################################################
        residuals = y - np.dot(X, betas) # resids
    
        sigma_squared = np.var(residuals, ddof=X.shape[1]) #variance of residuals
    
        var_cov_matrix = sigma_squared * X_T_X_inv
    
        se_coefficients = np.sqrt(np.diag(var_cov_matrix)) #obtain coeff std. errors

        coefficient_data = {'': ['(intercept)', list(df.columns)[0], list(df.columns)[1]],
                                'Estimate': [betas[0], betas[1], betas[2]],
                                'Std. Error': ['-', '-', '-'],
                                't value': ['-', '-', '-'],
                                'Pr{>|t|}': ['-', '-', '-']}
    
        coefficient_data = pd.DataFrame(coefficient_data)
    
        coefficient_data['Std. Error'] = se_coefficients
    
        coefficient_data['t value'] = betas / se_coefficients
    
        coefficient_data['Pr{>|t|}'] = 2 * (1 - stats.t.cdf(np.abs(betas / se_coefficients), df=len(X) - X.shape[1]))

        print(f'Coefficients: \n {coefficient_data}')

        ############################################################################################################################
        ########################################## Generate Regression Statistics Table ############################################
        ############################################################################################################################

        y_mean = np.mean(y)
    
        total_SS = np.sum((y - y_mean) ** 2) #total sum of squares
    
        fitted_y = betas[0] + betas[1] * X[:, 1] + betas[2] * X[:, 2]  # fitted vals
    
        reg_SS = np.sum((fitted_y - y_mean) ** 2) # regression sum of squares
    
        res_SS = np.sum((y - fitted_y) ** 2) #residual sum of squares

        r_squared = reg_SS / total_SS #Multiple R^2
    
        n = len(y)
    
        adjusted_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - X.shape[1] - 2)

        Reg_statistics = pd.DataFrame({
            'Metric': ['Multiple R','Multiple R^2', 'Adjusted R^2', 'Number of Observations'],
            'Value': [math.sqrt(r_squared), r_squared, adjusted_r_squared, n]
            })

        reg_df = X.shape[1]-1
    
        total_df = n-1
    
        res_df = total_df-reg_df
    
        f_stat = (reg_SS/reg_df) / (res_SS/res_df)
    
        f_pval = 1 - stats.f.cdf(f_stat, reg_df, res_df)
    
        ANOVA_TABLE = {'': ['Regression', 'Residual', 'Total'],
                    'df': [reg_df, res_df, total_df],
                    'SS': [reg_SS, res_SS, total_SS],
                    'MS': [reg_SS/reg_df, res_SS/res_df, '-'],
                    'F': [f_stat, '-', '-'],
                    'Significance F': [f_pval, '-', '-']}
    
        ANOVA_TABLE = pd.DataFrame(ANOVA_TABLE)
    
        print(f'\nANOVA TABLE: \n {ANOVA_TABLE}')
        print(f'\nRegression Statistics: \n{Reg_statistics}\n')

        # Save the plot as an image file
        plt.savefig("scatter_plot.png")
        print("Plot saved as scatter_plot.png\n") 

    #---------------------------------------------------------------------------------------------#






    #---------------------------------------------------------------------------------------------#
    #---------------------------- Simple Linear Regression Function ------------------------------#
    #---------------------------------------------------------------------------------------------#

    def simple_linear_regression():
        
        # Prompt the user to enter the file path
        print(f'\n\nUse the following instructions to format your data in the following manner: \n\t(1) Make sure your file has a .csv file extension\n\t(2) Ensure your data has column titles\n\t(3) The independent variable data must be in the first column, while the dependent variable is in the second column\n\t(4) All columns must be the same length and there should not be any missing cells of data\n\n')
        
        file_path = input("Enter the file path of the CSV file: ")

        # Read data from the CSV file
        df = pd.read_csv(file_path, header=0, usecols=[0, 1])

        ########################################################################################################################
        ########################### Calculates mean of x & y, standard deviation of x & y, covariance, ######################### 
        ######################################## slope (beta1), and intercept (beta0) ##########################################
        ########################################################################################################################

        # x and y values
        x_values = df[list(df.columns)[0]]
        y_values = df[list(df.columns)[1]]

        # mean values
        mean_x = df[list(df.columns)[0]].mean()
        mean_y = df[list(df.columns)[1]].mean()
        
        # standard deviation values
        sd_x = df[list(df.columns)[0]].std()
        sd_y = df[list(df.columns)[1]].std()
        
        covariance_xy = df[list(df.columns)[0]].cov(df[list(df.columns)[1]])
        
        beta1 = covariance_xy/(sd_x**2)
        beta0 = mean_y - (beta1) * (mean_x)

        print(f'\n\nThe linear regression equation is: y(x) = {beta0} + {beta1}x + ϵ\n')

        #########################################################################################################################
        ############## Calculate Summary Data: 0th (min), 25th, 50th (median), 75th, and 100th (max) percentiles ################
        #########################################################################################################################
        
        min = np.percentile(y_values, 0)
        
        q1 = np.percentile(y_values, 25)
        
        median = np.percentile(y_values, 50)
        
        q3 = np.percentile(y_values, 75)
        
        max = np.percentile(y_values, 100)


        ###############################################################################################################
        ################################# Create a DataFrame for y summary statistics #################################
        ###############################################################################################################
        
        summary_data = {'Minimum': [min],
                        'Quartile 1': [q1],
                        'Median': [median],
                        'Quartile 3': [q3],
                        'Maximum': [max]}

        summary_data = pd.DataFrame(summary_data)

        print(f'Summary Data: \n{summary_data}')

        ################################################################################################################
        ################################ Create tables with coefficients and other info ################################
        ################################################################################################################
        
        # Intercept standard error
        df['fitted_y'] = beta1 * df[list(df.columns)[0]] + beta0  # fitted y vals
        
        df['residuals'] = df[list(df.columns)[1]] - df['fitted_y']  # residuals
        
        n = len(df)  # no. of observations
        
        # sum of squares which is basically variance times n, depending on which formula you use
        sum_squared_diff = np.sum(
            ( df[list(df.columns)[0]] - np.mean( df[list(df.columns) [0] ] ) )**2 )  
        
        
        # Calculate the standard error of the regression intercept
        se_intercept = np.sqrt(
            sum(df['residuals']**2) / ( n - 2 ) * ( (1 / n) + (np.mean( df[list(df.columns) [0] ] )**2 ) / sum_squared_diff ) )  
        

        # Slope standard error
        se_slope = np.sqrt(sum(df['residuals']**2)/((n-2)*sum_squared_diff))

        # t values for intercept and slope
        intercept_tval = beta0/se_intercept
        slope_tval = beta1/se_slope

        # p-values for intercept and slope
        intercept_pval = 2 * (1 - t.cdf(abs(intercept_tval), n-2))
        slope_pval = 2 * (1 - t.cdf(abs(slope_tval), n-2))

        coefficient_data = {'': ['(intercept)', list(df.columns)[0]],
                            'Estimate': [beta0, beta1],
                            'Std. Error': [se_intercept, se_slope],
                            't value': [intercept_tval, slope_tval],
                            'Pr{>|t|}': [intercept_pval, slope_pval]}
        
        coefficient_data = pd.DataFrame(coefficient_data)

        print(f'\nCoefficients: \n {coefficient_data}')

        # For regression summary table
        R = covariance_xy/(sd_x*sd_y)
        
        R_Sq = R**2
        
        Mult_R_Sq = 1-((1-R_Sq)*(n-1))/(n-2)

        summary_data = [
            {'Statistic': 'Multiple R', 'Value': R},
            {'Statistic': 'Multiple R^2', 'Value': R_Sq},
            {'Statistic': 'Adjusted R^2', 'Value': Mult_R_Sq},
            {'Statistic': 'Observations', 'Value': n}
            ]
        regression_summary = pd.DataFrame(summary_data)

        print(f'\nRegression Statistics: \n {regression_summary}')

        # ANOVA Table
        reg_df = 1
        
        res_df = n-1-reg_df
        
        total_df = n-1
        
        reg_SS = sum((df['fitted_y'] - mean_y)**2)
        
        res_SS = sum((df[list(df.columns)[1]] - df['fitted_y'])**2)
        
        total_SS = reg_SS + res_SS
        
        f_stat = (reg_SS/reg_df)/(res_SS/res_df)
        
        f_pval = 1 - stats.f.cdf(f_stat, reg_df, res_df)
        
        ANOVA_TABLE = {'': ['Regression', 'Residual', 'Total'],
                        'df': [reg_df, res_df, total_df],
                        'SS': [reg_SS, res_SS, total_SS],
                        'MS': [reg_SS/reg_df, res_SS/res_df, '-'],
                        'F': [f_stat, '-', '-'],
                        'Significance F': [f_pval, '-', '-']}
        
        ANOVA_TABLE = pd.DataFrame(ANOVA_TABLE)

        print(f'\nANOVA TABLE: \n {ANOVA_TABLE}\n')

        ##############################################################################################
        ######################## Create a scatter plot and regression line ###########################
        ##############################################################################################
        
        plt.scatter(x_values, y_values, alpha=0.5)

        # regression line
        line = beta1 * x_values + beta0

        # Plot the regression line
        plt.plot(x_values, line, color='red', label='Regression Line')

        # Labels and title are obtained directly from the csv file for the user
        plt.xlabel(list(df.columns)[0])
        plt.ylabel(list(df.columns)[1])
        plt.title(f'Scatter Plot of {list(df.columns)[0]} and {list(df.columns)[1]}')

        # Save the plot as an image file
        plt.savefig("scatter_plot.png")

        print("Plot saved as scatter_plot.png\n")
    #----------------------------------------------------------------------#


