# Imports required packages
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score


def model_metrics(model, X_test, y_test):
    """
    Calculates model metrics for machine learning models.

    Parameters:
        model: Machine learning model.
        X_test (Dataframe): Test feature set.
        y_test (Dataframe): Actual disease outcome for test set.

    Returns:
        metric (dict):
            spec (float):
                Specificity - Out of all the people that do not have
                the disease, how many got negative results?
            recall (float):
                Recall (Sensitivity) - Out of all the people that
                have the disease, how many got positive test results?
            prec (float):
                Precision - Out of all the examples that predicted
                as positive, how many are really positive?
            acc (float):
                Accuracy - Fraction of predictions that the model
                got right.
            f1 (float):
                F1 score - Measure of the harmonic mean of
                precision and recall.
            roc_auc (float):
                Area under ROC curve.
    """
    # Make predictions on test data
    y_pred = model.predict(X_test)

    # Creates confusion matrix between predictions and actual results
    cm = confusion_matrix(y_test, y_pred)

    # Finds true positives/negatives and false positives/negatives
    TP = cm[0][0]
    FP = cm[0][1]
    TN = cm[1][1]
    FN = cm[1][0]

    # Calculates model scoring metrics
    spec = TN/(TN+FP)
    recall = TP/(TP+FN)
    prec = TP/(TP+FP)
    f1 = 2 * ((prec*recall) / (prec+recall))
    accuracy = (TP + TN) / (TP + FP + TN + FN)

    # Initialize roc_auc to None
    roc_auc = None

    # Check if the model has the predict_proba method for ROC-AUC calculation
    if hasattr(model, 'predict_proba'):
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        roc_auc = roc_auc_score(y_test, y_pred_proba)

    # Puts scores in metrics dict
    metrics = {
        'specificity': round(spec, 2),
        'recall': round(recall, 2),
        'precision': round(prec, 2),
        'accuracy': round(accuracy, 2),
        'f1_score': round(f1, 2),
        'roc_auc': round(roc_auc, 2) if roc_auc is not None else None
    }

    # Add confusion matrix to metrics
    metrics['confusion_matrix'] = cm.tolist()

    return metrics


def find_best_model(default_results, tuned_results, metric):
    """
    Find the best model(s) based on a specified evaluation metric.

    Parameters:
        default_results (dict): Dictionary with default model results.
        tuned_results (dict): Dictionary with tuned model results.
        metric (str): The metric to compare.

    Returns:
        list: List of dictionaries containing information about
              the best model(s).

    Raises:
        ValueError: If the provided metric is not valid.
    """
    # Initialize variables
    best_models = []
    best_score = float('-inf')

    # Check the specified evaluation metric is in results
    # If not, raise a value error
    check1 = default_results[next(iter(default_results))]['evaluation']
    check2 = tuned_results[next(iter(tuned_results))]['evaluation']
    comment = f"The metric '{metric}' is not a valid evaluation metric."
    if metric not in check1:
        raise ValueError(comment)
    elif metric not in check2:
        raise ValueError(comment)

    # Check in default results
    for model, data in default_results.items():
        # Get the score for the specified metric
        score = data['evaluation'].get(metric, float('-inf'))
        # Check if this score is better or the same
        if score > best_score:
            best_models = [{"Best Model": model, "Best Score": score,
                            "Is Tuned": False, "Hyperparameters": "default"}]
            best_score = score
        elif score == best_score:
            best_models.append({"Best Model": model, "Best Score": score,
                                "Is Tuned": False,
                                "Hyperparameters": "default"})

    # Check in tuned results
    for model, data in tuned_results.items():
        # Get the score for the specified metric
        score = data['evaluation'].get(metric, float('-inf'))
        # Check if this score is better or the same
        if score > best_score:
            best_models = [{"Best Model": model, "Best Score": score,
                            "Is Tuned": True,
                            "Hyperparameters": data.get('best_params', None)}]
            best_score = score
        elif score == best_score:
            best_models.append({"Best Model": model, "Best Score": score,
                                "Is Tuned": True,
                                "Hyperparameters": data.get('best_params',
                                                            None)})

    return best_models
