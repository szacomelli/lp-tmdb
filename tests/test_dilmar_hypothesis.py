import unittest
import pandas as pd # type: ignore

import src.dilmar_hypothesis as dm

class TestDilmar_Hypothesis(unittest.TestCase):

    def test_expected_dilmar_hypothesis(self):
        try:
            dm.dilmar_hypothesis(10, 10)
            dm.dilmar_hypothesis(100, 100)
        except Exception as e:
            self.fail(f"one function failed with the exception: {e}")
    
    def test_empty_arguments_dilmar_hypothesis(self):
        with self.assertRaises(TypeError):
            dm.dilmar_hypothesis()
    
    def test_toohigh_arguments_dilmar_hypothesis(self):
        with self.assertRaises(ValueError):
            dm.dilmar_hypothesis(999999999999, 99999999)

    def test_invalid_arguments_dilmar_hypothesis(self):
        with self.assertRaises(TypeError):
            dm.dilmar_hypothesis("jk", "banana")
