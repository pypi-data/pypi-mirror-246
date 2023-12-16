# test_userlogin.py

import os
import unittest
from unittest.mock import patch
from io import StringIO
import pandas as pd

from src.housemate_app.user.userlogin import login_get_file_path, view_profile, edit_profile, delete_profile
from src.housemate_app.user.userprofile import load_user_profiles
from src.housemate_app.user.security import string_hash

class TestUserProfileLoading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a common temporary CSV file for all test cases in the class
        cls.test_csv_filename = 'user_profiles.csv'

    def setUp(self):
        # Create a temporary CSV file for each test method with the expected filename
        with open(self.test_csv_filename, 'w') as file:
            file.write('user1,25,user1@email.com,username1,password1\n')
            file.write('user2,30,user2@email.com,username2,password2\n')
            file.write('user3,28,user3@email.com,username3,password3\n')

    def test_login_get_file_path(self):
        # Test the login_get_file_path function
        expected_path = os.path.abspath(self.test_csv_filename)
        file_path = login_get_file_path()
        self.assertEqual(file_path, expected_path)

    def test_load_user_profiles(self):
        # Test the load_user_profiles function
        file_path = os.path.abspath(self.test_csv_filename)
        user_profiles = load_user_profiles(file_path)

        # Ensure user_profiles is a DataFrame and has data rows
        self.assertIsInstance(user_profiles, pd.DataFrame)
        self.assertGreater(len(user_profiles), 0)
        
        # Additional assertions for DataFrame structure
        # Check column names
        self.assertListEqual(list(user_profiles.columns), ['user1', '25', 'user1@email.com', 'username1', 'password1'])
        # Check number of columns
        self.assertEqual(len(user_profiles.columns), 5)
        # Check number of rows
        self.assertEqual(len(user_profiles.index), 2)

    def tearDown(self):
        # Remove the temporary CSV file created for each test method
        os.remove(self.test_csv_filename)

    @classmethod
    def tearDownClass(cls):
        # Clean up the common temporary CSV file created for all test cases in the class
        if os.path.exists(cls.test_csv_filename):
            os.remove(cls.test_csv_filename)

        
class TestViewProfile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a common temporary CSV file for all test cases in the class
        cls.test_csv_filename = 'user_profiles.csv'

    def setUp(self):
        # Create a temporary CSV file for each test method with the expected filename
        sample_data = {
            'name': ['User 1', 'User 2', 'User 3'],
            'age': [25, 30, 28],
            'email': ['user1@email.com', 'user2@email.com', 'user3@email.com'],
            'username': ['username1', 'username2', 'username3'],
            'password': ['password1', 'password2', 'password3']
        }
        self.df = pd.DataFrame(sample_data)
        self.df.to_csv(self.test_csv_filename, index=False)

    def test_view_profile_existing_user(self):
        # Test the view_profile function
        user_profile_data = {
            'name': ['User 1'],
            'age': [25],
            'email': ['user1@email.com'],
            'username': ['3337'],  # Hashed value for username to match
            'password': ['3479']   # Hashed value for password to match
        }
        user_df = pd.DataFrame(user_profile_data)

        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_output:
            view_profile('username1', user_df)
            captured_output = fake_output.getvalue().strip()

        expected_output = (
            "Profile Information:\n     name  age            email username password\n"
            "0  User 1   25  user1@email.com     3337     3479"
        ).strip()

        self.assertEqual(expected_output, captured_output)

        # Checking if the output contains 'Profile Information'
        self.assertIn('Profile Information', captured_output)

        # Ensure the output format matches the expected structure
        self.assertTrue(captured_output.startswith("Profile Information:"))
        self.assertTrue(captured_output.endswith("3479"))

        # Checking the length of the captured output
        self.assertGreater(len(captured_output), 0)

        # Checking specific values in the output
        self.assertIn('User 1', captured_output)
        self.assertIn('25', captured_output)
        self.assertIn('user1@email.com', captured_output)
        self.assertIn('3337', captured_output)
        self.assertIn('3479', captured_output)

    def test_view_profile_nonexistent_user(self):
        # Test the view_profile function for users that don't exist
        expected_output = "No profile information found for this user.\n"

        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_output:
            view_profile('nonexistent_user', self.df)
            captured_output = fake_output.getvalue()

        self.assertEqual(expected_output, captured_output)

        # Checking if the output contains 'No profile information found'
        self.assertIn('No profile information found', captured_output)

        # Checking the length of the captured output
        self.assertEqual(len(captured_output), len(expected_output))

        # Checking for the absence of specific values
        self.assertNotIn('User 1', captured_output)
        self.assertNotIn('25', captured_output)
        self.assertNotIn('user1@email.com', captured_output)
        self.assertNotIn('3337', captured_output)
        self.assertNotIn('3479', captured_output)

class TestEditProfile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary dataframe for each test method with the expected output
        cls.sample_data = {
            'name': ['User 1'],
            'age': [25],
            'email': ['new_email@email.com'],
            'username': ['username1'],
            'password': ['password1']
        }
        cls.df = pd.DataFrame(cls.sample_data)

    def setUp(self):
        pass

    @patch('builtins.input', side_effect=['email', 'new_email@email.com'])
    def test_edit_profile_existing_field(self, mock_input):
        # Test the edit_profile function
        expected_output = "Profile updated successfully!\n"
        result = edit_profile('user1', self.df)
        self.assertEqual(result, ("no_change", None))
        # Checking if the email field is updated in the dataframe
        self.assertEqual(self.df.loc[0, 'email'], 'new_email@email.com')

    @patch('builtins.input', side_effect=['invalid_field'])
    def test_edit_profile_invalid_field(self, mock_input):
        expected_output = "Invalid field name. Profile not updated.\n"
        result = edit_profile('user1', self.df)
        # Checking if there is an invalid input
        self.assertEqual(result, ("no_change", None))
        # Checking if the profile remains unchanged
        self.assertEqual(self.df.loc[0, 'email'], 'new_email@email.com')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        # Cleanup or reset any values that were modified in setUpClass
        cls.sample_data = None
        cls.df = None
        
class TestDeleteProfile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary CSV file for each test method with the expected filename
        cls.test_csv_filename = 'user_profiles.csv'
        cls.sample_data = {
            'name': ['User 1', 'User 2', 'User 3'],
            'age': [25, 30, 28],
            'email': ['user1@email.com', 'user2@email.com', 'user3@email.com'],
            'username': ['username1', 'username2', 'username3'],
            'password': ['password1', 'password2', 'password3']
        }
        cls.df = pd.DataFrame(cls.sample_data)
        cls.df.to_csv(cls.test_csv_filename, index=False)

    def setUp(self):
        pass

    @patch('builtins.input', return_value='yes')
    def test_delete_profile_confirmation_yes(self, mock_input):
        # Test the delete_profile function
        expected_output = "Profile deleted successfully!\n"
        result = delete_profile('username1', self.df)
        self.assertEqual(result, '3337')

    @patch('builtins.input', return_value='no')
    def test_delete_profile_confirmation_no(self, mock_input):
        expected_output = "Profile deletion canceled.\n"
        result = delete_profile('username1', self.df)
        self.assertEqual(result, '3337')
    
    @patch('builtins.input', side_effect=['yes'])
    def test_delete_profile_decorator(self, mock_input):
        # Define user data to simulate user's profile information
        user_profile_data = {
            'name': ['User 1'],
            'age': [25],
            'email': ['user1@email.com'],
            'username': ['3337'],  # Hashed value for username to match
            'password': ['3479']   # Hashed value for password to match
        }

        # Create a DataFrame with the user profile data
        user_df = pd.DataFrame(user_profile_data)

        # Simulate the function call and capture the output
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_output:
            delete_profile('username1', user_df)  # Pass the original username for testing
            captured_output = fake_output.getvalue().strip()

        expected_output = "Profile deleted successfully!"

        # Compare the captured output with the expected output
        self.assertEqual(expected_output, captured_output)

        # Checking if the profile is actually deleted from the DataFrame
        self.assertEqual(len(user_df), 0)  # Assuming profile deletion means empty DataFrame

    def tearDown(self):
        # Remove the temporary CSV file after each test
        if os.path.exists(self.test_csv_filename):
            os.remove(self.test_csv_filename)

    @classmethod
    def tearDownClass(cls):
        # Cleanup or reset any values that were modified in setUpClass
        cls.test_csv_filename = None
        cls.sample_data = None
        cls.df = None

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)


