# test_userprofile.py module

import os
import io
import unittest
from unittest.mock import patch
import pandas as pd

from src.housemate_app.user.userprofile import load_user_profiles, create_profile_from_input, append_to_dataframe, save_dataframe_to_csv
from src.housemate_app.user.security import string_hash

class TestUserProfile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        # Create a temporary CSV file for testing
        self.test_csv_filename = 'test_user_profiles.csv'
        self.test_file_path = os.path.join(os.getcwd(), self.test_csv_filename)
        self.sample_data = {
            'name': ['Test User'],
            'age': [25],
            'email': ['test_user@example.com'],
            'username': ['hashed_test_user'],
            'password': ['hashed_password']
        }
        self.df = pd.DataFrame(self.sample_data)
        self.df.to_csv(self.test_file_path, index=False)

    def test_create_profile_from_input(self):
        # Simulate creating a user profile from user input
        profile_data = {
            'name': 'User 1',
            'age': 25,
            'email': 'user1@example.com',
            'username': 'username1',  # Keeping the original username and password
            'password': 'password1'
        }

        # Mock the user input process
        def mock_input(prompt):
            if 'Enter your name: ' in prompt:
                return profile_data['name']
            elif 'Enter your age: ' in prompt:
                return str(profile_data['age'])
            elif 'Enter your email: ' in prompt:
                return profile_data['email']
            elif 'Enter your username (8 characters or more): ' in prompt:
                return profile_data['username']
            elif 'Enter your password (8 characters or more): ' in prompt:
                return profile_data['password']

        with unittest.mock.patch('builtins.input', side_effect=mock_input):
            created_profile_data = create_profile_from_input()

        # Hash the username and password before assertion
        hashed_username = string_hash(profile_data['username'])
        hashed_password = string_hash(profile_data['password'])

        # Replace the original username and password with hashed values
        profile_data['username'] = hashed_username
        profile_data['password'] = hashed_password

        # Verify if the created profile matches the expected data
        self.assertEqual(created_profile_data, profile_data)
        self.assertEqual(len(created_profile_data), 5)
        self.assertEqual(created_profile_data['age'], 25)
        self.assertIn('user1@example.com', created_profile_data.values())

    def tearDown(self):
        # Remove the temporary CSV file after each test
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    @classmethod
    def tearDownClass(cls):
        pass

class TestAppendToDataFrame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up initial data for testing append_to_dataframe function
        cls.initial_data = {
            'name': ['User 1'],
            'age': [25],
            'email': ['user1@example.com'],
            'username': ['username1'],
            'password': ['password1']
        }
        cls.initial_df = pd.DataFrame(cls.initial_data)

    def setUp(self):
        pass

    def test_append_to_dataframe(self):
        # Append a new profile to the existing dataframe
        new_profile_data = {
            'name': 'User 2',
            'age': 30,
            'email': 'user2@example.com',
            'username': 'username2',
            'password': 'password2'
        }
        new_df = append_to_dataframe(self.initial_df, new_profile_data)

        # Verify if the new dataframe contains the added profile
        self.assertEqual(len(new_df), len(self.initial_df) + 1)
        self.assertListEqual(list(new_df.columns), list(self.initial_df.columns))
        self.assertIn('username2', new_df['username'].values)
        self.assertEqual(new_df.loc[new_df['username'] == 'username2', 'age'].values[0], 30)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

class TestSaveDataFrameToCSV(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up initial data for testing save_dataframe_to_csv function
        cls.test_data = {
            'name': ['User 1'],
            'age': [25],
            'email': ['user1@example.com'],
            'username': ['username1'],
            'password': ['password1']
        }
        cls.test_df = pd.DataFrame(cls.test_data)
        cls.test_file_path = os.path.join(os.getcwd(), 'test_save.csv')
        
    def setUp(self):
        pass

    def test_save_dataframe_to_csv(self):
        # Save the dataframe to a temporary CSV file
        save_dataframe_to_csv(self.test_df, self.test_file_path)

        # Check if the file was created and contains data
        self.assertTrue(os.path.exists(self.test_file_path))
        loaded_df = load_user_profiles(self.test_file_path)
        self.assertIsNotNone(loaded_df)
        self.assertEqual(len(loaded_df), len(self.test_df))
        self.assertListEqual(list(loaded_df.columns), list(self.test_df.columns))
        
    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        # Clean up class-level resources
        if os.path.exists(cls.test_file_path):
            os.remove(cls.test_file_path)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)


