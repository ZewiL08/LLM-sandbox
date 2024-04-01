import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_preds_candles(df, train, pred, model_name, savefig = ""):

    save_folder = "./plot/" + savefig
    index = len(train)

    opens = pd.Series(df['open'].values, index=df['date'])
    truth = pd.Series(df['close'].values, index=df['date'])
    highs = pd.Series(df['high'].values, index=df['date'])
    lows = pd.Series(df['low'].values, index=df['date'])

    plt.figure(figsize=(8, 6), dpi=100)

    ## Draw candles
    height = truth - opens
    bottom = np.where(height > 0, opens, truth + abs(height))
    color = np.where(height > 0, 'g', 'r')

    plt.bar(range(len(truth)), height, bottom=bottom, color=color, align='center')
    plt.vlines(range(len(highs)), ymin=lows, ymax=highs, color=color, linewidth=1)      

    lower = np.quantile(pred, 0.05, axis=0)
    upper = np.quantile(pred, 0.95, axis=0)
    plt.fill_between(range(index, index + len(lower)), lower, upper, alpha=0.3, color='purple')

    medians = [sorted(sublist)[len(sublist)//2] if len(sublist) % 2 != 0 else
           (sorted(sublist)[len(sublist)//2 - 1] + sorted(sublist)[len(sublist)//2]) / 2
           for sublist in zip(*pred)]  

    plt.plot(range(index, index + len(pred[0])), medians, label=model_name, color='purple')
    

    # plt.plot(range(index, index + len(pred[0])), pred[0], label=model_name, color='purple')
    plt.grid()
    plt.legend(loc='upper left')

    index_to_display = range(0, len(truth), len(truth) // 3)
    truth.index = truth.index.date
    display_date = truth.index[index_to_display]
    plt.xticks(index_to_display, display_date)

    # plt.xticks(range(len(truth)), truth.index)

    plt.savefig(save_folder)
    plt.show()


def plot_pred_classic(df, train, pred, model_name, savefig = "") :

    save_folder = "./plot/" + savefig
    index = len(train)

    plt.figure(figsize=(8, 6), dpi=100)

    plt.plot(range(len(df['date'])), df['close'], color='black')


    lower = np.quantile(pred, 0.05, axis=0)
    upper = np.quantile(pred, 0.95, axis=0)
    plt.fill_between(range(index, index + len(lower)), lower, upper, alpha=0.3, color='purple')

    medians = [sorted(sublist)[len(sublist)//2] if len(sublist) % 2 != 0 else
        (sorted(sublist)[len(sublist)//2 - 1] + sorted(sublist)[len(sublist)//2]) / 2
        for sublist in zip(*pred)]  

    plt.plot(range(index, index + len(pred[0])), medians, label=model_name, color='purple')


    # plt.plot(range(index, index + len(pred[0])), pred[0], label=model_name, color='purple')
    plt.grid()
    plt.legend(loc='upper left')

    index_to_display = range(0, len(df["date"]), len(df["date"]) // 3)
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.date
    display_date = df["date"][index_to_display]
    plt.xticks(index_to_display, display_date)

    # plt.xticks(range(len(truth)), truth.index)

    plt.savefig(save_folder)
    plt.show()