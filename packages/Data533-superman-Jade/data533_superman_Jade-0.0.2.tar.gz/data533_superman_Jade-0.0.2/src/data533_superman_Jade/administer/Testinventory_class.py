# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 17:05:17 2023

@author: Administrator
"""

import unittest
# import administer.inventory
# from administer.inventory import extend_informa
 
#import inventory
from inventory import extend_informa
from inventory import inventory_informa
from datetime import datetime as dt
from datetime import timedelta 
# import importlib
# importlib.reload(inventory)


class TestInventory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")
    def setUp(self):
        # milk_expire=dt.strptime("20231123", "%Y%m%d")
        # inventory_informa.store=[["item_name-measurement_unit","quantity","unit cost","unit price","date"],["milk-b",1000,3,6,milk_expire]]

        self.p1=extend_informa("flowers", 520, 3, 10, (dt.today()+timedelta(days=3)).strftime("%Y%m%d"))
        self.p2=extend_informa("A", 100, 5, 13, (dt.today()+timedelta(days=20)).strftime("%Y%m%d"))
        self.p3=inventory_informa("A", 100, 5, 13, (dt.today()+timedelta(days=20)).strftime("%Y%m%d"))

    def test__int__(self):
        self.p1.expire="20231209"
        self.p2.price=9
        self.p1.item="flower"
        self.p2.cost=17
        self.p1.quantity=100
        self.assertEqual(self.p1.expire,"20231209")
        self.assertEqual(self.p2.price,9)
        self.assertEqual(self.p1.quantity,100)
        self.assertEqual(self.p1.item,"flower")
        self.assertEqual(self.p2.cost,17)
        # self.p1.item="flowers"
        # self.p1.quantity=520
    def test__str__(self):
        self.assertEqual(str(self.p1),"flowers have 520 in store. The profit they can make is 3640")
        self.assertEqual(str(self.p2), 'A have 100 in store. The profit they can make is 800')
    def testprofit(self):
        self.assertEqual(self.p1.profit, 3640)
        self.assertEqual(self.p2.profit, 800)
    def testupdate(self):
        #dependent bigo
        self.assertEqual(self.p1.update("flowers", 520,6), "Suggest to adjust the price."+"flowers remains 1040")
        self.assertEqual(self.p1.update("flowers", -520,6), "flowers remains 520")
        self.assertEqual(self.p1.update("flower", -520,6), "No item here")
        

        self.assertEqual(self.p3.update("flowerss", -520,6), "No item here")
        #problem here
        self.assertEqual(self.p3.update("A", 100,10), "Suggest to adjust the price.A remains 300")
        self.assertEqual(self.p3.update("A", -200), "A remains 100")
        
    def testdelete(self):
        self.assertEqual(self.p2.delete("flowers"),"Have removed flowers" )
        # self.assertEqual(self.p2.delete("flowers"),"We don't have such kind of item" )
        # self.assertEqual(self.p3.delete("A"),"Have removed A" )
        self.assertEqual(self.p3.delete("flowers"),"We don't have such kind of item" )
    def test__add__(self):
           self.assertEqual(self.p3+self.p2,('A', 200, 5.0) )
          # self.assertEqual(self.p3.delete("flowers"),"We don't have such kind of item" )
      
    def tearDown(self):
        print("tear down")
    @classmethod
    def tearDownClass(cls):
        print("tearDownClass\n")
# unittest.main(module="Testinventory_class")
