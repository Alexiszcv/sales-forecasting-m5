# models/predictions.py

import pandas as pd
import lightgbm as lgb
from models.build_dataset import prepare_set
from utils.paths import DATA_SALES_VALIDATION, DATA_SALES_EVALUATION

def load_data(user_inputs : dict, period=730):
    df_train = pd.read_csv(DATA_SALES_VALIDATION)
    df_test = pd.read_csv(DATA_SALES_EVALUATION) # Étendre le fichier source si on veut des prédictions de plus de 28 jours 
    store = [user_inputs['store_id']]
    product = user_inputs['item_id'] # if isinstance(user_inputs['item_id'], list) else [user_inputs['item_id']]
    duration = user_inputs['period']
    X_train = prepare_set(df_train, store, product, period)
    X_test = prepare_set(df_test, store, product, duration)

    y_train = X_train['sales']
    X_train.drop(y_train)
    X_train.drop('date', axis=1, inplace=True)
    X_test.drop('date', axis=1, inplace=True)

    return X_train, y_train, X_test


def train_model(X_train, y_train):
    model = lgb.LGBMRegressor(verbose=-1)
    model.fit(X_train, y_train)
    return model

def predict_sales(user_inputs : dict):
    X_train, y_train, X_test = load_data(user_inputs, period = 730)
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    return X_test, predictions

