import pandas as pd
from utils.paths import DATA_CALENDAR, DATA_SALES_EVALUATION, DATA_SALES_VALIDATION, DATA_SELL_PRICES
from fastparquet import *
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Chargement
sales_eval = pd.read_csv(DATA_SALES_VALIDATION)
sales_validation = pd.read_csv(DATA_SALES_VALIDATION)
calendar = pd.read_csv(DATA_CALENDAR)
sell_prices = pd.read_csv(DATA_SELL_PRICES)

# Sélection du magasin et des produits
store = ['CA_1']
product_ids = ['FOODS_1_002'] #, 'FOODS_1_002', 'FOODS_1_003']  

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

def period_and_store_and_product_filter(df, store, product_id, period : int):
    df_filtered = df[
        (df['store_id'] == store[0]) & # ! À corriger si plusieurs magasins sélectionnés ! 
        (df['item_id'].isin(product_ids))
    ]
    # Restriction temporrelle des données données (aux period derniers jours)
    date_cols = [col for col in df_filtered.columns if col.startswith('d_')]
    d_cols_to_keep = date_cols[-period:] # 730 pour le train, 28 pour le test

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
    df_merged['date'] = pd.to_datetime(df_merged['date'])
    # Feature engineering temporel
    df_merged['dayofweek'] = df_merged['date'].dt.dayofweek
    df_merged['is_weekend'] = df_merged['dayofweek'].isin([5, 6]).astype(int)
    df_merged['day'] = df_merged['date'].dt.day
    df_merged['month'] = df_merged['date'].dt.month
    df_merged['year'] = df_merged['date'].dt.year
    df_merged['weekofyear'] = df_merged['date'].dt.isocalendar().week.astype(int)
    df_merged['is_month_start'] = df_merged['date'].dt.is_month_start
    df_merged['is_month_end'] = df_merged['date'].dt.is_month_end

    return df_merged

def encode_categories(df):
    for col in df.select_dtypes(include='object').columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))  # .astype(str) en cas de NaN ou valeurs mixtes
    return df


def prepare_set(df, store, product_id, period : int) : 
    df_long = period_and_store_and_product_filter(df, store, product_id, period)
    df_merged = merge_calendar_and_sell_dataset(df_long)
    df_with_features = add_temporal_features(df_merged)
    df_final = encode_categories(df_with_features)
    return df_final

if __name__ == "__main__" : 

    train_set = prepare_set(sales_eval, store, product_ids, 730)
    train_set.to_parquet("data/train_set.parquet", index=False)

    test_set = prepare_set(sales_validation, store, product_ids, 28)
    test_set.to_parquet("data/test_set.parquet", index = False)





