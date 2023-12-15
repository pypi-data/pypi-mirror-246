import unittest
import members


class Testmembers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")
        members.member()

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")

    def setUp(self):
        self.member1 = members.member(
            id=4, name="Bob", email="Bob@gmail.com", phone="12345", address="kelowna")
        self.member2 = members.member(
            id=5, name="Nancy", email="Nancy@gmail.com", phone="678910", address="richmond")
        self.member3 = members.member(
            id=6, name="Maria", email="MA@gmail.com", phone="unknown", address="unknown")
        self.member4 = members.member(
            id=7, name="Mike", email="ME@gmail.com", phone="456788", address="Vancouver")

    def tearDown(self):
        print("tearDown")

    def test_check_premium_status(self):
        # premium membership threshold is 50000
        self.member3.total_consumption = 50000
        self.member4.total_consumption = 50001
        self.assertFalse(self.member1.check_premium_status(
        ), "default value of total consumption is 0, premium status is False")
        self.assertFalse(self.member2.check_premium_status(
        ), "default value of total consumption is 0, premium status is False")
        self.assertFalse(self.member3.check_premium_status(
        ),  "total consumption greater than 50000, premium status is True")
        self.assertTrue(self.member4.check_premium_status(
        ),  "total consumption greater than 50000, premium status is True")

    def test_add_deposit(self):
        # deposit = money * 1.05
        self.member1.add_deposit(1)
        self.member2.add_deposit(2)
        self.member3.add_deposit(100)
        self.member4.add_deposit(200)
        self.assertEqual(self.member1.deposit, 1.05)
        self.assertEqual(self.member2.deposit, 2.1)
        self.assertEqual(self.member3.deposit, 105)
        self.assertEqual(self.member4.deposit, 210)

    def test_add_credits(self):
        self.member1.add_credits(1)
        self.member2.add_credits(1)
        self.member3.add_credits(1)
        self.member4.add_credits(1)
        self.assertEqual(self.member1.account_credits, 1)
        self.assertEqual(self.member2.account_credits, 1)
        self.assertEqual(self.member3.account_credits, 1)
        self.assertEqual(self.member4.account_credits, 1)

    def test_add_consumption(self):
        self.member1.add_consumption(1)
        self.assertEqual(self.member1.total_consumption, 1)
        #self.assertEqual(self.member1.account_credits, 0.01)
        self.member2.add_consumption(50000)
        self.assertEqual(self.member2.total_consumption, 50000)
        #self.assertEqual(self.member2.account_credits, 500)
        self.member3.add_consumption(50001)
        self.assertEqual(self.member3.total_consumption, 50001)
        #self.assertEqual(self.member3.account_credits, 5000.1)
        self.member2.add_consumption(100)
        self.assertEqual(self.member2.total_consumption, 50100)
        #self.assertEqual(self.member2.account_credits, 500+10)

    def test_get_member_info(self):
        info_dict1 = {
            "id": 4,
            "name": "Bob",
            "email": "Bob@gmail.com",
            "phone": "12345",
            "address": "kelowna",
            "credits": 0.0,
            "deposit": 0.0,
            "total consumption amount": 0.0,
            "premium membership status": 0
        }
        info_dict2 = {
            "id": 5,
            "name": "Nancy",
            "email": "Nancy@gmail.com",
            "phone": "678910",
            "address": "richmond",
            "credits": 0.0,
            "deposit": 0.0,
            "total consumption amount": 0.0,
            "premium membership status": 0
        }
        info_dict3 = {
            "id": 6,
            "name": "Maria",
            "email": "MA@gmail.com",
            "phone": "unknown",
            "address": "unknown",
            "credits": 0.0,
            "deposit": 0.0,
            "total consumption amount": 0.0,
            "premium membership status": 0
        }
        info_dict4 = {
            "id": 7,
            "name": "Mike",
            "email": "ME@gmail.com",
            "phone": "456788",
            "address": "Vancouver",
            "credits": 0.0,
            "deposit": 0.0,
            "total consumption amount": 0.0,
            "premium membership status": 0
        }
        self.assertEqual(self.member1.get_member_info(), info_dict1)
        self.assertEqual(self.member2.get_member_info(), info_dict2)
        self.assertEqual(self.member3.get_member_info(), info_dict3)
        self.assertEqual(self.member4.get_member_info(), info_dict4)

    def test_change_email(self):
        self.member1.change_email("change1")
        # _class name__private attribute name
        self.assertEqual(self.member1._member__email, "change1")
        self.member2.change_email("change2")
        self.assertEqual(self.member2._member__email, "change2")
        self.member3.change_email("change3")
        self.assertEqual(self.member3._member__email, "change3")
        self.member4.change_email("change4")
        self.assertEqual(self.member4._member__email, "change4")

    def test_change_phone(self):
        self.member1.change_phone("change5")
        self.assertEqual(self.member1._member__phone, "change5")
        self.member2.change_phone("change6")
        self.assertEqual(self.member2._member__phone, "change6")
        self.member3.change_phone("change7")
        self.assertEqual(self.member3._member__phone, "change7")
        self.member4.change_phone("change8")
        self.assertEqual(self.member4._member__phone, "change8")

    def test_change_address(self):
        self.member1.change_address("change9")
        self.assertEqual(self.member1._member__address, "change9")
        self.member2.change_address("change10")
        self.assertEqual(self.member2._member__address, "change10")
        self.member3.change_address("change11")
        self.assertEqual(self.member3._member__address, "change11")
        self.member4.change_address("change12")
        self.assertEqual(self.member4._member__address, "change12")

    def test_create_new_member(self):
        input_values = ["8", "John Doe", "john@gmail.com",
                        "1234567", "123 Street Kelowna"]
        original_input = __builtins__["input"]
        __builtins__["input"] = lambda _: input_values.pop(0)
        new_member = members.create_new_member()
        __builtins__["input"] = original_input  # restore input() in the built-in name space
        self.assertIsInstance(new_member, members.member)
        self.assertEqual(new_member._member__id, '8')
        self.assertEqual(new_member._member__name, 'John Doe')
        self.assertEqual(new_member._member__email, 'john@gmail.com')
        self.assertEqual(new_member._member__phone, '1234567')
        self.assertEqual(new_member._member__address, '123 Street Kelowna')


unittest.main(argv=[''], verbosity=2, exit=False)
