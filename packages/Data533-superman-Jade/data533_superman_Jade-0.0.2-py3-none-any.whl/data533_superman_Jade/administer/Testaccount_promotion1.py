# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 19:03:00 2023

@author: Administrator
"""

import unittest
import sys 
sys.path.append("..") 
import customer.members
from customer.members import member
# import administer.account
# from administer.account import promotion1

import account
from account import promotion1

import importlib
importlib.reload(account)
importlib.reload(customer.members)

class Testpromotion1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")
    @classmethod
    def tearDownClass(cls):
        print("tearDownClass\n")
    def setUp(self):
        self.q1=["A","B","C"]

    def tearDown(self):
        print("tearDown")
    def testpromotion(self):

        self.assertEqual(promotion1(self.q1),{'A': ['snack', 1000, 5], 'B': ['milk-b', 1000, 3], 'C': ['flower', 520, 3]})

# unittest.main(module='Testaccount_promotion1')