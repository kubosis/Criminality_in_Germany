import pandas as pd
import numpy as np

def new_column_from_cols_and_specif(col, specifier):
    col = ''.join(list(map(lambda x: str(x).strip("\n").strip("<NA>"), col)))
    new_col = f"{str(specifier).strip("\n")}: {col}"
    new_col = new_col.replace("nan", "").replace("\\n", "")
    return new_col


def create_new_cols(specifier_column, other_columns):
    return [new_column_from_cols_and_specif(col, specifier)
                for specifier in specifier_column
                for col in other_columns
            ]

def create_transformed_df(df, specifier_column, other_columns, year):
    new_columns = create_new_cols(specifier_column, other_columns)

    # Flatten the values of all columns except the specifier column
    new_values = df.loc[:, other_columns].to_numpy().flatten()
    filtered_values = new_values[np.array([np.issubdtype(type(x), np.floating) for x in new_values])]

    df_transformed = pd.DataFrame([new_values], columns=new_columns)
    df_transformed.insert(0, "year", [year])

    return df_transformed

def transform_one_df(df, specifier_key, interesting_values_basic_table, year):
    df = df[df[specifier_key].isin(interesting_values_basic_table)]

    specifier_column = df[specifier_key].to_numpy().flatten()
    other_columns = df.columns[df.columns != specifier_key]

    return create_transformed_df(df, specifier_column, other_columns, year)

#Lags the selected predictor by the lag amount
#Positive lag amount is the value of the predictor that many months/years ago
#Negative lag is the value of the predictor in the future
#Both will create NaN rows, at either the top or bottom of the df, use drop_nan_rows=True to drop all of those rows
#Use the option drop_original=True to also drop the pred_to_lag predictor passed to the function
#The pos=<int> is the position of where to insert the new lagged predictor, default is at the right end of the df
def create_lagged_predictor(df, pred_to_lag, lag_amount, **kwargs):
    #=kwargs.get("on", None)
    new_col_name = str(lag_amount)+ "-Lagged: " + pred_to_lag
    if kwargs.get("pos", None) is None:
        df.insert(len(df.columns),new_col_name, df[pred_to_lag].shift(lag_amount))
    else:
        df.insert(kwargs.get("pos", None),new_col_name, df[pred_to_lag].shift(lag_amount))
    if kwargs.get("drop_original", None) is not None:
        if kwargs.get("drop_original", None):
            df.drop([pred_to_lag], axis=1, inplace=True)
    if kwargs.get("drop_nan_rows", None) is not None:
        if kwargs.get("drop_nan_rows", None):
            if lag_amount > 0:
                df = df.iloc[lag_amount:,:]
            else:
                df = df.iloc[:lag_amount,:]
    return df

#Example usage:
#create_lagged_predictor(df, "Date", 2, pos=0, drop_original=True)
