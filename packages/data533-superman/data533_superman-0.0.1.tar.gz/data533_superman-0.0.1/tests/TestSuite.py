# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 20:48:50 2023

@author: Administrator
"""

import unittest
import sys
sys.path.append('administer')
sys.path.append('customer')
from administer.Testinventory_class import TestInventory
from administer.Testinventory_rollback import Testrollback
#from administer.Testaccount import Testpromotion
from administer.Testaccount_promotion import Testpromotion
from administer.Testaccount_promotion1 import Testpromotion1
#from administer.Testinventory import TestInventory
import customer
from customer.test_members import Testmembers
from customer.test_transactions import Testtransactions
def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    #suite.addTest(TestInventory('testupdate'))
    #suite.addTest(TestInventory('testprofit'))
    #suite.addTest(Testpromotion('testPromotion'))                                            
    #suite.addTest(Testpromotion('testElimiate')) 
    #class-inventory
    suite.addTest(TestInventory('test__add__'))
    suite.addTest(TestInventory('test__int__'))
    suite.addTest(TestInventory('test__str__'))
    suite.addTest(TestInventory('testupdate'))
    suite.addTest(TestInventory('testprofit'))
    suite.addTest(TestInventory('testdelete'))
    #function-inventory
    suite.addTest(Testrollback('testrollback'))   
    suite.addTest(Testrollback('testrollback2'))   
    #function-account
    suite.addTest(Testpromotion1('testpromotion'))    
    suite.addTest(Testpromotion('testpromotion'))       
    suite.addTest(Testpromotion('testeliminate'))   

    suite.addTest(Testmembers('test_check_premium_status')) 
    suite.addTest(Testmembers('test_add_deposit'))
    suite.addTest(Testmembers('test_add_credits'))
    suite.addTest(Testmembers('test_add_consumption'))
    suite.addTest(Testmembers('test_get_member_info'))
    suite.addTest(Testmembers('test_change_email'))
    suite.addTest(Testmembers('test_change_phone'))
    suite.addTest(Testmembers('test_change_address'))
    suite.addTest(Testmembers('test_create_new_member'))
    suite.addTest(Testtransactions('test_write_review'))
    suite.addTest(Testtransactions('test_rate_order'))
    suite.addTest(Testtransactions('test_get_order_info'))
    suite.addTest(Testtransactions('test_get_order_total'))
    suite.addTest(Testtransactions('test_new_review'))
    suite.addTest(Testtransactions('test_new_rate'))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))
my_suite()