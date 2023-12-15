# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 19:03:00 2023

@author: Administrator
"""

import unittest
import sys 
sys.path.append("..") 
from datetime import datetime as dt
from datetime import timedelta 

import customer.members
# import administer.account
# from administer.account import promotion
from customer.members import member
from customer.transactions import transaction
import account
from account import promotion
from account import eliminate

import importlib
# importlib.reload(account)
importlib.reload(customer.members)

class Testpromotion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")
    @classmethod
    def tearDownClass(cls):
        print("tearDownClass\n")
    def setUp(self):
        self.q1=member(id=1, name="Bob", email="Bob@gmail.com", phone="12345", address="kelowna")
        self.q2=member(id=2, name="Nancy", email="Nancy@gmail.com", phone="678910", address="richmond")
        self.q3=member(id=2, name="Maria", email="MA@gmail.com", phone="unknown", address="unknown")
        self.q4=member(id=2, name="Mike", email="ME@gmail.com", phone="456788", address="Vancouver")
   
        self.p1=transaction(items_name="milk", items_value=3, transaction_time=dt.today()-timedelta(days=3))
        self.p2=transaction(items_name="flower", items_value=99, transaction_time=dt.today()-timedelta(days=40))
  
    def tearDown(self):
        print("tearDown")
    def testpromotion(self):
        self.q1.add_deposit(100000)
        self.q2.add_deposit(50000)
        self.q3.add_deposit(10000)
        self.q4.add_deposit(100)
        
        
        self.q1.add_credits(110000)
        self.q2.add_credits(55000)
        self.q3.add_credits(11000)
        self.q4.add_credits(200)
        

        self.assertEqual(promotion(self.q1), "Congratulation! You gain 106050.0 in your account")
        self.assertEqual(promotion(self.q2), "Congratulation! You gain 53025.0 in your account")
        self.assertEqual(promotion(self.q3), "Congratulation! You gain 10510.5 in your account")
        self.assertEqual(promotion(self.q4), "Nothing change about the deposit")
    def testeliminate(self):
        self.assertEqual(eliminate(self.p1,self.q1), "You account_credits will be eliminated in 27 days. Come to Superman.")
        self.assertEqual(eliminate(self.p2,self.q4), "You account_credits become 0")

# unittest.main(module='Testaccount_promotion')

# q4=member(id=2, name="Mike", email="ME@gmail.com", phone="456788", address="Vancouver")
# p1=transaction(items_name="milk", items_value=3, transaction_time=dt.today()-timedelta(days=3))
# a=eliminate(p1, q4)
# print(a)