import pandas as pd
from utils.paths import DATA_CALENDAR, DATA_SALES_EVALUATION, DATA_SALES_VALIDATION, DATA_SELL_PRICES
from fastparquet import *
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Chargement
calendar = pd.read_csv(DATA_CALENDAR)
sell_prices = pd.read_csv(DATA_SELL_PRICES)


def merge_calendar_and_sell_dataset(df_long):
    calendar['wm_yr_wk'] = pd.to_numeric(calendar['wm_yr_wk'], errors='coerce')
    df_long = df_long.merge(calendar, on='d', how='left')

    sell_prices['wm_yr_wk'] = sell_prices['wm_yr_wk'].astype('int')
    df_merged = df_long.merge(
        sell_prices,
        on=['store_id', 'item_id', 'wm_yr_wk'],
        how='left'
    )
    return df_merged

def period_and_store_and_product_filter(df, store, product_id, period : int, is_train : bool = True):
    index_start_date = 1914

    df_filtered = df[
        (df['store_id'] == store) & # ! À corriger si plusieurs magasins sélectionnés ! 
        (df['item_id'] == product_id)
    ]
    date_cols = [col for col in df_filtered.columns if col.startswith('d_')]


    if is_train:
        # Restriction temporrelle des données données (aux period derniers jours)
        d_cols_to_keep = date_cols[-period : index_start_date] # period = 730 pour le train, 
    else:
        d_cols_to_keep = date_cols[index_start_date : index_start_date + period] # period = 28, 1 semaine, 1 mois, 1 an pour le test 

    # Concaténation avec les colonnes d'identification
    static_cols = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
    df_reduced = df_filtered[static_cols + d_cols_to_keep]

    # Melt : passage en long format
    df_long = df_reduced.melt(
        id_vars=static_cols,
        var_name='d',
        value_name='sales'
    )
    return df_long

def add_temporal_features(df_merged):
    import numpy as np

    df_merged['date'] = pd.to_datetime(df_merged['date'])
    df_merged['dayofweek'] = df_merged['date'].dt.dayofweek
    df_merged['is_weekend'] = df_merged['dayofweek'].isin([5, 6]).astype(int)
    df_merged['day'] = df_merged['date'].dt.day
    df_merged['month'] = df_merged['date'].dt.month
    df_merged['year'] = df_merged['date'].dt.year
    df_merged['weekofyear'] = df_merged['date'].dt.isocalendar().week.astype(int)
    df_merged['is_month_start'] = df_merged['date'].dt.is_month_start.astype(int)
    df_merged['is_month_end'] = df_merged['date'].dt.is_month_end.astype(int)

    df_merged = df_merged.sort_values(by=['id', 'date'])

    for lag in [1, 7, 28]:
        df_merged[f'sales_lag_{lag}'] = df_merged.groupby('id')['sales'].shift(lag)

    for window in [7, 28]:
        df_merged[f'sales_roll_mean_{window}'] = df_merged.groupby('id')['sales'].shift(1).rolling(window=window).mean()
        df_merged[f'sales_roll_std_{window}'] = df_merged.groupby('id')['sales'].shift(1).rolling(window=window).std()

    df_merged.fillna(-1, inplace=True)

    return df_merged


def encode_categories(df):
    for col in df.select_dtypes(include='object').columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))  # .astype(str) en cas de NaN ou valeurs mixtes
    return df


def prepare_set(df, store, product_id, period : int, is_train : bool = True) : 
    df_long = period_and_store_and_product_filter(df, store, product_id, period, is_train=is_train)
    df_merged = merge_calendar_and_sell_dataset(df_long)
    df_with_features = add_temporal_features(df_merged)
    df_final = encode_categories(df_with_features)
    return df_final

if __name__ == "__main__" : 
    sales_eval = pd.read_csv(DATA_SALES_EVALUATION)
    sales_validation = pd.read_csv(DATA_SALES_VALIDATION)
    store = 'CA_1'
    product_id = 'FOOD_1_001'
    train_set = prepare_set(sales_eval, store, product_id, 730, is_train=True)
    test_set = prepare_set(sales_validation, store, product_id, 28, is_train=False)




