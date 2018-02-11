import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pprint
import statsmodels.tsa.stattools as ts
import statsmodels.formula.api as sm

def plot_series(df, timestamp, ts1, ts2, normalize=True):
    _df = df[[timestamp, ts1, ts2]].sort_values(by=timestamp, ascending=True)
    _df = _df.dropna(how='any')
    if normalize:
        for x in [ts1,ts2]:
            _df[x] = (_df[x] - _df[x].mean())/_df[x].std()

    _ = _df.plot(x=timestamp, y=[ts1,ts2], kind='line')

    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('{0} and {1} Daily Prices'.format(ts1, ts2))
    plt.legend()
    plt.show()

def plot_scatter_series(df, ts1, ts2):
    plt.xlabel('{0} Price'.format(ts1))
    plt.ylabel('{0} Price'.format(ts2))
    plt.title('{0} and {1} Price Scatterplot'.format(ts1, ts2))
    plt.scatter(df[ts1], df[ts2])
    plt.show()

def plot_residuals(df):
    plt.title('Residual Plot')
    plt.legend()

    plt.plot(df["res"])
    plt.show()

if __name__ == '__main__':
    sugar_df = pd.read_csv('sugar701.csv')
    #sugar_df = sugar_df.dropna(how='any')

    chn_sugar_stk_list = ['600191', '000833', '000911', '000576', '600737', '002387', '002286']
    us_sugar_stk_list = ['HSY', 'TR', 'RMCF', 'SGG', 'CZZ']

    target_var= chn_sugar_stk_list[6]

    plot_series(sugar_df,'date','close',target_var)
    plot_scatter_series(sugar_df,'close',target_var)

    result = sm.ols(formula="close ~ {0}".format(target_var), data=sugar_df).fit()

    print(result.params)
    e = result.params['Intercept']
    b = result.params[target_var]

    sugar_df['res'] = sugar_df['close'] - b*sugar_df[target_var] - e
    plot_residuals(sugar_df)

    cadf = ts.adfuller(sugar_df['res'])
    pprint.pprint(cadf)