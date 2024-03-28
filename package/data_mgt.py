import pandas as pd


def get_data_set(name, input_length, start_date, end_date) :
    with open(name) as f:
        df = pd.read_csv(f, usecols=[0, 4], parse_dates=[0])
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        df = df.loc[mask]
        df['close'] = df['close'].astype(float)
        series = pd.Series(df['close'].values, index=df['date'])

        f.seek(0)
        df_raw = pd.read_csv(f, parse_dates=[0])
        df_raw = df_raw.loc[mask]

        splitpoint = input_length
        train = series.iloc[:splitpoint]
        test = series.iloc[splitpoint:]

    return (df_raw, train, test)

def get_data_set_return(name, input_length, start_date, end_date) :
    with open(name) as f:
        df = pd.read_csv(f, usecols=[0, 1, 4], parse_dates=[0])
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        df = df.loc[mask]
        df['close'] = df['close'].astype(float)
        df['open'] = df['open'].astype(float)
        df['return'] = ((df['close'] / df['open']) - 1) * 10000
        df = df[['date', 'return']]

        series = pd.Series(df['return'].values, index=df['date'])

        splitpoint = input_length
        train = series.iloc[:splitpoint]
        test = series.iloc[splitpoint:]

        f.seek(0)
        df_raw = pd.read_csv(f, parse_dates=[0])
        df_raw = df_raw.loc[mask]
        df_raw['close'] = df_raw['close'].astype(float)
        df_raw['open'] = df_raw['open'].astype(float)
        df_raw['return'] = ((df_raw['close'] / df_raw['open']) - 1) * 10000
        
    return (df_raw, train, test)
