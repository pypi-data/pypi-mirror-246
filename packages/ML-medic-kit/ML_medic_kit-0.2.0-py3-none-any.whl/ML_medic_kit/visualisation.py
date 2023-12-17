# Import required libraries
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import roc_auc_score, roc_curve
from ML_medic_kit.model_selection import create_classifier
import shap
import seaborn as sns
sns.set(color_codes=True)


def plot_class_distribution(data, column, title='Class Distribution'):
    """
    Plot the count of each value in the specified column.

    Parameters:
        data (DataFrame): The DataFrame containing the data.
        column (str): The column name for which the distribution
                      is to be plotted.
        title (str): The title of the plot.
        palette (str):  The color palette to use for the plot.

    Returns:
        None: Shows a count plot.
    """
    plt.figure(figsize=(8, 5))
    sns.countplot(x=data[column])

    # Add title and labels
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel('Count')

    # Show the plot
    plt.show()


def plot_explained_variance(X_scaled):
    """
    Plots the explained variance and cumulative explained variance
    for different numbers of components.

    Parameters:
        X_scaled (array): The scaled feature data.
    """
    pca = PCA().fit(X_scaled)
    explained_variance = pca.explained_variance_ratio_
    cumulative_explained_variance = explained_variance.cumsum()

    plt.figure(figsize=(14, 5))

    # Subplot 1: Explained Variance
    plt.subplot(1, 2, 1)
    plt.bar(range(1, len(explained_variance) + 1),
            explained_variance, alpha=0.5, align='center',
            label='Individual explained variance')
    plt.ylabel('Explained variance ratio')
    plt.xlabel('Principal component index')
    plt.title('Explained Variance by Different Principal Components')

    # Subplot 2: Cumulative Explained Variance
    plt.subplot(1, 2, 2)
    plt.step(range(1, len(cumulative_explained_variance) + 1),
             cumulative_explained_variance, where='mid',
             label='Cumulative explained variance')
    plt.ylabel('Cumulative explained variance ratio')
    plt.xlabel('Number of components')
    plt.title('Cumulative Explained Variance by Components')

    plt.show()


def correlation_heatmap(data, cmap='coolwarm', filt=['_se', '_worst'],
                        save_fig=False, filepath='n/a'):
    """
    Plot correlation heatmap of the data.

    Parameters:
        data (Dataframe): Dataset to plot.
        cmap (str): optional (default='coolwarm')
            Colour map of figure.
        filt (list): optional (default=['_se', '_worst'])
            Filters out columns with certain names not to plot.
        save_fig (bool): optional (default=False)
            If figure should be saved to specified location.
        filepath (str): optional (default='n/a')
            Filepath to save figure to.

    Returns:
        None: Plots a correlation heatmap.
    """
    # Create a copy of the data to avoid modifying original
    data_plot = data.copy()

    # Filters out columns with certain names
    for drop in filt:
        data_plot.drop(list(data_plot.filter(regex=drop)),
                       axis=1, inplace=True)

    # Calculates correlation
    correlation_matrix = data_plot.corr()

    # Sets figure with specified figure size
    plt.figure(figsize=(8, 6))
    # Plots heatmap
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    sns.heatmap(correlation_matrix, annot=True, cmap=cmap,
                fmt='.2f', linewidths=0.5, mask=mask)

    plt.xticks(rotation=90)
    plt.title('Correlation Heatmap')

    # Saves figure if required and prevents axis
    # labels being cut off with tight layout
    if save_fig:
        plt.tight_layout()
        plt.savefig(filepath, dpi=300)

    plt.show()


def plot_roc(models, X_test, y_test, title_prefix='',
             save_fig=False, filepath='n/a'):
    """
    Plots ROC curves for given models.

    Parameters:
        models (dict): Dictionary with model objects.
        X_test: Test set.
        y_test: Actual outcomes for the test set.
        title_prefix (str): Prefix for the plot titles.
        save_fig (bool): optional (default=False)
            If figure should be saved to specified location.
        filepath (str): optional (default='n/a')
            Filepath to save figure to.

    Returns:
        None: ROC curve plot.
    """
    num_classifiers = len(models)
    fig, axes = plt.subplots(1, num_classifiers,
                             figsize=(6 * num_classifiers, 5))

    # If there is only one classifier, convert axes to a list
    if num_classifiers == 1:
        axes = [axes]

    for i, (classifier, model) in enumerate(models.items()):
        ax = axes[i]

        # Check if the model has the predict_proba method
        if not hasattr(model, 'predict_proba'):
            raise ValueError((f'The model {classifier} does not '
                              f'support probability predictions.'))

        # Calculate ROC curve and AUC
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        auc_score = round(roc_auc_score(y_test, y_pred_proba), 4)

        # Plot the ROC curve on it's subplot
        ax.plot(fpr, tpr, label=f'AUC={auc_score}')
        ax.plot([0, 1], [0, 1], 'k--')  # Diagonal line
        ax.set_xlabel('1 – Specificity (False Positive Rate)')
        ax.set_ylabel('Sensitivity (True Positive Rate)')
        ax.set_title(f'{title_prefix}ROC Curve for {classifier}')
        ax.legend()
        ax.grid(True)

    plt.tight_layout()

    # Saves figure if required
    if save_fig:
        plt.savefig(filepath, dpi=300)

    plt.show()


def variables_based_outcome(data, var1, var2, cmap='PiYG',
                            save_fig=False, filepath='n/a'):
    """
    Plots two different variables from the data against each
    other and colour-codes them based on the disease outcome.

    Parameters:
        data (Dataframe): Dataset to plot.
        var1 + var2 (str): Names of variables in data to plot.
        cmap (str): optional (default='PiYG')
            Colour map to use in plot.
        save_fig (bool): optional (default=False)
            If figure should be saved to specified location.
        filepath (str): optional (default='n/a')
            Filepath to save figure to.

    Returns:
        None: Plots scatterplot of 2 variables.
    """
    # Sets figure with specified figure size
    fig = plt.figure(figsize=(5, 5))
    # Plots variables and colour-codes based on outcome
    plt.scatter(data[var1], data[var2], c=data['outcome'],
                cmap=cmap, s=5)

    # Axis labels
    var1_label = var1.title().replace('_', ' ')
    var2_label = var2.title().replace('_', ' ')
    plt.xlabel(var1_label)
    plt.ylabel(var2_label)

    # Saves figure if required
    if save_fig:
        plt.savefig(filepath, dpi=300)

    plt.show()


def histogram_based_outcome(data, label=['M', 'B'], colours=['b', 'r'],
                            filt=['_se', '_worst'], figsize=(8, 10),
                            save_fig=False, filepath='n/a'):
    """
    Plots stacked histogram for all features in the data based on the
    disease outcome.

    Parameters:
        data (Dataframe): Dataset to plot.
        label (list of str): optional (default=['M', 'B'])
            Names of outcome to label.
        colours (list of str): optional (default=['b', 'r'])
            Colours that represent outcomes.
        filt (list): optional (default=['_se', '_worst'])
            Filters out columns with certain names not to plot.
        save_fig (bool): optional (default=False)
            If figure should be saved to specified location.
        filepath (str): optional (default='n/a')
            Filepath to save figure to.

    Returns:
        None: Plots histogram of variables.
    """
    # Create a copy of the data to avoid modifying original
    data_plot = data.copy()

    # Sets up outcome to label graph
    outcome_1 = data_plot[data_plot['outcome'] == 1]
    outcome_0 = data_plot[data_plot['outcome'] == 0]

    # Locates only the features to plot
    # and filters out columns with certain names
    for drop in filt:
        data_plot.drop(list(data_plot.filter(regex=drop)),
                       axis=1, inplace=True)

    # Finds all features excluding the outcome column
    features = list(data_plot.loc[:, data_plot.columns != 'outcome'])
    nrows = math.ceil(len(features)/2)
    # Prevents error if not enough features to fill both sides
    if len(features) % 2 == 0:
        odd_num = False
    else:
        odd_num = True

    fig, axes = plt.subplots(nrows=nrows, ncols=2, figsize=figsize)
    axes = axes.ravel()

    # Plots each feature
    for ind, ax in enumerate(axes):
        if odd_num and ind >= len(features):
            break
        feats = data_plot[features[ind]]
        binwidth = (max(feats) - min(feats)) / 60
        ax.hist([outcome_1[features[ind]], outcome_0[features[ind]]],
                bins=np.arange(min(feats), max(feats)+binwidth, binwidth),
                stacked=True, label=label, color=colours)
        ax.legend(loc='best')
        label_name = features[ind].title().replace('_', ' ')
        ax.set_xlabel(label_name)

    plt.tight_layout()

    # Saves figure if required
    if save_fig:
        plt.savefig(filepath, dpi=300)

    plt.show()


def plot_confusion_matrix(results, title_prefix='',
                          save_fig=False, filepath='n/a'):
    """
    Plots confusion matrices for the given results.

    Parameters:
        results (dict): The results dictionary containing confusion matrices.
        title_prefix (str): optional (default='')
            The prefix title of each plot.
        save_fig (bool): optional (default=False)
            If figure should be saved to specified location.
        filepath (str): optional (default='n/a')
            Filepath to save figure to.

    Returns:
        None: Plots confusion matrices for each model.
    """
    # If there is only one classifier, convert axes to a list
    num_classifiers = len(results)
    num_rows = 1
    num_cols = num_classifiers

    # Create subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5))

    if num_classifiers == 1:
        axes = [axes]

    # Iterate over classifiers and their metrics
    for i, (classifier, metrics) in enumerate(results.items()):

        # Extract the confusion matrix from metrics
        confusion_matrix = np.array(metrics['confusion_matrix'])

        ax = axes[i]

        # Plot the confusion matrix as a heatmap
        sns.heatmap(confusion_matrix, annot=True, fmt='d',
                    cmap='Blues', cbar=False, ax=ax)

        # Set the title and axis labels
        ax.set_title(f'{title_prefix}Confusion Matrix for {classifier}')
        ax.set_xlabel('Predicted Label')
        ax.set_ylabel('True Label')

    # Adjust spacing between subplots
    plt.tight_layout()

    # Saves figure if required
    if save_fig:
        plt.savefig(filepath, dpi=300)

    # Show the plot
    plt.show()


def create_results_table(default_results, tuned_results):
    """
    Generate a results table comparing classifiers with and
    without hyperparameter tuning.

    Parameters:
        default_results (dict): A dictionary with classifier names
                                as keys and corresponding evaluation
                                metrics as values for the default models.
        tuned_results (dict): A dictionary with classifier names as keys,
                              where each value is another dictionary containing
                              the evaluation metrics for the tuned models.

    Returns:
        DataFrame: A DataFrame containing the performance metrics for each
                   classifier.
    """
    # Extract evaluation metrics and create DataFrame for default results
    default_metrics = {model: values['evaluation'] for model, values in
                       default_results.items()}
    default_df = pd.DataFrame(default_metrics).T
    default_df['Hyperparameter Tuning'] = 'No'

    # Extract evaluation metrics and create DataFrame for tuned results
    tuned_metrics = {model: values['evaluation'] for model, values in
                     tuned_results.items()}
    tuned_df = pd.DataFrame(tuned_metrics).T
    tuned_df['Hyperparameter Tuning'] = 'Yes'

    # Concatenate the two DataFrames
    results_df = pd.concat([default_df, tuned_df], axis=0).reset_index()
    results_df.rename(columns={'index': 'Classifier'}, inplace=True)

    # Reorder columns
    column_order = ['Classifier', 'Hyperparameter Tuning',
                    'specificity', 'recall', 'precision', 'accuracy',
                    'f1_score', 'roc_auc', 'cv_mean_recall', 'cv_std_recall']
    results_df = results_df[column_order]

    return results_df


def plot_shap(model, X_test, feature_names, plot_type='beeswarm'):
    """
    Plot SHAP values using a given model and test data.

    Parameters:
        model (object): A trained model.
        X_test (array): Test data.
        feature_names (list): List of feature names.
        plot_type (str): optional (default='beeswarm')
                         Type of SHAP plot to generate.

    Returns:
        None: This function will display a SHAP plot.
    """
    # If X_test is a numpy array, convert it to a DataFrame with feature names
    if isinstance(X_test, np.ndarray):
        X_test_df = pd.DataFrame(X_test, columns=feature_names)
    else:
        X_test_df = X_test

    # Create a SHAP explainer using the DataFrame
    explainer = shap.Explainer(model.predict, X_test_df)

    # Calculate SHAP values
    shap_values = explainer(X_test_df)

    # Create SHAP plot
    if plot_type == 'bar':
        shap.summary_plot(shap_values, X_test_df, plot_type=plot_type)
    elif plot_type == 'beeswarm':
        shap.plots.beeswarm(shap_values)
    else:
        raise ValueError("Invalid plot_type. Use 'bar' or 'beeswarm'.")

    plt.show()
