# test_security.py module

import unittest
import pandas as pd

from src.housemate_app.user.security import string_hash, reverse_hash, check_credentials

class TestStringHash(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapped_strings = {}

    def setUp(self):
        pass

    def test_string_hash_basic(self):
        # Test for basic string hashing
        result = string_hash("This is a test to see what happens")
        self.assertEqual(result, 53286)
        self.assertNotEqual(result, 0)
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)

    def test_string_hash_sensitive_info(self):
        # Test for hashing sensitive information
        result = string_hash("SensitiveInformationIsHere")
        self.assertEqual(result, 33376)
        self.assertNotEqual(result, 0)
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)

    def test_string_hash_special_characters(self):
        # Test for hashing strings with numbers and symbols
        result = string_hash("What if there are numbers (333!) and symbols too?")
        self.assertEqual(result, 101197)
        self.assertNotEqual(result, 0)
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)
        
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.mapped_strings = None
class TestReverseHash(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapped_strings = {}

    def setUp(self):
        pass

    def test_reverse_hash_basic(self):
        # Test for reversing hashed values
        string_hashed = "This is a test to see what happens"
        hash_value = string_hash(string_hashed)
        self.mapped_strings[hash_value] = string_hashed

        result = reverse_hash(hash_value, self.mapped_strings)
        self.assertEqual(result, string_hashed)
        self.assertIsNotNone(result)
        self.assertNotEqual(result, "")
        self.assertIsInstance(result, str)

        # Test for a non-existent hash value
        result = reverse_hash(12345, self.mapped_strings)
        self.assertIsNone(result)

    def test_reverse_hash_sensitive_info(self):
        # Additional test cases for string_hash2
        string_hash2 = "SensitiveInformationIsHere"
        hash_value_2 = string_hash(string_hash2)

        self.mapped_strings[hash_value_2] = string_hash2

        result_2 = reverse_hash(hash_value_2, self.mapped_strings)

        self.assertEqual(result_2, string_hash2)
        self.assertIsNotNone(result_2)
        self.assertNotEqual(result_2, "")
        self.assertIsInstance(result_2, str)

    def test_reverse_hash_special_characters(self):
        # Additional test cases for string_hash3
        string_hash3 = "What if there are numbers (333!) and symbols too?"
        hash_value_3 = string_hash(string_hash3)

        self.mapped_strings[hash_value_3] = string_hash3

        result_3 = reverse_hash(hash_value_3, self.mapped_strings)

        self.assertEqual(result_3, string_hash3)
        self.assertIsNotNone(result_3)
        self.assertNotEqual(result_3, "")
        self.assertIsInstance(result_3, str)
        
    def tearDown(self):
        pass
        
    @classmethod
    def tearDownClass(cls):
        cls.mapped_strings = None
        
class TestCheckCredentials(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = pd.DataFrame({
            'username': [str(string_hash('username1'))],
            'password': [str(string_hash('password1'))]
        })
        cls.df2 = pd.DataFrame({
            'username': [str(string_hash('222222222'))],
            'password': [str(string_hash('222222222'))]
        })
        cls.df3 = pd.DataFrame({
            'username': [str(string_hash('username3!'))],
            'password': [str(string_hash('password3!'))]
        })
        cls.df4 = pd.DataFrame({
            'username': [str(string_hash('USERNAME4'))],
            'password': [str(string_hash('PASSWORD4'))]
        })

        cls.result_true1 = check_credentials('username1', 'password1', cls.df)
        cls.result_true2 = check_credentials('222222222', '222222222', cls.df2)
        cls.result_true3 = check_credentials('username3!', 'password3!', cls.df3)
        cls.result_true4 = check_credentials('USERNAME4', 'PASSWORD4', cls.df4)

        cls.result_false1 = check_credentials('Unknown1', 'Password1', cls.df)
        cls.result_false2 = check_credentials('333333333', '333333333', cls.df2)
        cls.result_false3 = check_credentials('Unknown3!', 'Password3!', cls.df3)
        cls.result_false4 = check_credentials('UNKNOWN', 'UNKNOWN', cls.df4)

        cls.result_none1 = check_credentials('username1', 'password1', None)
        cls.result_none2 = check_credentials('222222222', '222222222', None)
        cls.result_none3 = check_credentials('username3!', 'password3!', None)
        cls.result_none4 = check_credentials('USERNAME4', 'PASSWORD4', None)

    def setUp(self):
        pass

    def test_check_credentials_match(self):
        # Test for matching credentials in DataFrame
        self.assertTrue(self.result_true1)
        self.assertTrue(self.result_true2)
        self.assertTrue(self.result_true3)
        self.assertTrue(self.result_true4)

    def test_check_credentials_no_match(self):
        # Test for no matching credentials in DataFrame
        self.assertFalse(self.result_false1)
        self.assertFalse(self.result_false2)
        self.assertFalse(self.result_false3)
        self.assertFalse(self.result_false4)

    def test_check_credentials_none_df(self):
        # Test when df is None
        self.assertFalse(self.result_none1)
        self.assertFalse(self.result_none2)
        self.assertFalse(self.result_none3)
        self.assertFalse(self.result_none4)
        
    def tearDown(self):
        pass
        
    @classmethod
    def tearDownClass(cls):
        cls.df = None
        cls.df2 = None
        cls.df3 = None
        cls.df4 = None

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)


