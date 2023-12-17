# Import required libraries
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from ML_medic_kit.cross_validation import perform_cross_validation
from ML_medic_kit.model_evaluation import model_metrics
from ML_medic_kit.hyperparameter_tuning import tune_hyperparameters
import numpy as np


def create_classifier(classifier_type, X_train, y_train, RANDOM_SEED=42,
                      **params):
    """
    Create and fit a classifier based on the specified classifier_type.

    Parameters:
        classifier_type (str): Type of classifier to create.
        X_train (array): Training data.
        y_train (array): Target labels.
        **params: Additional hyperparameters to pass to the classifier.

    Returns:
        classifier: The trained classifier.
    Raises:
        ValueError: If an invalid classifier_type is provided.
    """
    # Create and fit a classifier based on the specified classifier_type
    if classifier_type == "LogisticRegression":
        model = LogisticRegression(random_state=RANDOM_SEED, **params)
    elif classifier_type == "RandomForest":
        model = RandomForestClassifier(random_state=RANDOM_SEED, **params)
    elif classifier_type == "MLPClassifier":
        model = MLPClassifier(random_state=RANDOM_SEED, **params)
    else:
        raise ValueError("Invalid classifier type")

    # Fit the model using the training data
    model.fit(X_train, y_train)

    # Return model
    return model


def train_test_multiple(classifiers, X_train, y_train, X_test, y_test,
                        param_grids=None, scoring='recall', cv=5,
                        tune=False, RANDOM_SEED=42):
    """
    Train and test multiple classifiers with or without hyperparameter tuning.

    Parameters:
        classifiers (list):  List of classifier names.
        X_train (array): Training features
        y_train (array): Training labels
        X_test (array): Test features
        param_grids (dict): Parameter grids for each classifier for
                            hyperparameter tuning.
        scoring: Scoring method to use for evaluation and cross-validation.
        cv (int): Number of cross-validation folds.
        tune: Whether to perform hyperparameter tuning.

    Returns:
        dict: A dictionary with evaluation results for each classifier.
        dict: A dictionary with the trained models
    """
    results = {}
    models = {}

    for classifier_type in classifiers:
        results[classifier_type] = {}

        # Create the model
        model = create_classifier(classifier_type, X_train, y_train,
                                  RANDOM_SEED=RANDOM_SEED)

        if tune and param_grids:
            # Perform hyperparameter tuning
            tuned_model, best_params, \
                grid_search_results = tune_hyperparameters(
                    model, param_grids[classifier_type], X_train,
                    y_train, scoring=scoring, cv=cv)
            results[classifier_type]['best_params'] = best_params
            cv_scores = grid_search_results['mean_test_score']
            model = tuned_model  # Use the tuned model for evaluation
        else:
            # Fit the model for default parameters
            model.fit(X_train, y_train)
            cv_scores = perform_cross_validation(model, X_train, y_train,
                                                 scoring=scoring, cv=cv)

        # Evaluate model performance
        metrics = model_metrics(model, X_test, y_test)
        metrics['cv_mean_recall'] = round(np.mean(cv_scores), 2)
        metrics['cv_std_recall'] = round(np.std(cv_scores), 2)

        results[classifier_type]['evaluation'] = metrics
        models[classifier_type] = model

        # Store evaluation metrics and confusion matrix
        results[classifier_type]['evaluation'] = metrics
        results[classifier_type]['confusion_matrix'] = \
            metrics['confusion_matrix']

    return results, models
