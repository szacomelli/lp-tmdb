import unittest
import pandas as pd
import numpy as np
from src.filter import filter_first
from src.leonado_hypothesis import bins_IQR, bins_with_outliers, display_analysis, analysis, plot_charts


class TestBins(unittest.TestCase):

    def setUp(self):
        self.valid_df = pd.DataFrame({
            'name': ['Serie A', 'Serie B', 'Serie C', 'Serie D', 'Serie E', 
                     'Serie F', 'Serie G', 'Serie H', 'Serie I', 'Serie J'],
            'avg_ep_per_season': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            'number_of_episodes': [50, 100, 150, 200, 250, 300, 350, 400, 450, 500],
            'vote_average': [6.9, 7.5, 7.5, 8.2, 5.2, 7.6, 4.8, 3.9, 9.1, 6.7],
            'popularity': [200, 150, 180, 220, 170, 160, 190, 200, 210, 180]
        })

    def test_bins_IQR_valid(self):
        bin_edges, labels = bins_IQR(self.valid_df)
        expected_bin_edges = np.array([0, 5, 10, 15, 21, 26, 31, 36, 42, 47, 52, 57, 63, 68, 73, 78, 84, 89, 94, 100])
        expected_labels = ['0-4', '5-9', '10-14', '15-20', '21-25', '26-30', '31-35', '36-41', '42-46', '47-51', 
                           '52-56', '57-62', '63-67', '68-72', '73-77', '78-83', '84-88', '89-93', '94 or more']
        np.testing.assert_array_equal(bin_edges, expected_bin_edges)
        self.assertEqual(labels, expected_labels)

    def test_bins_IQR_invalid_dataframe_type(self):
        with self.assertRaises(TypeError):
            bins_IQR("Abacate")
        with self.assertRaises(TypeError):
            bins_IQR(15154021)
        with self.assertRaises(TypeError):
            bins_IQR(-5464421)
        with self.assertRaises(TypeError):
            bins_IQR("%&¨%&$%&¨*¨&%$)")
            

    def test_bins_IQR_missing_column(self):
        df_missing_col = self.valid_df.drop(columns=['avg_ep_per_season'])
        with self.assertRaises(ValueError):
            bins_IQR(df_missing_col)

    def test_bins_IQR_empty_dataframe(self):
        empty_df = pd.DataFrame()
        with self.assertRaises(ValueError):
            bins_IQR(empty_df)
    
    def test_bins_with_outliers(self):
        bin_edges, labels = bins_with_outliers(self.valid_df, num_bins=5)
        expected_bin_edges = np.array([0, 20, 40, 60, 80, 100])
        expected_labels = ['0-19', '20-39', '40-59', '60-79', '80 or more']
        np.testing.assert_array_equal(bin_edges, expected_bin_edges)
        self.assertEqual(labels, expected_labels)

    def test_bins_with_outliers_invalid_bins(self):
        with self.assertRaises(ValueError):
            bins_with_outliers(self.valid_df, 0)
        with self.assertRaises(ValueError):
            bins_with_outliers(self.valid_df, "abacate")
        with self.assertRaises(ValueError):
            bins_with_outliers("abacate", 0)
        with self.assertRaises(ValueError):
            bins_with_outliers(0, "abacate")
        with self.assertRaises(TypeError):
            bins_with_outliers(0, 10)
        with self.assertRaises(TypeError):
            bins_with_outliers("abacate", 10)      

class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.valid_df = pd.DataFrame({
            'name': ['Serie A', 'Serie B', 'Serie C', 'Serie D', 'Serie E'],
            'number_of_episodes': [50, 100, 200, 250, 300],
            'number_of_seasons': [2, 5, 10, 12, 15],
            'avg_ep_per_season': [25.0, 20.0, 20.0, 20.8, 25.0],
            'vote_average': [7.5, 8.0, 7.9, 7.4, 7.8],
            'popularity': [150, 250, 300, 350, 400],
            'category_bin_iqr': ['20-24', '15-19', '15-19', '15-19', '20-24'],
            'category_bin_outliers': ['20-24', '15-19', '15-19', '15-19', '20-24']
        })

    def test_display_analysis(self):
        try:
            display_analysis(self.valid_df)
        except Exception as e:
            self.fail(f"Unexpected error: {e}")

    def test_display_analysis_empty_dataframe(self):
        empty_df = pd.DataFrame()
        with self.assertRaises(ValueError):
            display_analysis(empty_df)

    def test_display_analysis_missing_column(self):
        df_missing_column = self.valid_df.drop(columns=['avg_ep_per_season'])
        with self.assertRaises(ValueError):
            display_analysis(df_missing_column)

    def test_display_analysis_invalid_dataframe_type(self):
        with self.assertRaises(TypeError):
            display_analysis("abacate")
        with self.assertRaises(TypeError):
            display_analysis(555152154)
        with self.assertRaises(TypeError):
            display_analysis(-5464421)
        with self.assertRaises(TypeError):
            display_analysis("%&¨%&$%&¨*¨&%$)")

class TestePlot(unittest.TestCase):
    def setUp(self):
         self.valid_df = pd.DataFrame({
            'name': ['Serie A', 'Serie B', 'Serie C', 'Serie D', 'Serie E'],
            'number_of_episodes': [50, 100, 200, 250, 300],
            'number_of_seasons': [2, 5, 10, 12, 15],
            'avg_ep_per_season': [25.0, 20.0, 20.0, 20.8, 25.0],
            'vote_average': [7.5, 8.0, 7.9, 7.4, 7.8],
            'popularity': [150, 250, 300, 350, 400],
            'category_bin_iqr': ['20-24', '15-19', '15-19', '15-19', '20-24'],
            'category_bin_outliers': ['20-24', '15-19', '15-19', '15-19', '20-24']
        })

    def test_plot_charts(self):
        try:
            plot_charts(self.valid_df)
        except Exception as e:
            self.fail(f"Unexpected error: {e}")
        
    
        
if __name__ == '__main__':
    unittest.main()