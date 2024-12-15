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
