import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf


def generate_data(filepath):
    """
    Generate data to be used in model training

    Separates data into features and labels,
     and splits into sets based on the value in dcode
    """
    db = pd.read_csv(filepath)
    enc_sex = OneHotEncoder(sparse_output=False)
    enc_age = OneHotEncoder(sparse_output=False)
    one_hot_sex = enc_sex.fit_transform(db['sex'].values.reshape(-1, 1))
    age = db[['age']].round(0)
    one_hot_age = enc_age.fit_transform(age['age'].values.reshape(-1, 1))

    # Get the indices matching a condition on a feature
    condition_indices = db[db['dcode'] == 0].index
    db = db.drop(['age', 'sex', 'scanner', 'euler', 'BrainSegVolNotVent', 'euler_med', 'sample', 'dcode',
                  'timepoint'], axis=1, inplace=False)

    # Create two new datasets based on the condition indices
    train_x = db.loc[condition_indices]
    test_x = db.loc[~db.index.isin(condition_indices)]

    y_data = np.concatenate((one_hot_age, one_hot_sex), axis=1).astype('float32')
    scaler = StandardScaler()
    train_x_norm = scaler.fit_transform(train_x)
    test_x_norm = scaler.transform(test_x)
    train_y = y_data[condition_indices, :]
    test_y = y_data[~db.index.isin(condition_indices), :]

    return train_x_norm, train_y, test_x_norm, test_y


def generate_data_thickness_only(filepath, validation_split=0.2, normalize=False):
    """ Generates data to be used in model training, returning data only from columns containing thickness data

    Args:
        filepath (str): path to the csv file containing the data
        validation_split (float): fraction of the data to be used for validation
        normalize (bool): whether to normalize the data

    Returns: train data, validation data and test data as numpy arrays, and the names of the columns in that order
    """

    db = pd.read_csv(filepath)
    enc_sex = OneHotEncoder(sparse_output=False)
    enc_age = OneHotEncoder(sparse_output=False)
    one_hot_sex = enc_sex.fit_transform(db['sex'].values.reshape(-1, 1))
    age = db[['age']].round(0)
    one_hot_age = enc_age.fit_transform(age['age'].values.reshape(-1, 1))
    condition_indices = db[db['dcode'] == 0].index
    # Select columns ending with '_thickness'
    thickness_columns = [col for col in db.columns if col.endswith('_thickness')]

    # Extract the data from the selected columns
    data = db[thickness_columns]

    data.to_csv(filepath + '/../thickness_data.csv', index=False)

    # Create two new datasets based on the condition indices
    train_x = data.loc[condition_indices]
    test_x = data.loc[~db.index.isin(condition_indices)]

    y_data = np.concatenate((one_hot_age, one_hot_sex), axis=1).astype('float32')
    scaler = StandardScaler()

    if normalize:
        train_x_norm = scaler.fit_transform(train_x)
        test_x_norm = scaler.transform(test_x)
    else:
        train_x_norm = train_x.values
        test_x_norm = test_x.values

    train_y = y_data[condition_indices, :]
    test_y = y_data[~db.index.isin(condition_indices), :]

    train_x, val_x, train_y, val_y = train_test_split(train_x_norm, train_y, test_size=validation_split,
                                                      random_state=42)
    val = tf.data.Dataset.from_tensor_slices((val_x, val_y))
    train = tf.data.Dataset.from_tensor_slices((train_x, train_y))
    test = tf.data.Dataset.from_tensor_slices((test_x_norm, test_y))

    return train, val, test, data.columns


def generate_data_thickness_only_analysis(filepath, normalize=False):
    db = pd.read_csv(filepath)
    enc_sex = OneHotEncoder(sparse_output=False)
    enc_age = OneHotEncoder(sparse_output=False)
    one_hot_sex = enc_sex.fit_transform(db['sex'].values.reshape(-1, 1))
    age = db[['age']].round(0)
    one_hot_age = enc_age.fit_transform(age['age'].values.reshape(-1, 1))
    condition_indices = db[db['dcode'] == 0].index
    # Select columns ending with '_thickness'
    thickness_columns = [col for col in db.columns if col.endswith('_thickness')]

    # Extract the data from the selected columns
    data = db[thickness_columns]

    data.to_csv(filepath + '/../thickness_data.csv', index=False)

    # Create two new datasets based on the condition indices
    train_x = data.loc[condition_indices]
    test_x = data.loc[~db.index.isin(condition_indices)]

    y_data = np.concatenate((one_hot_age, one_hot_sex), axis=1).astype('float32')
    scaler = StandardScaler()

    if normalize:
        train_x_norm = scaler.fit_transform(train_x)
        test_x_norm = scaler.transform(test_x)
    else:
        train_x_norm = train_x.values
        test_x_norm = test_x.values

    train_y = y_data[condition_indices, :]
    test_y = y_data[~db.index.isin(condition_indices), :]

    return (train_x_norm, train_y), (test_x_norm, test_y), data.columns


def data_train_test(filepath):
    """
    Generate data to be used in model training

    splits the data from the csv file into training test and validation sets
    """

    train_x, train_y, test_x, test_y = generate_data(filepath)
    train = tf.data.Dataset.from_tensor_slices((train_x, train_y))
    test = tf.data.Dataset.from_tensor_slices((test_x, test_y))
    return train, test


def data_validation(filepath, validation_split=0.2):
    """ Generate data to be used in model training

    splits the data from the csv file into training test and validation sets

    Args:
        filepath (str): path to the csv file containing the data
        validation_split (float): fraction of the data to be used for validation

    Returns: Tuple of tf.data.Dataset objects containing the training, validation and test data in that order.
    """
    train_x, train_y, test_x, test_y = generate_data(filepath)
    train_x, val_x, train_y, val_y = train_test_split(train_x, train_y, test_size=validation_split)
    train = tf.data.Dataset.from_tensor_slices((train_x, train_y))
    test = tf.data.Dataset.from_tensor_slices((test_x, test_y))
    val = tf.data.Dataset.from_tensor_slices((val_x, val_y))
    return train, val, test


def generate_feature_names(filepath):
    db = pd.read_csv(filepath)
    db = db.drop(['age', 'sex', 'scanner', 'euler', 'BrainSegVolNotVent', 'euler_med', 'sample', 'dcode',
                  'timepoint'], axis=1, inplace=False)
    return db.columns

#%%
