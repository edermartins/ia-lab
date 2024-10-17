import math
import threading
from flask import Flask, jsonify, request
from LstmWrapper import LstmWrapper

status = ''

# Creating the wrapper
lstm_wrapper = LstmWrapper()

app = Flask(__name__)

@app.post('/model')
def create_model():
    global status
    # Obtém os dados JSON da requisição
    data = request.get_json()
    # Processa os dados (exemplo: imprime na tela)
    print(data)

    #  Setting the variables
    # Dataset
    dataset_path = 'data/big_tech_stock_prices.csv'
    # Filtering the dataset with multiple companies stocks
    filter_stocks = data["filter_stocks"]
    # Number os splits to generate the train and test use by TimeSeriesSplit
    n_splits = data["n_splits"]
    # Number of hidden layers
    hidden_layers = data["hidden_layers"]
    # Number of neurons for each layer
    units = data["units"]
    # Selecting the Features (x)
    features = data["features"]
    # Select predict values (y)
    y_value = data["y_value"]

    '''
    Starting code
    '''

    # Creating and setting the LSTM model
    lstm_wrapper.create_setting_model(dataset_path=dataset_path, filter_stocks=filter_stocks, features=features, y_value=y_value, n_splits=n_splits, hidden_layers=hidden_layers, units=units)
    status = 'model_created'
    # Retorna uma resposta JSON confirmando o recebimento
    return jsonify({"message": "Model LSTM created with success"}), 201

@app.post('/model/fit')
def post_fit_model():
    global status
    code = 201
    if status == 'model_created' or status == 'model_trained':
        status = 'model_training_in_progress'
        # Obtém os dados JSON da requisição
        data = request.get_json()

        thread_fit_model = threading.Thread(target=fit_model, args=(data,))
        thread_fit_model.start()
        message = 'Model LSTM training in progress'
    elif status == 'model_training_in_progress':
        message = "Model still training in progress"
        code = 422
    else:
        message = "Model wasn't created"
        code = 422

    # Retorna uma resposta JSON confirmando o recebimento
    return jsonify({"message": message}), code

def fit_model(data):
    global status
    # Number of epochs
    epochs = data["epochs"]
    # Training the model
    try:
        lstm_wrapper.fit(epochs=epochs)
        status = 'model_trained'
    except Exception as e:
        status = 'None'
        print(e)





@app.post('/model/evaluate')
def post_evaluate_model():
    global status
    code = 201
    if status == 'model_trained':
        # Obtém os dados JSON da requisição
        data = request.get_json()

        # Verbose 0 = none, 1 more detail, 2 a lot of details and go on til 4
        verbose = data["verbose"]

        # Evaluating the model
        score = lstm_wrapper.evaluate(verbose=verbose)
        train_score = score['train']
        test_score = score['test']
        message = {
            "train_score": {"mse": train_score, "rmse": math.sqrt(train_score)},
            "test_score": {"mse": test_score, "rmse": math.sqrt(test_score)}
        }
    else:
        message = {"message": "Model wasn't trained"}
        code = 422

    # Retorna uma resposta JSON confirmando o recebimento
    return jsonify(message), code

if __name__ == '__main__':
    app.run(debug=True)

