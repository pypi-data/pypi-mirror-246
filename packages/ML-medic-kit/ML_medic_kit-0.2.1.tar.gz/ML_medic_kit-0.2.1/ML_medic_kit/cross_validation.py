from sklearn.model_selection import cross_val_score
import numpy as np


def perform_cross_validation(model, X, y, scoring, cv=5):
    """
    Perform cross-validation on a given model and dataset.

    Parameters:
        model (object): The object to use to fit the data.
        X (array): The data to fit.
        y (array): The target variable to try to predict.
        scoring (str): A scorer  object
        cv (int): Determines the cross-validation splits.

    Returns:
        scores (array): Array of scores of the estimator for each
                        run of the cross validation.
    """
    scores = cross_val_score(model, X, y, scoring=scoring, cv=cv)

    return scores
