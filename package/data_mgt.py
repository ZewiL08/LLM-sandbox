import pandas as pd
import darts.datasets


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


def get_data_set_simple(input_length) :
    with open('datasets/IstanbulTraffic.csv', 'rb') as f:
        df = pd.read_csv(f,  parse_dates=[0], names=['date', 'close'])
        df = df.head(input_length + 7)
        print(df)
        df['close'] = df['close'].astype(float)
        series = pd.Series(df['close'].values, index=df['date'])

        f.seek(0)
        df_raw = pd.read_csv(f, parse_dates=[0], names=['date', 'close'])
        df_raw = df_raw.head(input_length + 7)

    train = series.iloc[:input_length]
    test = series.iloc[input_length:]  

    return (df_raw, train, test)


def get_data_darts(input_length) :
    dsname = "AirPassengersDataset"
    darts_ds = getattr(darts.datasets,dsname)().load()
    
    print(darts_ds) 

    df =   darts_ds.pd_dataframe()
    df = df.head(input_length + 7)
    df.columns = ['date', 'close']

    print(df)

    df['close'] = df['close'].astype(float)
    series = pd.Series(df['close'].values, index=df['date'])

    df_raw =   darts_ds.pd_dataframe()
    df_raw = df.head(input_length + 7)
    df_raw.columns = ['date', 'close']

    train = series.iloc[:input_length]
    test = series.iloc[input_length:]  

    series = darts_ds.pd_series()
    series = series.rename(columns={'time': 'date', 'value': 'close'})

    return (df_raw, train, test)

