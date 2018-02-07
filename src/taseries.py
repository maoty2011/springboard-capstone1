import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr

import matplotlib.pyplot as plt

import talib
# note that talib requires that the time series index to be in increasing order

# calculate some technical time series from a price-volume dataframe

class TAcalc(object):
    def __init__(self):
        self.datetime_index = None
        self.data_dict = {} # numpy array-lized data

    def load_data(self,path):
        _data = pd.read_csv(path,index_col='date',parse_dates=['date'])
        self.datetime_index = _data.index
        # numpy array-lize the time series data
        for col_name in ['open','high','low','close','volume']:
            self.data_dict[col_name] = np.array(_data[col_name]).astype(float)

    def generate_indicator(self,name):
        if name == 'BBANDS_upper':
            se = talib.BBANDS(self.data_dict['close'])[0]
        elif name == 'BBANDS_middle':
            se = talib.BBANDS(self.data_dict['close'])[1]
        elif name == 'BBANDS_lower':
            se = talib.BBANDS(self.data_dict['close'])[2]
        elif name == 'MA':
            se = talib.MA(self.data_dict['close'], timeperiod=30)
        elif name=='EMA':
            se = talib.EMA(self.data_dict['close'], timeperiod=30)
        elif name=='SMA':
            se = talib.SMA(self.data_dict['close'], timeperiod=30)
        elif name == 'WMA':
            se = talib.WMA(self.data_dict['close'], timeperiod=30)

        if name == 'APO':
            se = talib.APO(self.data_dict['close'])
        elif name == 'MACD':
            se = talib.MACD(self.data_dict['close'])[0]
        elif name == 'MOM':
            se = talib.MOM(self.data_dict['close'])
        elif name == 'PPO':
            se = talib.PPO(self.data_dict['close'])
        elif name == 'RSI':
            se = talib.RSI(self.data_dict['close'])
        elif name == 'WILLR':
            se = talib.WILLR(self.data_dict['high'],self.data_dict['low'],self.data_dict['close'])

        if name == 'OBV':
            se = talib.OBV(self.data_dict['close'],self.data_dict['volume'])

        if name == 'ATR':
            se = talib.ATR(self.data_dict['high'], self.data_dict['low'], self.data_dict['close'], timeperiod=14)

        ans = pd.Series(se,index=self.datetime_index)
        ans.name = name
        return ans

# a class that explores the relation between two time series
class SeriesExplorer(object):
    def __init__(self,target):
        # import data:
        # target is the target variable (like return, volatility, etc.)
        # indep_vars is a pd.DataFrame with multiple time series as independent variables
        self.target = target.sort_index() # so that the time series is in chronicle order
        self.indep = {}
        self.data = pd.DataFrame(self.target)

    def add_indep_vars(self,se_list):
        for se in se_list:
            self.indep[se.name] = se

    def sync_index(self):
        # sync the datetime index so that the series share the same index
        # store it to self.data DataFrame
        for key in self.indep.keys():
            self.data[key] = self.indep[key]

    def fill_na(self,method='last'):
        # fill NaN's after the index sync step
        # note that the index is in increasing order
        if method == 'last':
            self.data.fillna(method='ffill',inplace=True)

    def best_shift_test(self,key,method='pearson',test_range=20,plot=False):
        # test which shift series of key column has best correlation with the target variable
        _indep = self.data[key]
        _tar = self.data[self.target.name]
        _corr_list = []
        for d in range(test_range):
            _se = _indep.shift(d)
            nas = np.logical_or(_se.isnull(), _tar.isnull())
            if method == 'pearson':
                ans = pearsonr(_tar[~nas],_se[~nas])[0]
            elif method == 'spearman':
                ans = spearmanr(_tar[~nas],_se[~nas])[0]
            _corr_list.append(ans)

        # if plot=True, plot the corr. vs diff scatter
        if plot:
            _ = plt.plot(_corr_list)
            maxarg = np.argmax(abs(np.array(_corr_list)))
            plt.title('{2} max={0} at d={1}'.format(_corr_list[maxarg],maxarg,key))
            plt.show()

        return _corr_list


def shift_series(se,diff):
    # shift a time series diff days towards future direction
    ans = se.shift(diff)
    ans.name = '{0}_{1}'.format(se.name,diff)
    return ans


if __name__=='__main__':
    # read sugar future SR701 data and generate return series
    df = pd.read_csv('../data/SR701.csv',index_col='date',parse_dates=['date'])
    hold_day = 20
    # note that SR701 data is reverse chronically ordered
    df['rtn'] = np.log(df['close'].shift(hold_day + 1) / df['close'].shift(1))
    rtn_series = df['rtn'].dropna()
    rtn_series.name = 'rtn'
    print(rtn_series)
    close_series = df['close'].shift(1).dropna()
    close_series.name = 'close'
    series_exp = SeriesExplorer(rtn_series)
    #series_exp = SeriesExplorer(close_series)

    # make potential independent variable series
    ta_name_list = ['BBANDS_upper','BBANDS_middle','BBANDS_lower','MA','EMA','SMA','WMA','APO','MACD','MOM','PPO','RSI','WILLR','OBV','ATR']
    ta = TAcalc()
    ta.load_data('../data/CZZ.csv')

    ta_se_list = []
    for ta_name in ta_name_list:
        se = ta.generate_indicator(ta_name)
        ta_se_list.append(se)
        #print(se)

    series_exp.add_indep_vars(ta_se_list)
    series_exp.sync_index()
    series_exp.fill_na()
    #print(series_exp.indep[se.name])
    #print(series_exp.data.head())

    for ta_name in ta_name_list:
        series_exp.best_shift_test(key=ta_name,method='spearman',plot=True)