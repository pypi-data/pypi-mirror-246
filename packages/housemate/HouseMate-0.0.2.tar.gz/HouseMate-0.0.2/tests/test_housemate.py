# test_housemate.py module

import profile
import unittest
from unittest.mock import patch, MagicMock

import sys
import io
import os
import pandas as pd
import random


from src.housemate_app.housemate import (
    main_menu,
    profile_menu,
    housemate_menu,
    rental_user_input,
    purchase_user_input,
    rental_main,
    purchase_main,
    rental_recommendation_main,
    get_file_path
)

from src.housemate_app.user.security import string_hash, reverse_hash, check_credentials
from src.housemate_app.user.userprofile import (
#    UserProfile,
    load_user_profiles,
    create_profile_from_input,
    append_to_dataframe,
    save_dataframe_to_csv
)
from src.housemate_app.user.userlogin import view_profile, edit_profile, delete_profile

from src.housemate_app.my_property.property import Property
from src.housemate_app.my_property.purchase import (
    Purchase,
    Condo,
    TownHome,
    Duplex,
    Bungalow,
    TwoStory,
    Mansion,
    gen_purchase,
    view_purchase_list,
    purchase_recommendation
)

from src.housemate_app.my_property.rental import (
    Rental,
    RentalCondo,
    RentalTownHome,
    RentalDuplex,
    RentalBungalow,
    RentalTwoStory,
    RentalMansion,
    gen_rental,
    view_rental_list,
    rental_recommendation
)


class TestMenus(unittest.TestCase):

    @ classmethod
    def classSetUp(clas):
        pass

    def setUp(self):
        self.main_output = (
            "Welcome to HouseMate! Please choose an option: \n"
            "1. Create Profile\n"
            "2. Login\n"
            "3. Exit HouseMate\n")
        self.profile_output = (
            "You are logged in. Please choose an option: \n"
            "1. View Profile Information\n"
            "2. Edit Profile\n"
            "3. Delete Profile\n"
            "4. View available homes\n"
            "5. Logout and return to the main menu\n"
        )
        self.housemate_output = (
            "Find a home today! Please choose an option: \n"
            "1. View ONLY recommended properties to rent\n"
            "2. View ONLY recommended properties to purchase\n"
            "3. View available rental properties\n"
            "4. View available purchase properties\n"
            "5. Return to the profile menu\n"
            "6. Logout and return to the main menu\n")

    @patch('builtins.input', side_effect=['1', '2', '3'])
    def test_main_menu_choices(self, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main_menu()
            self.assertEqual(mock_stdout.getvalue(), self.main_output)

    @patch('builtins.input', side_effect=['1', '2', '3', '4', '5'])
    def test_profile_menu_choices(self, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            profile_menu()
            self.assertEqual(mock_stdout.getvalue(), self.profile_output)

    @patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6'])
    def test_housemate_menu_choices(self, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            housemate_menu()
            self.assertEqual(mock_stdout.getvalue(), self.housemate_output)
  
# housemate.py 21% to 24%, overall 75% to 76%                  
    # @patch('sys.stdout', new_callable=io.StringIO)
    # @patch('builtins.input', side_effect=['1', '2', '3'])  # Mimicking user input
    # def test_main_menu_choices(self, mock_input, mock_stdout):
    #     main_menu()
    #     expected_output = (
    #         "Welcome to HouseMate! Please choose an option: \n"
    #         "1. Create Profile\n"
    #         "2. Login\n"
    #         "3. Exit HouseMate\n"
    #     )
    #     self.assertEqual(mock_stdout.getvalue(), expected_output)

    # @patch('sys.stdout', new_callable=io.StringIO)
    # @patch('builtins.input', side_effect=['1', '2', '3', '4', '5'])  # Mimicking user input
    # def test_profile_menu_choices(self, mock_input, mock_stdout):
    #     profile_menu()
    #     expected_output = (
    #         "You are logged in. Please choose an option: \n"
    #         "1. View Profile Information\n"
    #         "2. Edit Profile\n"
    #         "3. Delete Profile\n"
    #         "4. View available homes\n"
    #         "5. Logout and return to the main menu\n"
    #     )
    #     self.assertEqual(mock_stdout.getvalue(), expected_output)

    # @patch('sys.stdout', new_callable=io.StringIO)
    # @patch('builtins.input', side_effect=['1', '2', '3', '4', '5', '6'])  # Mimicking user input
    # def test_housemate_menu_choices(self, mock_input, mock_stdout):
    #     housemate_menu()
    #     expected_output = (
    #         "Find a home today! Please choose an option: \n"
    #         "1. View ONLY recommendated properties to rent\n"
    #         "2. View ONLY recommendated properties to purchase\n"
    #         "3. View available rental properties\n"
    #         "4. View available purchase properties\n"
    #         "5. Return to the profile menu\n"
    #         "6. Logout and return to the main menu\n"
    #     )
    #     self.assertEqual(mock_stdout.getvalue(), expected_output)
    
    # ------------------------------------------------------------------------------------- also 21% to 24%, 75% to 76%
    #     def setUp(self):
    #     self.main_output = (
    #         "Welcome to HouseMate! Please choose an option: \n"
    #         "1. Create Profile\n"
    #         "2. Login\n"
    #         "3. Exit HouseMate\n")
    #     self.profile_output = (
    #         "You are logged in. Please choose an option: \n"
    #         "1. View Profile Information\n"
    #         "2. Edit Profile\n"
    #         "3. Delete Profile\n"
    #         "4. View available homes\n"
    #         "5. Logout and return to the main menu\n"
    #     )
    #     self.housemate_output = (
    #         "Find a home today! Please choose an option: \n"
    #         "1. View ONLY recommended properties to rent\n"
    #         "2. View ONLY recommended properties to purchase\n"
    #         "3. View available rental properties\n"
    #         "4. View available purchase properties\n"
    #         "5. Return to the profile menu\n"
    #         "6. Logout and return to the main menu\n")

    # def test_main_menu_choices(self):
    #     with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
    #         main_menu()
    #         self.assertEqual(mock_stdout.getvalue(), self.main_output)

    # def test_profile_menu_choices(self):
    #     with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
    #         profile_menu()
    #         self.assertEqual(mock_stdout.getvalue(), self.profile_output)

    # def test_housemate_menu_choices(self):
    #     with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
    #         housemate_menu()
    #         self.assertEqual(mock_stdout.getvalue(), self.housemate_output)
            
# -----------------------------------------------------------------------------------------------------------------

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @classmethod
    def tearDownClass(cls):
        # tearDownClass is a requirement
        pass


class TestHelperFunctions(unittest.TestCase):
    @ classmethod
    def classSetUp(clas):
        pass

    def setUp(self):
        random.seed(123)

    def test_get_file_path(self):
        self.assertEqual(get_file_path(), os.getcwd()+"\\user_profiles.csv")

    @patch('builtins.input', return_value='tEsT')
    def test_rental_user_input(self, mock_input):
        self.assertEqual(rental_user_input(), 'test')

    @patch('builtins.input', return_value='ABCD')
    def test_purchase_user_input(self, mock_input):
        self.assertEqual(purchase_user_input(), 'abcd')

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @classmethod
    def tearDownClass(cls):
        # tearDownClass is a requirement
        pass


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)