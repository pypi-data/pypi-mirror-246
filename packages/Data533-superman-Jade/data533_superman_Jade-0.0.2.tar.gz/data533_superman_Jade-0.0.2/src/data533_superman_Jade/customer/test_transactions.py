import unittest
import transactions


class Testtransactions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")

    def setUp(self):
        self.trans1 = transactions.transaction(
            1, 2193, 'banana,apple', '1,2', '1,2', '1,4', '2023-12-06', 'bought salad and chips, good', '4')
        self.trans2 = transactions.transaction(
            2, 9884, 'lemon,orange', '1,2', '1,2', '1,4', '2023-12-06', 'great', '5')
        self.trans3 = transactions.transaction(
            2, 1052, 'bread,rice', '1,2', '1,2', '1,4', '2023-12-06', 'great quality', '5')
        self.trans4 = transactions.transaction(
            1, 1475, 'salad,chips', '1,3', '2,4', '2.0,12.0', '2023-12-08 10:53:41', 'bought salad and chips again, great quality', '5')

    def tearDown(self):
        print("tearDown")

    def test_write_review(self):
        self.trans1.write_review("+review1")
        self.assertEqual(self.trans1.order_review,
                         "bought salad and chips, good+review1")
        self.trans2.write_review("+review2")
        self.assertEqual(self.trans2.order_review, "great+review2")
        self.trans3.write_review("+review3")
        self.assertEqual(self.trans3.order_review, "great quality+review3")
        self.trans4.write_review("+review4")
        self.assertEqual(self.trans4.order_review,
                         "bought salad and chips again, great quality+review4")

    def test_rate_order(self):
        self.trans1.rate_order("5")
        self.assertEqual(self.trans1.order_rate, "5")
        self.trans2.rate_order("4")
        self.assertEqual(self.trans2.order_rate, "4")
        self.trans3.rate_order("3")
        self.assertEqual(self.trans3.order_rate, "3")
        self.trans4.rate_order("2")
        self.assertEqual(self.trans4.order_rate, "2")

    def test_get_order_info(self):
        info_dict1 = {
            "customer id": 1,
            "transaction id": 2193,
            "name": 'banana,apple',
            "quantity": '1,2',
            "price": '1,2',
            "value": '1,4',
            "transaction time": '2023-12-06',
            "review": 'bought salad and chips, good',
            "rate": '4'
        }
        info_dict2 = {
            "customer id": 2,
            "transaction id": 9884,
            "name": 'lemon,orange',
            "quantity": '1,2',
            "price": '1,2',
            "value": '1,4',
            "transaction time": '2023-12-06',
            "review": 'great',
            "rate": '5'
        }
        info_dict3 = {
            "customer id": 2,
            "transaction id": 1052,
            "name": 'bread,rice',
            "quantity": '1,2',
            "price": '1,2',
            "value": '1,4',
            "transaction time": '2023-12-06',
            "review": 'great quality',
            "rate": '5'
        }
        info_dict4 = {
            "customer id": 1,
            "transaction id": 1475,
            "name": 'salad,chips',
            "quantity": '1,3',
            "price": '2,4',
            "value": '2.0,12.0',
            "transaction time": '2023-12-08 10:53:41',
            "review": 'bought salad and chips again, great quality',
            "rate": '5'
        }
        self.assertEqual(self.trans1.get_order_info(), info_dict1)
        self.assertEqual(self.trans2.get_order_info(), info_dict2)
        self.assertEqual(self.trans3.get_order_info(), info_dict3)
        self.assertEqual(self.trans4.get_order_info(), info_dict4)

    def test_get_order_total(self):
        self.assertEqual(transactions.get_order_total(self.trans1), 5.0)
        self.assertEqual(transactions.get_order_total(self.trans2), 5.0)
        self.assertEqual(transactions.get_order_total(self.trans3), 5.0)
        self.assertEqual(transactions.get_order_total(self.trans4), 14.0)

    def test_new_review(self):
        input_values = ['review 1']
        original_inputs = __builtins__["input"]
        __builtins__["input"] = lambda _: input_values.pop(0)
        self.trans1_new = transactions.new_review(self.trans1)
        self.assertIsInstance(self.trans1_new, transactions.transaction)
        self.assertEqual(self.trans1_new.order_review,
                         "bought salad and chips, goodreview 1")

        input_values = ['review 2']
        __builtins__["input"] = lambda _: input_values.pop(0)
        self.trans2_new = transactions.new_review(self.trans2)
        self.assertIsInstance(self.trans2_new, transactions.transaction)
        self.assertEqual(self.trans2_new.order_review, "greatreview 2")
        __builtins__["input"] = original_inputs

    def test_new_rate(self):
        input_values = ['1']
        original_inputs = __builtins__["input"]
        __builtins__["input"] = lambda _: input_values.pop(0)
        self.trans3_new = transactions.new_rate(self.trans3)
        self.assertIsInstance(self.trans3_new, transactions.transaction)
        self.assertEqual(self.trans3_new.order_rate, "1")

        input_values = ['2']
        __builtins__["input"] = lambda _: input_values.pop(0)
        self.trans4_new = transactions.new_rate(self.trans4)
        self.assertIsInstance(self.trans4_new, transactions.transaction)
        self.assertEqual(self.trans4_new.order_rate, "2")
        __builtins__["input"] = original_inputs


unittest.main(argv=[''], verbosity=2, exit=False)
