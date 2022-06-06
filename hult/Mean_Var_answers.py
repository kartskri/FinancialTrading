# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 01:49:17 2019

@author: MichaelRolleigh
"""
# Timestamp indicates prof needs sleep
# Script to run mean-variance optimization for portfolio in bt.py

# Import the bt package so we can use the backtesting functions
import bt
import pandas as pd

# Intead of using a date to get the data in every call, I set up a variable here
# It is usually better to use variables so you can change things later in ONE place
# rather than many places. 
beginning = '2015-01-01'

# Import data
equity_list = ['AAPL', 'MCD', 'MSFT', 'TGT', 'GE', 'AMZN', 'ABBV', 'UPS', 'GM', 'IBM', 'PEP', 'VZ', 'DIS', 'INTC', 'FORD', 'CMCSA', 'IEF']
data = bt.get(equity_list, start=beginning)
data.head()

# We will need the risk-free rate to get correct Sharpe Ratios 
riskfree =  bt.get('^IRX', start=beginning)
# Convert risk free from % to decimal
riskfree_rate = float(riskfree.mean()) / 100
# Print out the risk free rate to make sure it looks good
print(riskfree_rate)

s_mark = bt.Strategy('Markowitz', 
                       [bt.algos.RunEveryNPeriods(30, offset=30),
                       bt.algos.SelectAll(),
                       bt.algos.WeighMeanVar(lookback=pd.DateOffset(months=3),bounds=(0.025,0.2), rf=riskfree_rate),
                       bt.algos.Rebalance()])

b_mark = bt.Backtest(s_mark, data)

result = bt.run(b_mark)
result.set_riskfree_rate(riskfree_rate)
result.plot()
# Show some performance metrics
result.display()
result.plot_security_weights()

benchmark = bt.Strategy('Benchmark',
                       [bt.algos.RunEveryNPeriods(30, offset=30),
                       bt.algos.SelectAll(),
                       bt.algos.WeighEqually(),
                       bt.algos.Rebalance()])
"""
benchmark = bt.Strategy('Benchmark', [bt.algos.RunMonthly(),
                       bt.algos.SelectAll(),
                       bt.algos.WeighEqually(),
                       bt.algos.Rebalance()])
"""
benchmark_test = bt.Backtest(benchmark, data)

results_both = bt.run(b_mark, benchmark_test)



results_both.display()
results_both.plot()

