import unittest
import pandas as pd

from src.silvio_hypothesis import most_frequent_genre, most_popular_genre, most_voted_genre, plot_bar

class TestSilvio_Hypothesis(unittest.TestCase):

    def test_expected_most_frequent_genre(self):
        try:
            most_frequent_genre(10)
            most_frequent_genre(10, 10)
            most_frequent_genre(100, 1, [2023,2024])
        except Exception as e:
            self.fail(f"one function failed with the exception: {e}")
    
    def test_empty_arguments_most_frequent_genre(self):
        with self.assertRaises(TypeError):
            most_frequent_genre()

    def test_empty_arguments_most_popular_genre(self):
        with self.assertRaises(TypeError):
            most_popular_genre()

    def test_empty_arguments_most_voted_genre(self):
        with self.assertRaises(TypeError):
            most_voted_genre()
    
    def test_toohigh_arguments_most_frequent_genre(self):
        with self.assertRaises(ValueError):
            most_frequent_genre(100000000000, 10000000000000000)

    def test_toohigh_arguments_most_popular_genre(self):
        with self.assertRaises(ValueError):
            most_popular_genre(100000000000, 10000000000000000)

    def test_toohigh_arguments_most_voted_genre(self):
        with self.assertRaises(ValueError):
            most_voted_genre(100000000000, 10000000000000000)

    def test_invalid_date1_most_frequent_genre(self):
        with self.assertRaises(ValueError):
            most_frequent_genre(10, 10, [2025,2024])

    def test_invalid_date1_most_popular_genre(self):
        with self.assertRaises(ValueError):
            most_popular_genre(10, 10, [2025,2024])

    def test_invalid_date1_most_voted_genre(self):
        with self.assertRaises(ValueError):
            most_voted_genre(10, 10, [2025,2024])

    def test_invalid_date2_most_frequent_genre(self):
        with self.assertRaises(TypeError):
            most_frequent_genre(10, 10, [289])

    def test_invalid_date2_most_popular_genre(self):
        with self.assertRaises(TypeError):
            most_popular_genre(10, 10, [289])

    def test_invalid_date2_most_voted_genre(self):
        with self.assertRaises(TypeError):
            most_voted_genre(10, 10, [289])

    def test_invalid_arguments_most_frequent_genre(self):
        with self.assertRaises(TypeError):
            most_frequent_genre("kajhsdasd", "leão")

    def test_invalid_arguments_most_popular_genre(self):
        with self.assertRaises(TypeError):
            most_popular_genre("kajhsdasd", "leão")

    def test_invalid_arguments_most_voted_genre(self):
        with self.assertRaises(TypeError):
            most_voted_genre("kajhsdasd", "leão")

if __file__ == "__main__":
    unittest.main()
