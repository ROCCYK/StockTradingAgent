import datetime
import random
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class Agent:
    def __init__(self, env, cash=100): # constructor that takes in the environment and how much
        self.env = env                 # cash the agents starts with.
        self.cash = cash
        self.spent = [[],[]] # initializes self.spent as nested lists for buys and sells.
        self.price = env.df # initializes self.price as the environment's prices dataframe.

    def moving_average(self, prices, rate=5): # function to calculate the moving average given
        return prices.rolling(rate).mean()    # price and the moving average period/rate.

    def run(self): # the run function used to run the agent class.
        df = self.price # stores the dataframe as df
        df['5 Period Moving Average'] = self.moving_average(df['Prices']) # creates new column in dataframe
        df['3 Period Moving Average'] = self.moving_average(df['Prices'],rate=3) # for moving averages.
        flag = 0 # flags so that the agent can only buy or sell 1 at a time.
        self.buy = [] # list to store all the prices the agent buys at.
        self.sell = [] # list to store all the prices the agent sells at.
        for i in range(len(df)): # the condition for when the agent buys or sells.
            if df['3 Period Moving Average'][i] <= df['5 Period Moving Average'][i]:
                if flag != 1:
                    flag = 1 # sets flag to 1 so that agent cant buy stock more than once.
                    self.buy.append(df['Prices'][i]) # appends the price bought to buy list.
                    self.sell.append(np.nan) # appends numpy nan value to sell list.
                    self.spent[0].append(df['Prices'][i]) # appends the price bought to buy spent list.
                else:
                    self.sell.append(np.nan) # when no buy condition has been met it will append
                    self.buy.append(np.nan) # a numpy nan value to both buy/sell list.
            elif df['3 Period Moving Average'][i] >= df['5 Period Moving Average'][i]:
                if flag != -1:
                    flag = -1 # sets flag to -1 so that agent cant sell stock more than once.
                    self.sell.append(df['Prices'][i]) # appends the price sold to sell list.
                    self.buy.append(np.nan) # appends numpy nan value to buy list.
                    self.spent[1].append(df['Prices'][i]) # appends the price sold to sell spent list.
                else:
                    self.sell.append(np.nan) # when no sell condition has been met it will append
                    self.buy.append(np.nan) # a numpy nan value to both buy/sell list.
            else:
                self.sell.append(np.nan) # when no buy or sell condition has been met it will append
                self.buy.append(np.nan) # a numpy nan value to both buy/sell list.
        df['buy signal price'] = self.buy # sets buy signal price column as the buy list.
        df['sell signal price'] = self.sell # sets sell signal price column as the sell list.
        self.df = df # initializes self.df as the complete dataframe with all the added columns.
        pnl = [0] # assigns pnl as a list with a value of 0.
        for i in range(len(self.spent[0])): # subtracts price sold at from price bought and
            pnl.append(self.spent[1][i] - self.spent[0][i]) # appends value into pnl list.
        self.pnl = pnl # initializes self.pnl as the pnl list.
        balance = [self.cash] # creates a list with initial cash balance inside the list.
        tradeno = [] # creates an empty list for trade number.
        for i, v in enumerate(pnl): # appends trade number and what the balance of the agent
            tradeno.append(i) # is to the trade number list and balance list.
            balance.append(balance[-1] + v) # the balance is its previous value + the profit and loss.
        balance.pop(0) # deletes the first index of the balance list to delete repeat of 1st and 2nd index.
        self.tradeno = tradeno # initializes self.tradeno as the trade number list.
        self.balance = balance # initializes self.balance as the balance list.
        print(f'your profit/loss is: ${sum(pnl)}')
        print(f'your new total balance is: ${self.cash + sum(pnl)}')

class Environment:
    def __init__(self):
        self.price = {date.today():random.randint(1,10)} # sets a random price for the first day.
        while True: # takes in price from the user input until user inputs a value less than
            price_today = int(input('Enter the price for today: ')) # or equal to 0.
            self.price[list(self.price)[-1] + datetime.timedelta(days=1)] = price_today
            # adds key (date) and value (price) into the price self.price dictionary
            print('enter a value less than or equal to 0 when finished entering prices')
            if price_today <= 0: # once user inputs a value less than or equal to 0,
                self.price.popitem() # pops the last key:value from the dictionary so it doesn't plot it.
                self.df = pd.DataFrame() # initializes a Pandas Dataframe
                self.df['Date'] = self.price.keys() # sets column of dates to the dates key of the dictionary.
                self.df['Prices'] = self.price.values() # sets column of prices to the price value of the dictionary.
                break # breaks from the while loop.


class Plot:
    def __init__(self, ag, env): # constructor that takes in agent and environment.
        self.ag = ag # assigns self.ag as the agent.
        self.env = env # assigns self.env as the environment.

    def plotagent(self):
        date = self.env.df['Date'] # assigns date as the Dates column in the environment's dataframe.
        price = self.env.df['Prices'] # assigns price as the Prices column in the environment's dataframe.
        plt.xlabel('Date') # labels the x axis as Date.
        plt.ylabel('Price') # labels the y axis as Price.
        plt.plot(date, price, label='price') # plots the date and price and labels it as price.
        plt.plot(date, self.ag.df['5 Period Moving Average'], label='5 Period Moving Average') # plots the 5 period moving average.
        plt.plot(date, self.ag.df['3 Period Moving Average'], label='3 Period Moving Average') # plots the 3 period moving average.
        plt.scatter(date, self.ag.df['buy signal price'], label='buy', marker='^', color='green') # plots where the agent bought.
        plt.scatter(date, self.ag.df['sell signal price'], label='sell', marker='v', color='red') # plots where the agent sold.
        plt.legend(loc='best') # puts the legend in the best location.
        plt.title('Stock Trading Agent') # sets the title as Stock Trading Agent.
        plt.show() # shows the graph.

    def plotpnl(self): # plots the profit and loss and agents cash balance.
        tradeno = self.ag.tradeno # assigns trade no as the agent's trade number list.
        pnl = self.ag.pnl # assigns pnl as the agent's pnl list.
        balance = self.ag.balance # assigns balance as the agent's balance list.
        plt.xlabel('Trade Number') # labels x axis as Trade Number.
        plt.ylabel('Amount in $') # labels y axis as Amount in $.
        plt.plot(tradeno,pnl, label='Profit & Loss') # plots trade number and pnl and labels it Profit & Loss.
        plt.plot(tradeno, balance, label='Account balance') # plots trade number and balance and labels it Account Balance.
        plt.legend(loc='best') # puts the legend in the best location.
        plt.title('Agent Balance and P&L') # sets the title as Agent Balance and P&L.
        plt.show() # shows the graph.

    def run(self): # the run function used to run the plot class.
        self.plotagent() # runs the agent plot.
        self.plotpnl() # runs the pnl and balance plot.





if __name__ == '__main__': # runs the script in this order.
    test = Environment() # creates test object as an environment class.
    testai = Agent(test) # creates testai object as an agent class then passes in the test environment.
    testai.run() # runs testai
    plot = Plot(testai,test) # creates plot object as plot class then passes testai, and test to plot.
    plot.run() # runs plot.

