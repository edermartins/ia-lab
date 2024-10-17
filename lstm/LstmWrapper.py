import pandas as pd
import numpy as np

from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential  # type: ignore
from tensorflow.keras.layers import Dense, LSTM, Dropout  # type: ignore
from tensorflow.keras.models import load_model
from pandas import DataFrame


class LstmWrapper:
    data_frame: DataFrame
    data_frame_loaded = False
    data_frame_scaled: DataFrame
    target_data_frame: DataFrame
    X_train, y_train, X_test, y_test = None, None, None, None
    features = None
    model: Sequential

    def __init__(self):
        pass

    def load_csv(self, path):
        """
        Loads a CSV file to a Pandas DataFrame
        :param path: Path relative for a CSV file
        """
        self.data_frame = pd.read_csv(path)
        self.data_frame_loaded = True

    def filter_data_frame(self, field_name, filter_text):
        # Create and return a DataFrame subset
        return self.data_frame[self.data_frame[field_name] == filter_text]

    def add_train(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

    def add_test(self, X_test, y_test):
        self.X_test = X_test
        self.y_test = y_test

    def set_features(self, features):
        self.features = features

    def generate_min_max_scaler(self, data_frame):
        # Scaling Min-Max
        scaler = MinMaxScaler()
        data_frame_scaled = scaler.fit_transform(data_frame[self.features])
        self.data_frame_scaled = pd.DataFrame(columns=self.features, data=data_frame_scaled, index=data_frame.index)

    def generate_target_data_frame(self, data_frame, variable):
        self.target_data_frame = pd.DataFrame(data_frame[variable])

    def generate_train_test(self, target_data_frame=None, n_splits=20):
        # Set Target Variable
        if not target_data_frame:
            target_data_frame = self.target_data_frame

        # Splitting to Training set and Test set
        time_split = TimeSeriesSplit(n_splits=n_splits)

        for train_index, test_index in time_split.split(self.data_frame_scaled):
            self.X_train, self.X_test = self.data_frame_scaled[:len(train_index)], self.data_frame_scaled[
                                                                                   len(train_index): (
                                                                                               len(train_index) + len(
                                                                                           test_index))]
            self.y_train, self.y_test = target_data_frame[:len(train_index)].values.ravel(), target_data_frame[
                                                                                             len(train_index): (
                                                                                                         len(train_index) + len(
                                                                                                     test_index))].values.ravel()

        # Process the data for LSTM
        train_X = np.array(self.X_train)
        test_X = np.array(self.X_test)
        self.X_train = train_X.reshape(self.X_train.shape[0], 1, self.X_train.shape[1])
        self.X_test = test_X.reshape(self.X_test.shape[0], 1, self.X_test.shape[1])

    def create_model(self, hidden_layers=1, units=10, dropout=0.01, units_output=1, activation='relu', optimizer='adam',
                     loss='mean_squared_error'):
        self.model = Sequential()
        # Creating the first layer
        self.model.add(LSTM(units=units, return_sequences=True, activation=activation,
                            input_shape=(self.X_train.shape[1], self.X_train.shape[2])))
        # Creating neurons for the hidden layers
        for size in range(hidden_layers):
            # Adding hidden layers
            self.model.add(LSTM(units=units, return_sequences=True, activation=activation))
            # Dropout
            self.model.add(Dropout(dropout))

        # Adding output layer with one neuron
        self.model.add(Dense(units=units_output))

        # Compiling RNN type LSTM
        self.model.compile(optimizer=optimizer, loss=loss)
        return self.model

    def fit(self, epochs=10, batch_size=32):
        # Predicting
        self.model.fit(self.X_train, self.y_train, epochs=epochs, batch_size=batch_size)

    def evaluate(self, verbose=0):
        # Evaluating the model
        return {'train': self.model.evaluate(self.X_train, self.y_train, verbose=verbose),
                'test': self.model.evaluate(self.X_test, self.y_test, verbose)}

    def save_model(self, path_with_name='lstm_stock.h5'):
        # Save the trained model
        self.model.save(path_with_name)

    def load_model(self, path_with_name='lstm_stock.h5'):
        # Load de trained model
        self.model = load_model(path_with_name)

    def create_setting_model(self, dataset_path : str, filter_stocks: dict, features: list, y_value : str, n_splits=5, hidden_layers=1, units=10):
        # Opening the dataset
        self.load_csv(dataset_path)

        # Filtering the Dataset to use one of fourteen
        filtered_data_frame = self.filter_data_frame(filter_stocks['filed_name'], filter_stocks['field_text'])

        self.set_features(features)

        # Generating the target
        self.generate_target_data_frame(filtered_data_frame, y_value)

        # Scaling
        self.generate_min_max_scaler(filtered_data_frame)

        # Splitting and Generating test and train
        self.generate_train_test(n_splits=n_splits)

        # Creating the model
        self.create_model(hidden_layers=hidden_layers, units=units)