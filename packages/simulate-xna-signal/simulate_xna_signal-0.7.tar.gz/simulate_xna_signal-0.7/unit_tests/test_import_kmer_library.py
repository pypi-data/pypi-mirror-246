import unittest
import pandas as pd
from unittest.mock import patch
from simulate_xna_signal import import_kmer_library

class TestYourFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    pass

# Test to check if the dataframes are not empty and have the expected structure

    @patch('pandas.read_csv')
    def test_import_kmer_library_not_empty(self, mock_read_csv):
        # Mocking the behavior of read_csv to avoid actual file I/O during the test
        mock_read_csv.return_value = pd.DataFrame({'KXmer': ['A', 'C', 'G'], 'Mean level': [1, 2, 3]})
        
        # Call the function
        import_kmer_library()
        
        # Access the generated dataframe
        result_dataframe = pd.concat.call_args[0][0]
        
        # Add assertions to check if the dataframe is not empty
        self.assertFalse(result_dataframe.empty, "The generated dataframe should not be empty")

@patch('pandas.read_csv')
    def test_import_kmer_library_dimensions(self, mock_read_csv):
        # Mocking the behavior of read_csv to avoid actual file I/O during the test
        mock_read_csv.return_value = pd.DataFrame({'KXmer': ['A', 'C', 'G'], 'Mean level': [1, 2, 3]})
        
        # Call the function
        import_kmer_library()
        
        # Access the generated dataframe
        result_dataframe = pd.concat.call_args[0][0]
        
        # Assertion to check dataframe dimensions
        self.assertEqual(result_dataframe.shape, (3, 2), "The generated dataframe should have 4352 rows and 2 columns")

if __name__ == '__main__':
    unittest.main()