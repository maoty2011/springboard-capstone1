import psycopg2
import pandas as pd
from time import clock
import configparser

from datetime import datetime

import quandl
from pandas_datareader import data

def str2dt(_str):
    return datetime.strptime(_str,'%Y-%m-%d').date()


class FuData(object):
    def __init__(self, branch_loc='DEFAULT'):
        self.fudata_date = []
        #branch_loc = 'DEFAULT'  # 'DEFAULT' for US
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.db_name = config[branch_loc]['DBName']  # 'ultralpha'
        self.host_name = config[branch_loc]['HostName']
        self.port = config[branch_loc]['Port']
        self.user = config[branch_loc]['Username']
        self.password = config[branch_loc]['Password']
        # self.db_name='ultralpha'
        # self.host_name = 'ultralpha-postgresql-futuredb.cgridhma5omk.us-east-1.rds.amazonaws.com'
        self.col_list = ['date', 'open', 'high', 'low', 'close', 'volume']

        self.conn = None
        self.cur = None

    def get_all_data_of_future(self, contract_code):  # return db data as df
        conn = psycopg2.connect(database=self.db_name, user=self.user, password=self.password,
                                host=self.host_name, port=self.port)
        cur = conn.cursor()

        sql_temp = "select * from fut_day where instrument=" + "\'" + contract_code + "\';"
        cur.execute(sql_temp)
        rows = cur.fetchall()

        conn.commit()
        conn.close()

        dataframe_cols = [tuple[0] for tuple in cur.description]
        df = pd.DataFrame(rows, columns=dataframe_cols)
        return df
        pass

class StkData(object):
    def __init__(self, branch_loc='Stock'):
        self.fudata_date = []
        #branch_loc = 'DEFAULT'  # 'DEFAULT' for US
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.db_name = config[branch_loc]['DBName']  # 'ultralpha'
        self.host_name = config[branch_loc]['HostName']
        self.port = config[branch_loc]['Port']
        self.user = config[branch_loc]['Username']
        self.password = config[branch_loc]['Password']
        # self.db_name='ultralpha'
        # self.host_name = 'ultralpha-postgresql-futuredb.cgridhma5omk.us-east-1.rds.amazonaws.com'
        self.col_list = ['date', 'open', 'high', 'low', 'close', 'volume']

        self.conn = None
        self.cur = None

    def get_all_data(self, contract_code):  # return db data as df
        conn = psycopg2.connect(database=self.db_name, user=self.user, password=self.password,
                                host=self.host_name, port=self.port)
        cur = conn.cursor()

        sql_temp = "select * from hdata_date where instrument=" + "\'" + contract_code + "\';"
        cur.execute(sql_temp)
        rows = cur.fetchall()

        conn.commit()
        conn.close()

        dataframe_cols = [tuple[0] for tuple in cur.description]
        df = pd.DataFrame(rows, columns=dataframe_cols)
        return df
        pass


if __name__ == '__main__':
    reader = FuData()
    df = reader.get_all_data_of_future('SR701')
    df = df[df.date>str2dt('2014-01-01')]
    df = df.sort_values(by='date',ascending=False)
    df = df.set_index('date')
    print(df.shape)
    print(df.head())

    reader2 = StkData()
    chn_sugar_stk_list = ['600191','000833','000911','000576','600737','002387','002286']
    for stk_code in chn_sugar_stk_list:
        df2 = reader2.get_all_data(stk_code)
        df2 = df2[df2.date > str2dt('2014-01-01')]
        df2 = df2.sort_values(by='date', ascending=False)
        df2 = df2.set_index('date')
        #print(df2[df2.isnull().any(axis=1)])
        #input('======')
        df[stk_code] = df2['close']

    print(df.shape)
    print(df.head())
    print(df.info())
    print(df[df.isnull().any(axis=1)])

    input('======')

    quandl.ApiConfig.api_key = 'FCr-76r6uLchvcovFHzi'

    '''
    The Hershey Company (NYSE:HSY), 
    Tootsie Roll Industries, Inc. (NYSE:TR), 
    Rocky Mountain Chocolate Factory, Inc. (NASDAQ:RMCF)
    iPath Dow Jones-UBS Sugar Total Return Sub-Index Exchange Traded Note (NYSEARCA:SGG)
    Cosan Ltd. (NYSE:CZZ)
    
    Baotou Huazi Industry Co., Ltd (SHA: 600191)
    Guangxi Guitang Group 000833 (SHE)
    Nanning Sugar Industry 000911 (SHE)
    Jiangmen Sugarcane Chmcl Fctry Grp CoLtd SHE: 000576
    COFCO Tunhe Sugar Co Ltd SHA: 600737
    Blackcow Food Co., Ltd. SHE: 002387
    Baolingbao Biology Co., Ltd. SHE: 002286
    '''
    #dataf = quandl.get_table('WIKI/PRICES', ticker=['HSY','TR','RMCF'],
    #                        date={'gte': '2016-01-01', 'lte': '2017-01-01'}, )
    #print(dataf.head())
    #print(dataf['ticker'].unique())

    tickers = ['HSY','TR','RMCF','SGG','CZZ']
    data_source = 'yahoo'
    start_date = '2015-07-01'
    end_date = '2017-01-16'
    panel_data = data.DataReader(tickers, data_source, start_date, end_date)
    print(panel_data.keys())
    close_df = panel_data['Adj Close']
    print(close_df.head())

    close_df.index = close_df.index.map(lambda x:x.date())
    print(type(close_df.index[0]),close_df.index[0])
    print(type(df.index[0]))
    print(df.index[0] > close_df.index[0])

    joint_df = df.join(close_df)
    print(joint_df.head())
    #joint_df.to_csv('sugar701.csv')