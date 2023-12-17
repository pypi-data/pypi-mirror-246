import unittest
from sklearn.datasets import make_classification
from ML_medic_kit.model_selection import train_test_multiple, create_classifier
from sklearn.model_selection import train_test_split


class TestModelSelection(unittest.TestCase):
    """Tests for the model_selection module."""

    def setUp(self):
        # Create a dataset for testing
        self.X, self.y = make_classification(n_samples=30, n_features=5,
                                             random_state=42)

    def test_create_classifier(self):
        """Test creating classifiers with different types."""

        # Test that a valid classifier is created
        for classifier_type in ["LogisticRegression", "RandomForest",
                                "MLPClassifier"]:
            model = create_classifier(classifier_type, self.X, self.y)
            self.assertIsNotNone(model)

    def test_invalid_classifier(self):
        """Test creating a classifier with an invalid type."""
        # Test that creating an invalid classifier type raises a ValueError
        with self.assertRaises(ValueError):
            create_classifier("InvalidType", self.X, self.y)

    def test_train_test_multiple(self):
        """Test training and testing multiple classifiers."""

        # Split the dataset for training and testing
        X_train, X_test, y_train, y_test = train_test_split(self.X,
                                                            self.y,
                                                            test_size=0.3,
                                                            random_state=42)

        classifiers = ["LogisticRegression", "RandomForest", "MLPClassifier"]

        # default results
        results, _ = train_test_multiple(classifiers, X_train, y_train, X_test,
                                         y_test, cv=3)

        # Check that the function returns a dictionary
        self.assertIsInstance(results, dict)

        # Check that each classifier is in the results
        # and has an evaluation key
        for classifier in classifiers:
            self.assertIn(classifier, results)
            self.assertIn('evaluation', results[classifier])
            self.assertIn('cv_mean_recall',
                          results[classifier]['evaluation'])
            self.assertIn('cv_std_recall',
                          results[classifier]['evaluation'])

        # Simple param_grids for testing
        param_grids = {
            "LogisticRegression": {"C": [1]},
            "RandomForest": {"n_estimators": [10]},
            "MLPClassifier": {"hidden_layer_sizes": [(50,)]}
        }

        # tuned results
        tuned_results, _ = train_test_multiple(classifiers, X_train,
                                               y_train, X_test, y_test,
                                               param_grids=param_grids,
                                               scoring='recall', cv=3,
                                               tune=True)

        # Check that the function returns a dictionary
        self.assertIsInstance(tuned_results, dict)

        # Check that each classifier is in the results
        # and has an evaluation key
        for classifier in classifiers:
            self.assertIn(classifier, tuned_results)
            self.assertIn('evaluation', tuned_results[classifier])
            self.assertIn('best_params', tuned_results[classifier])
            self.assertIn('cv_mean_recall',
                          tuned_results[classifier]['evaluation'])
            self.assertIn('cv_std_recall',
                          tuned_results[classifier]['evaluation'])


if __name__ == '__main__':
    unittest.main()
