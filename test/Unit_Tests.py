"""Perform unit tests to ensure the functionality of some functions created in Main_Code.py.
There are seven unit tests in this programme.
=============================================

(1) test_write_key tests the functionality of write_key function
(2) test_load_key tests the functionality of load_key function
(3) test_encrypt_text_file tests the functionality of encrypt_text_file function
(4) test_pickle_dict tests the functionality of pickle_dict function
(5) test_json_dict tests the functionality of json_dict function
(6) test_create_dict tests the functionality of create_dict function
(7) test_receive_data tests the functionality of receive_data function
"""
import sys
sys.path.append("..")
from src import Main_Code
import unittest
import os


class Test_Main_Code(unittest.TestCase):

    def test_write_key(self):
        """This function tests whether the "write_key" can create an encryption key and store it
        in a file called "file_key.key". """
        Main_Code.write_key()
        # Obtain the current path of the directory
        current_path = os.getcwd()
        # List all the file names in the directory
        dir_list = os.listdir(current_path)
        # Check whether the file "file_key.key" exists in the directory.
        self.assertEqual('file_key.key' in dir_list, True)
        os.remove('file_key.key')

    def test_load_key(self):
        """This function tests whether the "load_key" can load the encryption key file."""
        Key = Main_Code.load_key()
        # Check whether the function returns a binary variable
        self.assertEqual(type(Key), bytes)

    def test_encrypt_text_file(self):
        """This function tests the functionality of the test_encrypt_text_file function and ensures a file can be
        encrypted correctly
        """
        Main_Code.write_key()
        Key = Main_Code.load_key()
        with open('temporary_test_file.txt', 'w') as f:
            f.write('Creating a test text file...')
        Main_Code.encrypt_text_file('temporary_test_file.txt', Key)
        # Obtain the current path of the directory
        current_path = os.getcwd()
        # List all the file names in the directory
        dir_list = os.listdir(current_path)
        # Check whether the file "file_key.key" exists in the directory.
        self.assertEqual('temporary_test_file_encrypted.txt' in dir_list, True)
        # Remove the temporary test files from the directory
        os.remove('temporary_test_file.txt')
        if 'temporary_test_file_encrypted.txt' in dir_list:
            os.remove('temporary_test_file_encrypted.txt')

    def test_pickle_dict(self):
        """This function tests "pickle_dict" and whether the function input can be serialised using pickle."""
        # Check if the pickle_dict can return binary object.
        return_value = Main_Code.pickle_dict('Testing pickle_dict function ...')
        self.assertEqual(type(return_value), bytes)

    def test_json_dict(self):
        """This function tests "json_dict" and whether the function input can be serialised using json."""
        # Create a test dictionary
        Dictionary = Main_Code.create_dict('Sarah Brown', 'Data Science and Artificial Intelligence', 65, 72, 50)
        # Check if the json_dict can return string .
        return_value = Main_Code.json_dict(Dictionary)
        self.assertEqual(type(return_value), str)

    def test_create_dict(self):
        """This function tests "create_dict" and checks whether the dictionary can be created in
        the correct format and type
        """
        # Check if the dictionary can be created by executing the function of Main_Code.create_dict().
        return_value = Main_Code.create_dict('Sarah Brown', 'Data Science and Artificial Intelligence', 65, 72, 50)
        # Make a list of the dictionary values
        Keys = []
        for Key in return_value.keys():
            Keys.append(Key)
        # Check if the function returns a value with type "dict"
        with self.subTest(1):
            self.assertEqual(type(return_value), dict)
        # Check if the values of the dictionary are the correct ones
        with self.subTest(2):
            self.assertEqual(Keys, ['Full Name', 'Programme', 'Grades', 'GPA'])

    def test_receive_data(self):
        """
        This function tests the "receive_data" function, where some data are given the user,
        including name of the student, name of the course, and his/her grades for Modules A, B and C.
        :return: name, course, grade_moduleA, grade_moduleB, grade_moduleC
        """
        name, course, grade_moduleA, grade_moduleB, grade_moduleC = Main_Code.receive_data()
        # Confirm the type of grade_moduleA, grade_moduleB and grade_moduleC data is a float number.
        with self.subTest(1):
            self.assertEqual(type(grade_moduleA), float)
        with self.subTest(2):
            self.assertEqual(type(grade_moduleB), float)
        with self.subTest(3):
            self.assertEqual(type(grade_moduleC), float)
        # Confirm the numbers assigned for grade_moduleA, grade_moduleB and grade_moduleC are greater than or equal to 0
        with self.subTest(4):
            self.assertGreaterEqual(grade_moduleA, 0)
        with self.subTest(5):
            self.assertGreaterEqual(grade_moduleB, 0)
        with self.subTest(6):
            self.assertGreaterEqual(grade_moduleC, 0)
        # Confirm the numbers assigned for grade_moduleA, grade_moduleB and grade_moduleC are less than or equal to 100.
        with self.subTest(7):
            self.assertLessEqual(grade_moduleA, 100)
        with self.subTest(8):
            self.assertLessEqual(grade_moduleB, 100)
        with self.subTest(9):
            self.assertLessEqual(grade_moduleC, 100)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
