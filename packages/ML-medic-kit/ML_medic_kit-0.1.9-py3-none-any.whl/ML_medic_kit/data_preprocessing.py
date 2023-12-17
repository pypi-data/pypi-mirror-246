# Import required libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
import pkg_resources

def load_data(filename):
    """
    Load data from a CSV file within the package into a pandas DataFrame.

    Parameters:
        filename (str): The filename of the CSV file to be read.

    Returns:
        DataFrame: DataFrame containing the data read from the CSV file.
    """
    filepath = pkg_resources.resource_filename('ML_medic_kit', f'data/{filename}')
    data = pd.read_csv(filepath)
    return data


def clean_dataset(data, outcome_name='diagnosis',
                  disease_outcome=['B', 'M'], binary=False,
                  to_drop=['id', 'Unnamed: 32'], encode=False):
    """
    Cleans the dataset by converting outcome column to binary if necessary,
    encoding any non-numeric predictor variables, renaming the outcome column,
    replacing spaces in column names, and dropping unnecessary columns.
    The default settings are suitable for cleaning the Wisconsin Breast Cancer
    dataset.

    Parameters:
        data (DataFrame): The dataset to be cleaned.
        outcome_name (str): optional (default="diagnosis")
            Name of disease outcome column.
        disease_outcome (list): optional (default=["B", "M"])
            Name of disease outcome.
        binary (bool): optional (default=False)
            If disease outcome names are binary.
        to_drop (list): optional (default=["id", "Unnamed: 32"])
            Names of columns to drop from dataset.
        encode: False (bool) or list, optional (default=False)
            False if no predictor variables need to be encoded,
            otherwise list of column names containing non-numeric
            values that need to be encoded.

    Returns:
        data (DataFrame): The cleaned dataset.
    """
    # Convert the outcome column to binary values
    if not binary:
        data[outcome_name] = data[outcome_name].map({disease_outcome[0]: 0,
                                                     disease_outcome[1]: 1})

    # Rename the outcome column
    data.rename(columns={outcome_name: 'outcome'}, inplace=True)

    # Drop unnecessary columns
    if len(to_drop) > 0:
        data.drop(columns=to_drop, inplace=True, errors='ignore')

    # Encodes other non-numeric columns using label encoder
    if encode is not False:
        for enc in encode:
            le = LabelEncoder()
            data[enc] = le.fit(data[enc]).transform(data[enc])

    # Replace spaces with underscores in column names
    data.columns = data.columns.str.replace(' ', '_')

    # Make column names all lower case
    data.columns = map(str.lower, data.columns)

    return data


def test_train_split_data(data, test_size):
    """
    The function separates the 'outcome' column from the rest of the data,
    then splits the dataset into training and test sets while stratifying based
    on the 'outcome' column to maintain the same proportion of classes.

    Parameters:
        data (DataFrame): The dataset to be split.
        test_size (int): The proportion to be test data

    Returns:
        tuple: Tuple containing the training and testing subsets
               (X_train, X_test, Y_train, Y_test).
    """

    # Separate features and the outcome variable
    Y = data['outcome']
    X = data.drop('outcome', axis=1)

    # Split dataset into training and test sets
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=test_size, stratify=Y, random_state=21
    )

    return X_train, X_test, Y_train, Y_test


def standard_scale_data(X_train, X_test):
    """
    Standard scales the data by removing the mean and scaling to unit variance.

    Parameters:
        X_train (DataFrame): Training data.
        X_test (DataFrame): Testing data.

    Returns:
        X_train_scaled (DataFrame): Standard scaled training data.
        X_test_scaled (DataFrame): Standard scaled testing data.
    """

    # Initialize StandardScaler
    scaler = StandardScaler()

    # Fit scaler on training data and transform it
    X_train_scaled = scaler.fit_transform(X_train)

    # Apply same transformation to test data
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled


def apply_pca(X_train, X_test, n_components):
    """
    Applies PCA dimensionality reduction to the training and test sets.

    Parameters:
        X_train (array): Training data.
        X_test (array): Test data.
        n_components (int): The number of principal components to keep.

    Returns:
        X_train_pca (array): PCA transformed training data.
        X_test_pca (array): PCA transformed test data.
    """
    pca = PCA(n_components=n_components)

    # Fit PCA on training data and transform test data
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)

    return X_train_pca, X_test_pca
