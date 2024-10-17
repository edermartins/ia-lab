from ast import literal_eval
from types import SimpleNamespace
import argparse

def lstm_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset_path', metavar="", type=str, help="path to dataset. Default: 'data/big_tech_stock_prices.csv'", default='data/big_tech_stock_prices.csv')
    parser.add_argument('-fs', '--filter_stocks', metavar="", type=str, help='Column name and value to be filtered (between quotes and with no spaces). Default: "{\'filed_name\':\'stock_symbol\',\'field_text\':\'GOOGL\'}"', default="{'filed_name':'stock_symbol','field_text':'GOOGL'}")
    parser.add_argument('-f', '--features', metavar="", type=str, help='Array with the field names to use as features (between quotes and with no spaces). Default: "[\'open\',\'high\',\'low\',\'volume\']"', default="['open','high','low','volume']")
    parser.add_argument('-y', '--y_value', metavar="", type=str, help='y value is the name of field in the dataset that your model will predict. Default: "adj_close"', default="adj_close")
    parser.add_argument('-n', '--n_splits', metavar="", type=int, help='n_splits is the number that you will slices you dataset. Default: 4', default=4)
    parser.add_argument('-hl', '--hidden_layers', metavar="", type=int, help='hidden_layers is the number of internal layers of your model. Default: 4', default=4)
    parser.add_argument('-u', '--units', metavar="", type=int, help='units is the number of neurons of you hidden layers. Default: 10', default=10)
    parser.add_argument('-e', '--epochs', metavar="", type=int, help='epochs is the number of repetitions to train you model. Default: 10', default=10)
    parser.add_argument('-v', '--verbose', metavar="", type=int, help='How much data you need to output. O is only necessary more numbers more output data. Default: 0', default=0, choices = [0, 1, 2, 3, 4, 5])
    args = parser.parse_args()
    lstm_wrapper_values = {
        # Dataset
        "dataset_path" : args.dataset_path,
        # Filtering the dataset with multiple companies stocks
        "filter_stocks" : literal_eval(args.filter_stocks),
        # Number os splits to generate the train and test use by TimeSeriesSplit
        "n_splits" : args.n_splits,
        # Number of hidden layers
        "hidden_layers" : args.hidden_layers,
        # Number of neurons for each layer
        "units" : args.units,
        # Number of epochs
        "epochs" : args.epochs,
        # Verbose 0 = none, 1 more detail, 2 a lot of details and go on til 4
        "verbose" : args.verbose,
        # Selecting the Features (x)
        "features" : literal_eval(args.features),
        # Select predict values (y)
        "y_value" : args.y_value
    }
    return SimpleNamespace(**lstm_wrapper_values)



