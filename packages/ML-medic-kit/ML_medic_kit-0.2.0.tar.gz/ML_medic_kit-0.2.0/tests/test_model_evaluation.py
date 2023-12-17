import unittest
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from ML_medic_kit.model_evaluation import model_metrics, find_best_model


class TestModelEvaluation(unittest.TestCase):
    """Tests for the model_evaluation module."""

    # Define test data
    default_results = {
        'RandomForestClassifierDefault': {
            'evaluation': {
                'accuracy': 0.85,
                'f1_score': 0.9,
            }
        }
    }

    tuned_results = {
        'RandomForestClassifierTuned': {
            'evaluation': {
                'accuracy': 0.88,
                'f1_score': 0.92,
            },
            'best_params': {'n_estimators': 200, 'max_depth': 10}
        }
    }

    def setUp(self):
        # Create a dataset
        self.X, self.y = make_classification(n_samples=30, n_features=5,
                                             random_state=42)

        # Train a model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(self.X, self.y)

    def test_model_metrics(self):
        # Calculate metrics using the model
        metrics = model_metrics(self.model, self.X, self.y)

        # Check if the metrics dictionary contains expected keys
        expected_keys = ['specificity', 'recall', 'precision',
                         'accuracy', 'f1_score', 'roc_auc', 'confusion_matrix']
        self.assertEqual(set(metrics.keys()), set(expected_keys))

    def test_find_best_model(self):
        # Find the best model based on accuracy
        best_models = find_best_model(self.default_results, self.tuned_results,
                                      'accuracy')

        # Check if the best_models list contains the expected model
        expected_best_models = [{'Best Model': 'RandomForestClassifierTuned',
                                 'Best Score': 0.88, 'Is Tuned': True,
                                 'Hyperparameters': {'n_estimators': 200,
                                                     'max_depth': 10}}]
        self.assertEqual(best_models, expected_best_models)


if __name__ == '__main__':
    unittest.main()
