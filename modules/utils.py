import pandas as pd



def dataset_summary(df):
    return {
        'rows': df.shape[0],
        'columns': df.shape[1],
        'missing_values': int(df.isnull().sum().sum())
    }
