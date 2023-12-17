import unittest
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from ML_medic_kit.hyperparameter_tuning import tune_hyperparameters


class TestHyperparameterTuning(unittest.TestCase):
    """Tests for the hyperparameter_tuning module."""

    def setUp(self):
        # Create testing dataset
        self.X, self.y = make_classification(n_samples=100, n_features=5,
                                             random_state=42)

        # Create model
        self.model = RandomForestClassifier(random_state=42)

        #  Parameter grid for testing
        self.param_grid = {
            'n_estimators': [10, 50, 100],
            'max_depth': [None, 5, 10]
        }

    def test_tune_hyperparameters(self):
        # Perform hyperparameter tuning
        best_estimator, best_params, cv_results = tune_hyperparameters(
            self.model, self.param_grid, self.X, self.y)

        # Check if best_estimator is an instance of RandomForestClassifier
        self.assertIsInstance(best_estimator, RandomForestClassifier)

        # Check if best_params contains keys from param_grid
        self.assertTrue(all(key in self.param_grid for key in best_params))

        # Check if cv_results is a dictionary
        self.assertIsInstance(cv_results, dict)


if __name__ == '__main__':
    unittest.main()
