#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 13:02:26 2023

@author: Brizzia Munoz Robles
"""

#%%
import numpy as np
import unittest
from photokineticanalysis import PhotokineticAnalysis

#%%

class TestPhotokineticAnalysis(unittest.TestCase): 

    def setUp(self):
      #Correct x and k input 
      x = np.array([0,1,5,10])
      k = 0.7

      #Incorrect x input
      x1 = np.array([0,1,'hello',10])
      k1 = 0.7

      #Incorrect kinetic input
      k2 = 1

      #excel sheet containing experimental data
      p = "example_2.xlsx"

      self.entry = PhotokineticAnalysis(x,k,p)
      self.entry1 = PhotokineticAnalysis(x1,k1,p)
      self.entry2 = PhotokineticAnalysis(x, k2,p)
      self.entry3 = PhotokineticAnalysis(x1,k2,p)

    def test_check(self):
      result = self.entry.check()
      result1 = self.entry1.check()
      result2 = self.entry2.check()
      result3 = self.entry3.check()
      self.assertEqual(result, "Valid input")
      self.assertEqual(result1, "Invalid x input")
      self.assertEqual(result2, "Invalid k input")
      self.assertEqual(result3, "Invalid x input and k input")

    def test_theoretical(self):
      result_theoretical = self.entry.calculate_theoretical(display = True)
      result_theoretical2 = self.entry.calculate_theoretical(display = False)
      self.assertTrue(result_theoretical)
      self.assertIsNone(result_theoretical2)

    def test_experimental(self):
      result_experimental = self.entry.calculate_experimental(graph = True)
      result_experimental1 = self.entry.calculate_experimental(graph = False)
      self.assertTrue(result_experimental)
      self.assertIsNone(result_experimental1)


if __name__ == '__main__':
  unittest.main(argv=['first-arg-is-ignored'], exit=False)
