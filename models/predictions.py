# models/predictions.py

import pandas as pd
import lightgbm as lgb
from models.build_dataset import prepare_set
from utils.paths import DATA_SALES_VALIDATION, DATA_SALES_EVALUATION
from sklearn.ensemble import RandomForestRegressor
import numpy as np

def load_data(user_inputs : dict, period=730):
    df_train = pd.read_csv(DATA_SALES_VALIDATION)
    df_test = pd.read_csv(DATA_SALES_EVALUATION) # Étendre le fichier source si on veut des prédictions de plus de 28 jours 
    store = user_inputs['store_id']
    product = user_inputs['item_id'] # if isinstance(user_inputs['item_id'], list) else [user_inputs['item_id']]
    duration = user_inputs['period']
    print(product, store)
    X_train = prepare_set(df_train, store, product, period)
    X_test = prepare_set(df_test, store, product, duration, is_train=False)

    y_train = X_train['sales']
    y_real = X_test['sales']

    X_train.drop(columns=['sales'], inplace=True)
    X_test.drop(columns=['sales'], inplace=True)

    X_train.drop('date', axis=1, inplace=True)
    X_test.drop('date', axis=1, inplace=True)

    return X_train, y_train, X_test, y_real


def train_model_lgbm(X_train, y_train):
    model = lgb.LGBMRegressor(verbose=-1)
    model.fit(X_train, y_train)
    return model

def train_model_rf(X_train, y_train):
    model = RandomForestRegressor(verbose=0)
    model.fit(X_train, y_train)
    return model

def predict_sales(user_inputs : dict):
    X_train, y_train, X_test, y_real = load_data(user_inputs, period = 730)
    model = train_model_rf(X_train, y_train)
    predictions = model.predict(X_test)
    y_pred_rounded = np.round(predictions)
    return X_test, y_pred_rounded, y_real

