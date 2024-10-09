import unittest
import pandas as pd

from src.filter import filter_second, filter_third

class TestFilter(unittest.TestCase):

    def test_normal_nodate_filter_second(self):
        try:
            result_df = filter_second(100)
            self.assertIsInstance(result_df, pd.DataFrame)  # check result is a DataFrame
        except Exception as e:
            self.fail(f"filter_second failed to filter the dataset with the exception: {e}")
    
    def test_noarguments_filter_second(self):
        with self.assertRaises(TypeError):
            filter_second()

    def test_lotofshows_filter_second(self):
        with self.assertWarns(Warning):
                    filter_second(10000000)
    
    def test_invalid_date1_filter_second(self):
         with self.assertRaises(ValueError):
            filter_second(10, [2025, 2024])

    def test_invalid_date2_filter_second(self):
         with self.assertRaises(TypeError):
            filter_second(10, [2025])

    def test_invalid_date3_filter_second(self):
         with self.assertRaises(TypeError):
            filter_second(10, [2025, "abacate"])
            
    def test_invalid_date4_filter_second(self):
         with self.assertRaises(TypeError):
            filter_second(10, ['oi', "abacate"])
    
    def test_noarguments_filter_third(self):
        with self.assertRaises(TypeError):
            filter_third()

    def test_normal_filter_third(self):
        try:
            result_df = filter_third(100, 10000000000000)
            self.assertIsInstance(result_df, pd.DataFrame)  # check result is a DataFrame
        except Exception as e:
            self.fail(f"filter_second failed to filter the dataset with the exception: {e}")

    def test_lotofshows_filter_second(self):
        with self.assertWarns(Warning):
                    filter_third(10000000)