from sklearn.model_selection import GridSearchCV


def tune_hyperparameters(model, param_grid, X_train, y_train,
                         scoring=None, cv=5):
    """
    Perform hyperparameter tuning for a given model using GridSearchCV.

    Parameters:
        model (Object): The model for hyperparameter tuning
        param_grid (dict): Dictionary specifying the hyperparameter
                           grid to search.
        X_train (array): Training data.
        y_train (array): target labels
        scoring (str): A scorer object.
        cv (int): Determines the cross-validation splits.

    Returns:
        best_estimator (object): The best estimator found during
                                 the grid search.
        best_params (dict): The parameters of the best estimator
        cv_results (dict): Cross-validation results for the best estimator.

    """
    # If no scoring metric is provided, default to recall
    if scoring is None:
        scoring = 'recall'

    # Perform hyperparameter tuning using GridSearchCV
    grid_search = GridSearchCV(model, param_grid, scoring=scoring, cv=cv,
                               return_train_score=True)
    grid_search.fit(X_train, y_train)

    # Return the best estimator, best hyperparameters
    # and cross-validation results
    return (grid_search.best_estimator_, grid_search.best_params_,
            grid_search.cv_results_)
