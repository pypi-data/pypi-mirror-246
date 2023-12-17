import unittest
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from ML_medic_kit import cross_validation


class TestCrossValidation(unittest.TestCase):
    """Tests for the cross_validation module."""

    def setUp(self):
        # Create dataset for testing
        self.X, self.y = make_classification(n_samples=100, n_features=4,
                                             n_classes=2, random_state=42)

    def test_perform_cross_validation(self):
        """Test the perform_cross_validation function."""
        # Create model for testing
        model = LogisticRegression()

        # Perform cross-validation
        scores = cross_validation.perform_cross_validation(model, self.X,
                                                           self.y,
                                                           scoring='recall',
                                                           cv=5)

        # Check if the scores array is not empty
        self.assertTrue(len(scores) > 0)

        # Check if the scores array has the correct length of 5 (cv = 5)
        self.assertEqual(len(scores), 5)


if __name__ == '__main__':
    unittest.main()
