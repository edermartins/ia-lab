import math

from LstmWrapper import LstmWrapper
from CommandLine import lstm_command_line_args

# Get command line arguments or default values if not arguments
args = lstm_command_line_args()

# Creating the wrapper
lstm_wrapper = LstmWrapper()

# Creating and setting the LSTM model
lstm_wrapper.create_setting_model(dataset_path=args.dataset_path, filter_stocks=args.filter_stocks, features=args.features, y_value=args.y_value, n_splits=args.n_splits, hidden_layers=args.hidden_layers, units=args.units)

# Training the model
lstm_wrapper.fit(epochs=args.epochs)

# Evaluating the model
score = lstm_wrapper.evaluate(verbose=args.verbose)
trainScore = score['train']
testScore = score['test']
print('Train Score: %.2f MSE (%.2f RMSE)' % (trainScore, math.sqrt(trainScore)))
print('Test Score: %.2f MSE (%.2f RMSE)' % (testScore, math.sqrt(testScore)))