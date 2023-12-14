import unittest
import pandas as pd
from unittest.mock import patch
from simulate_xna_signal import input_to_4mers

class TestYourFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    pass


def test_input_to_4mers(self):
        # Test the input_to_4mers function
        # Using patch to mock the user input
        with patch('builtins.input', return_value='ATGC'):
            input_to_4mers()
            # Assertions to check if the KXmers list is generated correctly

def test_empty_input() -> None:
    input = ""
    assert KXmers == []

def test_known_sequence() -> None: 
    input = "ATAGCTGAC"
    assert KXmers == ['ATAG', 'TAGC', 'AGCT', 'GCTG', 'CTGA', 'TGAC']
