# Exploratory Data Analysis

import quandl
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

import matplotlib.pyplot as plt

from collections import defaultdict

quandl.ApiConfig.api_key = 'FCr-76r6uLchvcovFHzi'

related_stock_list = ['CZZ','HSY','RMCF','SGG','TR']

sugar_df = pd.read_csv('sugar701.csv')
print(sugar_df.info())

#print(sugar_df[sugar_df.isnull().any(axis=1)])
# we see that all NaN's come from US holidays that are not China holidays
# also note that there is time difference

sugar_df = sugar_df.dropna(how='any')
# plot something
df_for_plot = sugar_df[['date','close','CZZ']].sort_values(by='date',ascending=True)
df_for_plot['close'] = (df_for_plot['close'] - df_for_plot['close'].mean())/df_for_plot['close'].std()
df_for_plot['CZZ'] = (df_for_plot['CZZ'] - df_for_plot['CZZ'].mean())/df_for_plot['CZZ'].std()
_ = df_for_plot.plot(x='date',y=['close','CZZ'],kind='line')
_ = df_for_plot.plot(x='close',y='CZZ',kind='scatter')
plt.show()

# examine potential correlations b/w time series

# 1. calculate shifted return of target instrument:
# return if buy on the next day and hold d days
test_range = 20
for hold_day in range(1,test_range+1):
    col_name = 'ret_{0}'.format(hold_day)
    sugar_df[col_name] = np.log(sugar_df['close'].shift(hold_day+1)/sugar_df['close'].shift(1))
    # also save shift price
    sugar_df['close_{0}'.format(hold_day)] = sugar_df['close'].shift(hold_day)

# also add first different/link relatives
sugar_df['close_diff'] = sugar_df['close'] - sugar_df['close'].shift(-1)
for stock in related_stock_list:
    sugar_df[stock+'_diff'] = sugar_df[stock] - sugar_df[stock].shift(-1)

print(sugar_df[['date','ret_1','ret_3','close_1','close_diff','CZZ_diff']].head())
# plot something
df_for_plot = sugar_df[['date','close_diff','CZZ_diff']].sort_values(by='date',ascending=True)
df_for_plot = df_for_plot.dropna(how='any')
df_for_plot['close'] = (df_for_plot['close_diff'] - df_for_plot['close_diff'].mean())/df_for_plot['close_diff'].std()
df_for_plot['CZZ'] = (df_for_plot['CZZ_diff'] - df_for_plot['CZZ_diff'].mean())/df_for_plot['CZZ_diff'].std()
#_ = df_for_plot.plot(x='date',y=['close','CZZ'],kind='line')
_ = df_for_plot.plot(x='CZZ',y='close',kind='scatter')
plt.show()
print('Corr:',pearsonr(df_for_plot['CZZ'],df_for_plot['close']))

# 2. check correlation coeffs
corr_record = {}
for stock in related_stock_list:
    corr_record[stock] = [np.empty(2) for x in range(test_range+1)]
for hold_day in range(1,test_range+1):
    col_name = 'close_{0}'.format(hold_day)
    for stock in related_stock_list:
        se = sugar_df[[col_name,stock]].dropna(how='any')
        #se[stock] = se[stock]/se[stock].shift(-1)-1
        #print(se.tail())
        #se = se.dropna(how='any')
        #_ = se.plot(stock,col_name,kind='scatter')
        #_ = se.hist(column=col_name)
        #_ = se.hist(column=stock)
        #plt.show()
        #input('===')
        '''
        cov = np.array(se.corr())
        ans = cov[0][1]
        '''
        ans = pearsonr(se[stock],se[col_name])
        corr_record[stock][hold_day] = ans

for key in corr_record.keys():
    print(key,np.argmax(corr_record[key]))
    print(corr_record[key])

'''
for delay_days in range(20):
    se2[keyword+'_delay'] = se2[keyword].shift(delay_days)

    df = pd.merge(se1,se2[['date',keyword+'_delay']],on='date').dropna()

    #print(df.head())

    rel = pearsonr(df['return'],df[keyword+'_delay'])
    print(delay_days,rel)
'''