# Import required libraries
import unittest
import pandas as pd
from ML_medic_kit import data_preprocessing
from sklearn.decomposition import PCA
import numpy as np
from sklearn.preprocessing import StandardScaler


class TestDataPreprocessing(unittest.TestCase):
    """Tests for the 'data_preprocessing' module."""

    def test_load_data(self):
        """Test the load_data function to ensure it returns a DataFrame."""

        FILEPATH = "ML_medic_kit/data/breast_cancer_data.csv"

        data = data_preprocessing.load_data(FILEPATH)

        # Check if the result is a DataFrame
        self.assertIsInstance(data, pd.DataFrame)

    def test_clean_dataset(self):
        """Test the clean_dataset function to ensure it cleans
        the data properly.
        """
        # Define the test data
        test_data = pd.DataFrame({
            'diagnosis': ['B', 'M', 'B', 'M'],
            'id': [1, 2, 3, 4],
            'Unnamed:_32': [5, 6, 7, 8],
            'feature': [9, 10, 11, 12]
        })
        cleaned_data = data_preprocessing.clean_dataset(test_data)

        # Check if 'id' column is dropped
        self.assertNotIn('id', cleaned_data.columns)

        # Check if 'Unnamed:_32' column is dropped
        self.assertNotIn('Unnamed:_32', cleaned_data.columns)

        # Check if 'diagnosis' is renamed to 'outcome'
        self.assertIn('outcome', cleaned_data.columns)

    def test_train_test_split_data(self):
        """Test the test_train_split_data function to ensure
        proper data splitting.
        """
        # Define the test data
        test_data = pd.DataFrame({
            'outcome': [0, 1, 0, 1],
            'feature1': [1, 2, 3, 4],
            'feature2': [5, 6, 7, 8]
        })

        X_train, X_test, Y_train, Y_test = \
            data_preprocessing.test_train_split_data(test_data, test_size=0.3)

        # Check if train size is 70% of 4
        self.assertEqual(len(X_train), 2)

        # Check if test size is 30% of 4
        self.assertEqual(len(X_test), 2)

    def test_standard_scale_data(self):
        """Test the standard scaling function on the feature data."""
        test_features = pd.DataFrame({
            'outcome': [0, 1, 0, 1],
            'feature1': [1, 2, 3, 4],
            'feature2': [10, 20, 30, 40]
        })

        X_train, X_test, Y_train, Y_test = \
            data_preprocessing.test_train_split_data(test_features,
                                                     test_size=0.5)

        # Initialize StandardScaler
        scaler = StandardScaler()

        # Fit scaler on training data and transform it
        X_train_scaled = scaler.fit_transform(X_train)

        # Apply transformation to test data
        X_test_scaled = scaler.transform(X_test)

        # Check that scaled data has zero mean and unit variance
        self.assertTrue(np.allclose(X_train_scaled.mean(axis=0), 0))
        self.assertTrue(np.allclose(X_train_scaled.std(axis=0), 1))

    def test_apply_pca(self):
        """Test the apply_pca function."""

        # Test data
        X_train = np.array([[1, 2], [3, 4], [5, 6]])
        X_test = np.array([[7, 8], [9, 10]])

        # Number of components to keep
        n_components = 2

        # Apply PCA
        X_train_pca, X_test_pca = data_preprocessing.apply_pca(X_train, X_test,
                                                               n_components)

        # Check if the dimensions are correct
        self.assertEqual(X_train_pca.shape[1], n_components)
        self.assertEqual(X_test_pca.shape[1], n_components)


if __name__ == '__main__':
    unittest.main()
