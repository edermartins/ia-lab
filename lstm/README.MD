# Wrapper LSTM (Long Short-Term Memory)

This is a simple wrapper to make easy to use LSTM for study or real use in a real world

# Requiments

## Python

- Python 3.11 + pip

## Miniconda
Before any installation I had installed Miniconda to use the Venv: https://docs.anaconda.com/miniconda/miniconda-install/

After that I create a virtual env and installed everything inside this `venv`: `conda create --name tf-wsl python=3.11`

Activate this virtual env and install all you needs: `conda activate tf-wsl`

## Main Libraries

- Keras 3.5.0: `pip install keras`
- SKLearn: `pip install sklearn`
- Pandas: `pip install pandas`
- Numpy: `pip install numpy`
- More libraries: `pip install matplotlib seaborn pandas_datareader jupyter jupyterlab`

## NVIDIA CUDA

I recommend to use NVIDIA CUDA, otherwise will take a lot of time to train in a normal AMD or Intel CPU: https://developer.nvidia.com/cuda-downloads

# How to use

## Running the `lstm.py` file

Just run the `lstm.py` file using you local python

`python lstm.py`

If you a `conda` virtual environment:

`conda run -n <your virtual environment> --no-capture-output python ./lstm.py `

or activate the `venv` and run the `lstm.py` file (in my case, the virtual environment is tf-wsl):
```bash
# conda activate tf-wsl
(tf-wsl) # python lstm.py
```


## Use the wrapper inside you application

```python
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
```

### Command line option

If you not pass any arguments, default values will seted:

```text
usage: lstm.py [-h] [-d] [-fs] [-f] [-y] [-n] [-hl] [-u] [-e] [-v]

options:
  -h, --help            show this help message and exit
  -d , --dataset_path   path to dataset. Default: 'data/big_tech_stock_prices.csv'
  -fs , --filter_stocks Column name and value to be filtered (between quotes and with no spaces). 
                        Default: "{'filed_name':'stock_symbol','field_text':'GOOGL'}"
                        
  -f , --features       Array with the field names to use as features (between quotes and with no spaces).
                        Default: "['open','high','low','volume']"

  -y , --y_value        y value is the name of field in the dataset that your model will predict.
                        Default: "adj_close"

  -n , --n_splits       n_splits is the number that you will slices you dataset.
                        Default: 4

  -hl , --hidden_layers hidden_layers is the number of internal layers of your model.
                        Default: 4

  -u , --units          units is the number of neurons of you hidden layers. 
                        Default: 10

  -e , --epochs         epochs is the number of repetitions to train you model. 
                        Default: 10

  -v , --verbose        How much data you need to output. O is only necessary more numbers more output data.
                        Default: 0
```


## Start API services: `lstm-sercice.py`

This service was made with Flask. So you need to install it: `pip install flask`
Just run the script. It will be waiting for API REST calls:
` python lstm-sercice.py`

Or use Conda command:

`conda run -n tf-wsl --no-capture-output python -m flask run`

### Endpoints available

#### POST model 
Create the model using the body params.

Request:
```json
{
    "filter_stocks": {"filed_name": "stock_symbol", "field_text":"GOOGL"},
    "features": ["open", "high", "low", "volume"],
    "y_value": "adj_close", 
    "n_splits":20, 
    "hidden_layers":4, 
    "units":100
}
```
Responses:

- 201
```json
{
    "message": "Model LSTM created with success"
}
```
- Otherwise, is an error

#### POST model/fit 
Train the model created in `POST /model`. As the training can get a lot of time, this endpoint is async. If you get code 201, you need to try `/model/evaluate` till it gets success. 

Request:
```json
{
    "epochs": 10
}
```
Responses:
- 201 This is a Async call (if you try again will get an error)
```json
{
    "message": "Model LSTM training in progress"
}
```
- 402
```json
{
    "message": "message"
}
```
Messages:
- `Model wasn't created`
- `Model still training in progress`

#### POST model/evaluate 
This function evaluate your model when ready as the endpoint `/model/fit` is asynx. After training the model and calling `/model/fit`, you need to try this method till you get success.

Request:
```json
{
    "verbose": 0
}
```

Responses:
- 201
```json
{
    "test_score": {
        "mse": 4157.3818359375,
        "rmse": 64.47776233661882
    },
    "train_score": {
        "mse": 1187.6351318359375,
        "rmse": 34.46208252320132
    }
}
```
- 422
```json
{
    "message": "Model wasn't trained"
}
```
