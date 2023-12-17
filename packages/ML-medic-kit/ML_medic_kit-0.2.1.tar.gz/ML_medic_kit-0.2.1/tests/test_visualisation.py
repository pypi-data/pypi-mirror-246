import unittest
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from unittest.mock import patch
from ML_medic_kit.visualisation import (
    plot_class_distribution,
    plot_explained_variance,
    correlation_heatmap,
    plot_roc,
    variables_based_outcome,
    histogram_based_outcome,
    plot_confusion_matrix,
    create_results_table,
    plot_shap
)


class TestVisualisation(unittest.TestCase):
    """Tests for visulaisation module"""

    def setUp(self):
        # Create date frame for testing
        data = {'Category': ['B', 'B', 'M', 'M', 'B', 'B', 'M', 'B']}
        self.df = pd.DataFrame(data)
        self.X_test = np.array([[1, 2, 3], [4, 5, 6]])
        self.feature_names = ['feature1', 'feature2', 'feature3']
        self.model = RandomForestClassifier(random_state=42)

        # Generate synthetic training data
        X_train, y_train = make_classification(n_samples=100,
                                               n_features=3,
                                               n_informative=2,
                                               n_redundant=0,
                                               n_repeated=0,
                                               random_state=42)

        # Fit the model with the synthetic training data
        self.model.fit(X_train, y_train)

    def test_plot_class_distribution(self):
        with patch("matplotlib.pyplot.show") as show_patch:
            plot_class_distribution(self.df, 'Category',
                                    title='Test Distribution')
            show_patch.assert_called_once()

    def test_plot_explained_variance(self):
        with patch("matplotlib.pyplot.show") as show_patch:
            plot_explained_variance(self.X_test)
            show_patch.assert_called_once()

    def test_create_results_table(self):
        default_results = {
            'Model1': {'evaluation': {'specificity': 0.8, 'recall': 0.7,
                                      'f1_score': 0.7, 'accuracy': 0.85,
                                      'precision': 0.8, 'roc_auc': 0.98,
                                      'cv_mean_recall': 0.7,
                                      'cv_std_recall': 0.02}},
            'Model2': {'evaluation': {'specificity': 0.8, 'recall': 0.7,
                                      'f1_score': 0.7, 'accuracy': 0.85,
                                      'precision': 0.8, 'roc_auc': 0.98,
                                      'cv_mean_recall': 0.7,
                                      'cv_std_recall': 0.02}},
        }
        tuned_results = {
            'Model1': {'evaluation': {'specificity': 0.8, 'recall': 0.7,
                                      'f1_score': 0.7, 'accuracy': 0.85,
                                      'precision': 0.8, 'roc_auc': 0.98,
                                      'cv_mean_recall': 0.7,
                                      'cv_std_recall': 0.02}},
            'Model2': {'evaluation': {'specificity': 0.8, 'recall': 0.7,
                                      'f1_score': 0.7, 'accuracy': 0.85,
                                      'precision': 0.8, 'roc_auc': 0.98,
                                      'cv_mean_recall': 0.7,
                                      'cv_std_recall': 0.02}},
        }
        results_df = create_results_table(default_results, tuned_results)

        # Check the number of rows in the data frame
        self.assertEqual(len(results_df), 4)

    def test_plot_confusion_matrix(self):
        with patch("matplotlib.pyplot.show") as show_patch:
            results = {'Model1': {'confusion_matrix': [[1, 2], [3, 4]]},
                       'Model2': {'confusion_matrix': [[5, 6], [7, 8]]}}
            plot_confusion_matrix(results, title_prefix='Test')
            show_patch.assert_called_once()

    def test_correlation_heatmap(self):
        with patch("matplotlib.pyplot.show") as show_patch:
            data = pd.DataFrame(np.random.randn(10, 3),
                                columns=['A', 'B', 'C'])
            correlation_heatmap(data)
            show_patch.assert_called_once()

    def test_plot_roc(self):
        with patch("matplotlib.pyplot.show") as show_patch:
            X_test, y_test = make_classification(n_samples=100,
                                                 n_features=3,
                                                 n_informative=2,
                                                 n_redundant=0,
                                                 n_repeated=0,
                                                 random_state=42)
            models = {'RandomForest': self.model}
            plot_roc(models, X_test, y_test)
            show_patch.assert_called_once()

    def test_variables_based_outcome(self):
        with patch("matplotlib.pyplot.show") as show_patch:
            data = pd.DataFrame({'var1': np.random.rand(10),
                                 'var2': np.random.rand(10),
                                 'outcome': np.random.randint(0, 2, 10)})
            variables_based_outcome(data, 'var1', 'var2')
            show_patch.assert_called_once()

    def test_histogram_based_outcome(self):
        with patch("matplotlib.pyplot.show") as show_patch:
            data = pd.DataFrame({'feature1': np.random.rand(100),
                                 'feature2': np.random.rand(100),
                                 'outcome': np.random.randint(0, 2, 100)})
            histogram_based_outcome(data)
            show_patch.assert_called_once()

    def test_plot_shap(self):
        with patch("matplotlib.pyplot.show") as show_patch:
            X_test = np.random.rand(10, 3)
            feature_names = ['feature1', 'feature2', 'feature3']
            plot_shap(self.model, X_test, feature_names)
            # SHAP function generates two plots
            self.assertEqual(show_patch.call_count, 2)


if __name__ == '__main__':
    unittest.main()
