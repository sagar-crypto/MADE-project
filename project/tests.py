import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import pandas as pd
import numpy as np
from dataProcessing import (
    connect_to_kaggle, downdload_kaggle_dataset, download_other_databases,
    checkIfExists, process_crop_irrigation, process_climate_change, store_in_sql
)

class TestDataProcessing(unittest.TestCase):

    @patch.dict('os.environ', {'KAGGLE_USERNAME': 'test_user', 'KAGGLE_KEY': 'test_key'})
    @patch('dataProcessing.KaggleApi')
    def test_connect_to_kaggle(self, mock_kaggle_api):
        mock_kaggle_api_instance = MagicMock()
        mock_kaggle_api.return_value = mock_kaggle_api_instance
        
        api = connect_to_kaggle()
        
        self.assertEqual(api, mock_kaggle_api_instance)
        mock_kaggle_api_instance.authenticate.assert_called_once()

    @patch('dataProcessing.requests.get')
    @patch('dataProcessing.os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_other_databases(self, mock_file, mock_makedirs, mock_requests_get):
        mock_response = MagicMock()
        mock_response.content = b'data'
        mock_requests_get.return_value = mock_response
        
        csv_links = {
            "test_file.csv": "http://example.com/test_file.csv"
        }
        
        download_other_databases('test_directory', csv_links)
        
        mock_makedirs.assert_called_once_with('test_directory', exist_ok=True)
        mock_requests_get.assert_called_once_with("http://example.com/test_file.csv")
        mock_file.assert_called_once_with('test_directory/test_file.csv', 'wb')
        mock_file().write.assert_called_once_with(b'data')

    @patch('dataProcessing.os.path.exists')
    def test_check_if_exists(self, mock_exists):
        mock_exists.side_effect = lambda x: x == "existing_file.csv"
        
        result = checkIfExists(["existing_file.csv"], "non_existing_file.csv")
        self.assertFalse(result)

        result = checkIfExists(["existing_file.csv"], "existing_file.csv")
        self.assertTrue(result)
if __name__ == "__main__":
    unittest.main()
