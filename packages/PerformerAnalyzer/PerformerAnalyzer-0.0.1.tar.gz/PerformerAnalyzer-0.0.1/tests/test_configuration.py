import unittest
from unittest.mock import patch
from data_processor.configuration import Config
import shutil
import os
import json
from data_transformer.custom_exception import UnsupportedDataType
class TestConfig(unittest.TestCase):
    """
    Test case for class configuration.
    """
    @classmethod
    def setUpClass(cls):
        """
        Create a temporary directory for testing
        """
        cls.test_dir = os.path.join(os.getcwd(), 'test_config')
        os.makedirs(cls.test_dir, exist_ok=True)
    def setUp(self):
        """
        Create a temporary config file for testing
        """
        self.config_file = os.path.join(self.test_dir, 'config.json')
        with open(self.config_file, 'w') as json_file:
            json.dump({
                'path': 'example.csv',
                'data_type': 'CSV',
                'entity_collection': 'employees',
                'base_field': 'id',
                'computable_fields': ['salary', 'bonus']
            }, json_file)
    '''@patch('builtins.input', side_effect=['y'])
    def test_is_valid_config_valid_file(self, mock_input):
        """
        Initialize Config with the temporary config file
        """
        # valid file
        config = Config()
        self.assertIsNotNone(config)
        #self.assertFalse(config.is_valid_config())
        # invalid file
        config_file_invalid_type = os.path.join(self.test_dir, 'config_invalid_type.txt')
        with open(config_file_invalid_type, 'w') as txt_file:
            txt_file.write('This is an invalid file content.')
        # Initialize Config with the temporary config file
        config = Config()
        config.path = config_file_invalid_type
        # Assert that is_valid_config returns False for an invalid file type
        #with self.assertRaises(UnsupportedDataType):
            #config.is_valid_config()
        self.assertIsNotNone(config.read_config())'''

    def test_write_config(self):
        """
        Read the written config file and check if the values match
        """
        config = Config()
        config.data_type = 'CSV'
        config.entity_collection = 'employees'
        config.base_field = 'id'
        config.computable_fields = ['salary', 'bonus']
        config.path = os.path.join(self.test_dir, 'config.json')
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(config.path), exist_ok=True)
        config.write_config()
        with open(config.path, 'r') as written_file:
            written_data = json.load(written_file)
            self.assertEqual(written_data['data_type'], 'CSV')
            self.assertEqual(written_data['entity_collection'], 'employees')
            self.assertEqual(written_data['base_field'], 'id')
            self.assertEqual(written_data['computable_fields'], ['salary', 'bonus'])
    def tearDown(self):
        """
        Remove the temporary config file after each test
        """
        os.remove(self.config_file)
    @classmethod
    def tearDownClass(cls):
        """
        Remove the temporary directory after testing
        """
        shutil.rmtree(cls.test_dir)
