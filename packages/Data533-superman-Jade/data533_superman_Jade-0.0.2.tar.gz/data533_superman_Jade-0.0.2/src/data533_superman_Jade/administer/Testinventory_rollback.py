# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 09:14:16 2023

@author: Administrator
"""


import unittest
import random
import inventory as I
# from administer import inventory as I
import importlib
importlib.reload(I)

class Testrollback(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")
    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")     
    def setUp(self):
        self.list1=I.inventory_informa.store
    def tearDown(self):
        print("tearDown")
    def testrollback(self):
        self.assertEqual(I.rollback(self.list1), {'50%': [['milk-b', 3.0, -17],
                  ['pork', 17.5, 0],
                  ['fish', 10.0, 1],
                  ['flower', 5.0, 2]],
          '80%': [['beef', 34.4, 5]]}
            )
    def testrollback2(self):
        self.assertEqual(I.rollback2(self.list1),  [['milk-b', 1000, 3], ['flower', 520, 3], ['snack', 1000, 5]]
            )       
# unittest.main(module="Testinventory_rollback")

    
