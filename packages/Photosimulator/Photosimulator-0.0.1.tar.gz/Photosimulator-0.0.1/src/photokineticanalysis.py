#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Dec  7 12:59:32 2023

@author: Brizzia Munoz Robles
"""

#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate
import scipy.optimize

#%%

class PhotokineticAnalysis(object):

  def __init__(self,x_value,k_value, file_name):
    """
    Initializes parameters

    Parameters:
    ----------
    x = values to calculate theoretical values for and plot

    k = kinetic rate constant

    file_name = excel file name in the form of "example.xlsx" containing experimental values with headers of x and y data

    theoretical_output = boolean on whether or not to graph theoretical data

    experimental_output = boolean on whether or not to graph experimental data

    """
    self.x_value = x_value
    self.k_value = k_value
    self.file_name = file_name


  def check(self):
    def check_x(self):
      """
      Checks that the inputs for the calculate_theoretical function are correct

        Args:
        ----------
          x_input: 
          k_input: 

        Returns:
        ----------
          A statement with whether input values are correct and can be plotted

      """
      if self.x_value is None and self.k_value is None:
        input = "Skip"
      elif all([isinstance(item, np.int64) for item in self.x_value]) and type(self.k_value) == float:
        input = "Valid input"
        #return ("Valid input")
      elif not all([isinstance(item, np.int64) for item in self.x_value]) and type(self.k_value) == float :
        input = "Invalid x input"

      elif all([isinstance(item, np.int64) for item in self.x_value]) and type(self.k_value) != float :
        input = "Invalid k input"

      elif not all([isinstance(item, np.int64) for item in self.x_value]) and type(self.k_value) != float:
        input = "Invalid x input and k input"

      return input
    results = check_x(self)

    return results

  def calculate_theoretical(self, display = False):
    """
      Calculates theoretical photokinetics

        Args:
        ----------
        x: x-values to be calculated
        k: photokinetic rate constant

        Returns:
        ----------
        A scatter plot of the values plotted as well as the output data in a table.

    """
    if all([isinstance(item, np.int64) for item in self.x_value]) and type(self.k_value) == float:
      column_headers = ["x", "y"]

      y = 1 - np.exp(-self.k_value*self.x_value)

      merged_array = np.array([self.x_value,y]).T

      output = tabulate(merged_array , column_headers, tablefmt="fancy_grid", floatfmt = ".2f")
      if display == True:
        Displayed = True
        figure1, axis1 = plt.subplots(1, 1)
        plt.scatter(self.x_value,y)
        plt.xlabel("x")
        plt.ylabel("y")
        print(output)
      else:
        Displayed = None
    return Displayed


  def calculate_experimental(self, graph = False):
    """
    Calculates the kinetic rate constant from experimental photokinetic data

        Args:
        ----------
        x: excel sheet containing initial x and y data with headers
        k: estimated photokinetic rate constant

        Returns:
        ----------
        A scatter plot of the values plotted as well as the output data in a table.
    """
    def exp_association(xx, k):
      """
      exponential association equation used to fit the data

      """
      return 1-np.exp(-k*xx)
    try:
        df = pd.read_excel(self.file_name)
        labels = list(df.columns.values)
        x_array = df[labels[0]]
        y_array = df[labels[1]]
        column_headers = [labels[0], labels[1]]
        popt, pcov = scipy.optimize.curve_fit(exp_association, x_array, y_array)
        k_rate = '%5.3f' %tuple(popt)
        perr = np.sqrt(np.diag(pcov))
        merged_array2 = np.array([x_array,y_array]).T
        output2 = tabulate(merged_array2 , column_headers, tablefmt="fancy_grid", floatfmt = ".2f")
        print("The kinetic constant is ", k_rate, u"\u00B1", '%5.3f' %perr)
        if graph == True:
          Data = True
          print(output2)
          figure, axis = plt.subplots(1, 1)
          plt.scatter(x_array,y_array)
          plt.xlabel(labels[0])
          plt.ylabel(labels[1])
        else:
          Data = None
    except FileNotFoundError:
        print('File does not exist or the title is incorrect. Verify file is in the format: title.xlsx ')
        Data=None


    return Data