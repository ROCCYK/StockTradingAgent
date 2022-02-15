import datetime
import random
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class Agent:
    def __init__(self, env, cash=100):
        self.env = env
        self.cash = cash
        self.spent = [[],[]]
        self.price = env.df

    def moving_average(self, prices, rate=5):
        return prices.rolling(rate).mean()

    def run(self):
        df = self.price
        df['5 Period Moving Average'] = self.moving_average(df['Prices'])
        df['3 Period Moving Average'] = self.moving_average(df['Prices'],rate=3)
        flag = 0
        self.buy = []
        self.sell = []
        for i in range(len(df)):
            if df['3 Period Moving Average'][i] <= df['5 Period Moving Average'][i]:
                if flag != 1:
                    flag = 1
                    self.buy.append(df['Prices'][i])
                    self.sell.append(np.nan)
                    self.spent[0].append(df['Prices'][i])
                else:
                    self.sell.append(np.nan)
                    self.buy.append(np.nan)
            elif df['3 Period Moving Average'][i] >= df['5 Period Moving Average'][i]:
                if flag != -1:
                    flag = -1
                    self.sell.append(df['Prices'][i])
                    self.buy.append(np.nan)
                    self.spent[1].append(df['Prices'][i])
                else:
                    self.sell.append(np.nan)
                    self.buy.append(np.nan)
            else:
                self.sell.append(np.nan)
                self.buy.append(np.nan)
        df['buy signal price'] = self.buy
        df['sell signal price'] = self.sell
        self.df = df
        pnl = [0]
        for i in range(len(self.spent[0])):
            pnl.append(self.spent[1][i] - self.spent[0][i])
        self.pnl = pnl
        balance = [self.cash]
        tradeno = []
        for i, v in enumerate(pnl):
            print(i,v)
            tradeno.append(i)
            balance.append(balance[-1] + v)
        balance.pop(0)
        self.tradeno = tradeno
        self.balance = balance
        print(balance)
        print(pnl)
        print(df)
        print(f'your profit/loss is: ${sum(pnl)}')
        print(f'your new total balance is: ${self.cash + sum(pnl)}')

class Environment:
    def __init__(self):
        self.price = {date.today():random.randint(1,10)}
        while True:
            price_today = int(input('Enter the price for today: '))
            self.price[list(self.price)[-1] + datetime.timedelta(days=1)] = price_today
            print('enter a value less than or equal to 0 when finished entering prices')
            if price_today <= 0:
                self.price.popitem()
                self.df = pd.DataFrame()
                self.df['Date'] = self.price.keys()
                self.df['Prices'] = self.price.values()
                break

    def price(self):
        return self.price()

class Plot:
    def __init__(self, ag, env):
        self.ag = ag
        self.env = env
        plt.xlabel('date')
        plt.ylabel('price')

    def plotagent(self):
        date = self.env.df['Date']
        price = self.env.df['Prices']
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.plot(date, price, label='price')
        plt.plot(date, self.ag.df['5 Period Moving Average'], label='5 Period Moving Average')
        plt.plot(date, self.ag.df['3 Period Moving Average'], label='3 Period Moving Average')
        plt.scatter(date, self.ag.df['buy signal price'], label='buy', marker='^', color='green')
        plt.scatter(date, self.ag.df['sell signal price'], label='sell', marker='v', color='red')
        plt.legend(loc='best')
        plt.title('Stock Trading Agent')
        plt.show()
    def plotpnl(self):
        tradeno = self.ag.tradeno
        pnl = self.ag.pnl
        balance = self.ag.balance
        plt.xlabel('Trade Number')
        plt.ylabel('Amount in $')
        plt.plot(tradeno,pnl, label='Profit & Loss')
        plt.plot(tradeno, balance, label='Account balance')
        plt.legend(loc='best')
        plt.title('Agent Balance and P&L')
        plt.show()
    def run(self):
        self.plotagent()
        self.plotpnl()





if __name__ == '__main__':
    test = Environment()
    testai = Agent(test)
    testai.run()
    plot = Plot(testai,test)
    plot.run()

