#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 12:07:09 2023

@author: Brizzia Munoz Robles
"""

#%%

import unittest
import numpy as np
import os 
from chemotaxissimulation import ChemotaxisSimulation

#%%

class TestChemotaxisSimulation(unittest.TestCase): 

    def setUp(self):

      #correct inputs
      n=24 #lattice nodes in x-direction
      m=24 #lattice nodes in y-direction
      CC=np.zeros((m,n)) #inital array of the area
      CC[:,0:4]=1 #Initial condition of scratch assay
      CC[:,20:24]=1 #Initial condition of scratch assay
      V=1 #one cell per compartment
      rm=1 #motility
      rp=0.4 #proilferation
      rd=rp*.01 #death
      tf=10 #unntiless time
      C_start = 0
      C_end = tf
      rhox=np.zeros((m,n)) #no bias

      #no cells
      self.CC2=np.zeros((m,n)) #inital array of the area

      self.entry = ChemotaxisSimulation(n,m,CC,V,rm,rp,rd,tf,C_start,C_end,rhox)
      self.entry1 = ChemotaxisSimulation(n,m,self.CC2,V,rm,rp,rd,tf,C_start,C_end,rhox)


    def test_cell_movment(self):
      result = self.entry.cell_movement()
      result1 = self.entry1.cell_movement()
      self.assertIsNotNone(result)
      #self.assert_array_equal(result1==self.CC2)

    def test_simulate(self):
      result = self.entry.simulate("fig1.gif")
      file_exists = os.path.isfile('fig1.gif')
      self.assertIsNone(result)
      self.assertTrue(file_exists)
      os.remove('fig1.gif')
      


if __name__ == '__main__':
  unittest.main()
