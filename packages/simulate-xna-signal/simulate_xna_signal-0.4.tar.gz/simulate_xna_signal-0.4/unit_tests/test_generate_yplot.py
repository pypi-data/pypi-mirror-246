import unittest
import pandas as pd
from unittest.mock import patch
from simulate_xna_signal import generate_yplot

class TestYourFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    pass


    @patch('builtins.input', return_value='ATGC')  # Mock user input
    def test_generate_yplot_list_dimensions(self, mock_input):
        # Mock the behavior of KXmer_signal
        mock_kxmer_signal = pd.DataFrame({'KXmer': ['ATGC', 'CGTA'], 'Mean level': [1.0, 2.0]})
        with patch('your_module_name.KXmer_signal', return_value=mock_kxmer_signal):
            # Call the function
            generate_yplot()

            # Access the generated y list
            y_list = y  # Assuming y is a global variable or declared in a scope accessible to the test

            # Add assertions to check if y_list has the same dimensions as KXmers
            self.assertIsInstance(y_list, list, "The generated y should be a list")
            self.assertEqual(len(y_list), len(KXmers), "The dimensions of y should be the same as KXmers")

if __name__ == '__main__':
    unittest.main()