from dotenv import load_dotenv
import os
from utils.db_utils import *
from utils.calc_utils import *
from utils.avan_utils import *
import pandas as pd
from config import *
from utils.strat_utils import *
import json 
from backtesting import Backtest, Strategy
from backtesting.lib import cross



class SpreadZscore(Strategy):
    def init(self):
        price = self.data.Close
        self.rolling_mean = self.I(lambda x: pd.Series(x).rolling(window=20).mean(), price)
        self.rolling_std = self.I(lambda x: pd.Series(x).rolling(window=20).std(), price)
        self.zscore = (self.data.Close - self.rolling_mean) / self.rolling_std
        
    def next(self):
        if cross(self.data.Close, self.rolling_mean+self.rolling_std):
            self.sell(size=0.2)
        elif cross(self.data.Close, self.rolling_mean-self.rolling_std):
            self.buy(size=0.2)
        
        for trade in self.trades:
            if cross(self.data.Close, self.rolling_mean):
                trade.close()
 
df_test = pd.read_csv(DATA_FOLDER+'/test_filtered.csv')
results = pd.DataFrame()
for column in df_test.columns[1:]:
    df = pd.DataFrame()
    df['Close'] = df_test[column] + 100
    df['Open'] = df['High'] = df['Low'] = df['Close']
    bt = Backtest(df, SpreadZscore, cash=10000)
    stats = bt.run()
    results = pd.concat([results,pd.Series(stats)], axis=1)
    print(f'{column}')
    print(stats)

results.to_csv(DATA_FOLDER+'/testtest.csv')