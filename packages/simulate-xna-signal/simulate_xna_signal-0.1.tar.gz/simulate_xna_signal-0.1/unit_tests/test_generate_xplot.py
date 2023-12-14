import unittest
import pandas as pd
from unittest.mock import patch
from simulate_xna_signal import generate_xplot

class TestYourFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    pass

    @patch('builtins.input', return_value='ATGC')  # Mock user input
    
    def test_generate_xplot_list(self, mock_input):
        # Call the function
        generate_xplot()

        # Access the generated x list
        x_list = x  # Assuming x is a global variable or declared in a scope accessible to the test

        # Add assertions to check if x_list is a list and not empty
        self.assertIsInstance(x_list, list, "The generated x should be a list")
        self.assertTrue(x_list, "The generated x list should not be empty")

if __name__ == '__main__':
    unittest.main()